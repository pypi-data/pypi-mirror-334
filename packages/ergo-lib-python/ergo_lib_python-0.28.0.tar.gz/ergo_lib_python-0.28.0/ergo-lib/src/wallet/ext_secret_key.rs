//! Extended private key operations according to BIP-32
use core::convert::TryInto;

use super::{
    derivation_path::{ChildIndex, ChildIndexError, DerivationPath},
    ext_pub_key::ExtPubKey,
    mnemonic::MnemonicSeed,
    secret_key::SecretKey,
};
use crate::ArrLength;
use alloc::{string::String, vec::Vec};
use ergotree_interpreter::sigma_protocol::{private_input::DlogProverInput, wscalar::Wscalar};
use ergotree_ir::{
    serialization::{SigmaParsingError, SigmaSerializable, SigmaSerializationError},
    sigma_protocol::sigma_boolean::ProveDlog,
};
use hmac::{Hmac, Mac};

use sha2::Sha512;
use thiserror::Error;

/// Private key (serialized Scalar) bytes
pub type SecretKeyBytes = [u8; 32];
/// Chain code bytes
pub type ChainCode = [u8; 32];

type HmacSha512 = Hmac<Sha512>;

/// Extended secret key
/// implemented according to BIP-32
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct ExtSecretKey {
    /// The secret key
    private_input: DlogProverInput,
    chain_code: ChainCode,
    derivation_path: DerivationPath,
}

/// Extended secret key errors
#[derive(Error, PartialEq, Eq, Debug, Clone)]
pub enum ExtSecretKeyError {
    /// Parsing error
    #[error("parsing error: {0}")]
    SigmaParsingError(#[from] SigmaParsingError),
    #[error("serialization error: {0}")]
    /// Serializing error
    SigmaSerializationError(#[from] SigmaSerializationError),
    /// Error encoding bytes as SEC-1-encoded scalar
    #[error("scalar encoding error")]
    ScalarEncodingError,
    /// Derivation path child index error
    /// For example trying to use a u32 value for a private index (31 bit size)
    #[error("child index error: {0}")]
    ChildIndexError(#[from] ChildIndexError),
    /// Incompatible derivation paths when trying to derive a new key
    #[error("incompatible paths: {0}")]
    IncompatibleDerivation(String),
}

impl ExtSecretKey {
    const BITCOIN_SEED: &'static [u8; 12] = b"Bitcoin seed";

    /// Create a new extended secret key instance
    pub fn new(
        secret_key_bytes: SecretKeyBytes,
        chain_code: ChainCode,
        derivation_path: DerivationPath,
    ) -> Result<Self, ExtSecretKeyError> {
        let private_input = DlogProverInput::from_bytes(&secret_key_bytes)
            .ok_or(ExtSecretKeyError::ScalarEncodingError)?;
        Ok(Self {
            private_input,
            chain_code,
            derivation_path,
        })
    }

    /// Derivation path associated with the ext secret key
    pub fn path(&self) -> DerivationPath {
        self.derivation_path.clone()
    }

    /// Returns secret key
    pub fn secret_key(&self) -> SecretKey {
        self.private_input.clone().into()
    }

    /// Byte representation of the underlying scalar
    pub fn secret_key_bytes(&self) -> SecretKeyBytes {
        self.private_input.to_bytes()
    }

    /// Public image associated with the private input
    pub fn public_image(&self) -> ProveDlog {
        self.private_input.public_image()
    }

    /// Public image bytes in SEC-1 encoded & compressed format
    pub fn public_image_bytes(&self) -> Result<Vec<u8>, ExtSecretKeyError> {
        Ok(self.public_image().h.sigma_serialize_bytes()?)
    }

    /// The extended public key associated with this secret key
    pub fn public_key(&self) -> Result<ExtPubKey, ExtSecretKeyError> {
        #[allow(clippy::unwrap_used)]
        Ok(ExtPubKey::new(
            // unwrap is safe as it is used on an Infallible result type
            self.public_image_bytes()?.try_into().unwrap(),
            self.chain_code,
            self.derivation_path.clone(),
        )?)
    }

    /// Derive a child extended secret key using the provided index
    pub fn child(&self, index: ChildIndex) -> Result<ExtSecretKey, ExtSecretKeyError> {
        // Unwrap is fine due to `ChainCode` type having fixed length of 32.
        #[allow(clippy::unwrap_used)]
        let mut mac = HmacSha512::new_from_slice(&self.chain_code).unwrap();
        match index {
            ChildIndex::Hardened(_) => {
                mac.update(&[0u8]);
                mac.update(&self.secret_key_bytes());
            }
            ChildIndex::Normal(_) => mac.update(&self.public_image_bytes()?),
        }
        mac.update(&index.to_bits().to_be_bytes());
        let mac_bytes = mac.finalize().into_bytes();
        let mut secret_key_bytes = [0; SecretKeyBytes::LEN];
        secret_key_bytes.copy_from_slice(&mac_bytes[..32]);
        if let Some(dlog_prover) = DlogProverInput::from_bytes(&secret_key_bytes) {
            // parse256(IL) + kpar (mod n).
            // via https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#child-key-derivation-ckd-functions
            let child_secret_key: DlogProverInput = Wscalar::from(
                dlog_prover
                    .w
                    .as_scalar_ref()
                    .add(self.private_input.w.as_scalar_ref()),
            )
            .into();
            if child_secret_key.is_zero() {
                // ki == 0 case of:
                // > In case parse256(IL) ≥ n or ki = 0, the resulting key is invalid, and one
                // > should proceed with the next value for i
                // via https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#child-key-derivation-ckd-functions
                self.child(index.next()?)
            } else {
                let mut chain_code = [0; ChainCode::LEN];
                chain_code.copy_from_slice(&mac_bytes[32..]);
                ExtSecretKey::new(
                    child_secret_key.to_bytes(),
                    chain_code,
                    self.derivation_path.extend(index),
                )
            }
        } else {
            // not in range [0, modulus), thus repeat with next index value (BIP-32)
            // This is the 'parse256(IL) ≥ n' case of:
            // > In case parse256(IL) ≥ n or ki = 0, the resulting key is invalid, and one
            // > should proceed with the next value for i
            // via https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#child-key-derivation-ckd-functions
            self.child(index.next()?)
        }
    }

    /// Derive a new extended secret key based on the provided derivation path
    pub fn derive(&self, up_path: DerivationPath) -> Result<ExtSecretKey, ExtSecretKeyError> {
        // TODO: branch visibility must also be equal
        let is_matching_path = up_path.0[..self.derivation_path.depth()]
            .iter()
            .zip(self.derivation_path.0.iter())
            .all(|(a, b)| a == b);

        if up_path.depth() >= self.derivation_path.depth() && is_matching_path {
            up_path.0[self.derivation_path.depth()..]
                .iter()
                .try_fold(self.clone(), |parent, i| parent.child(*i))
        } else {
            Err(ExtSecretKeyError::IncompatibleDerivation(format!(
                "{}, {}",
                up_path, self.derivation_path
            )))
        }
    }

    /// Derive a root master key from the provided mnemonic seed
    pub fn derive_master(seed: MnemonicSeed) -> Result<ExtSecretKey, ExtSecretKeyError> {
        // Unwrap is safe, we are using a valid static length slice
        #[allow(clippy::unwrap_used)]
        let mut mac = HmacSha512::new_from_slice(ExtSecretKey::BITCOIN_SEED).unwrap();
        mac.update(&seed);
        let hash = mac.finalize().into_bytes();
        let mut secret_key_bytes = [0; SecretKeyBytes::LEN];
        secret_key_bytes.copy_from_slice(&hash[..32]);
        let mut chain_code = [0; ChainCode::LEN];
        chain_code.copy_from_slice(&hash[32..]);

        ExtSecretKey::new(secret_key_bytes, chain_code, DerivationPath::master_path())
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used)]
mod tests {
    use ergotree_ir::chain::address::{Address, NetworkAddress};

    use crate::wallet::{
        derivation_path::{ChildIndexHardened, ChildIndexNormal},
        mnemonic::Mnemonic,
    };

    use super::*;
    // Covers the test cases found here: https://en.bitcoin.it/wiki/BIP_0032_TestVectors
    // Only tests secret key derivation, pub key derivation is tested in `ext_pub_key.rs`

    struct Bip32Vector {
        next_index: ChildIndex,
        expected_secret_key: [u8; 32],
    }

    impl Bip32Vector {
        pub fn new(next_index: &str, expected_secret_key: &str) -> Self {
            Bip32Vector {
                next_index: next_index.parse::<ChildIndex>().unwrap(),
                expected_secret_key: base16::decode(expected_secret_key)
                    .unwrap()
                    .try_into()
                    .unwrap(),
            }
        }
    }

    #[test]
    fn bip32_test_vector1() {
        let vectors = vec![
            // m/0'
            Bip32Vector::new(
                "0'",
                "edb2e14f9ee77d26dd93b4ecede8d16ed408ce149b6cd80b0715a2d911a0afea",
            ),
            // m/0'/1
            Bip32Vector::new(
                "1",
                "3c6cb8d0f6a264c91ea8b5030fadaa8e538b020f0a387421a12de9319dc93368",
            ),
            // m/0'/1/2'
            Bip32Vector::new(
                "2'",
                "cbce0d719ecf7431d88e6a89fa1483e02e35092af60c042b1df2ff59fa424dca",
            ),
            // m/0'/1/2'/2
            Bip32Vector::new(
                "2",
                "0f479245fb19a38a1954c5c7c0ebab2f9bdfd96a17563ef28a6a4b1a2a764ef4",
            ),
            // m/0'/1/2'/2/1000000000
            Bip32Vector::new(
                "1000000000",
                "471b76e389e528d6de6d816857e012c5455051cad6660850e58372a6c3e6e7c8",
            ),
        ];
        let secret_key =
            base16::decode(b"e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35")
                .unwrap();
        let chain_code =
            base16::decode(b"873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508")
                .unwrap();
        let mut ext_secret_key = ExtSecretKey::new(
            secret_key.try_into().unwrap(),
            chain_code.try_into().unwrap(),
            DerivationPath::master_path(),
        )
        .unwrap();

        for v in vectors {
            ext_secret_key = ext_secret_key.child(v.next_index).unwrap();
            assert_eq!(ext_secret_key.secret_key_bytes(), v.expected_secret_key);
        }
    }

    #[test]
    fn bip32_test_vector2() {
        let vectors = vec![
            // m/0
            Bip32Vector::new(
                "0",
                "abe74a98f6c7eabee0428f53798f0ab8aa1bd37873999041703c742f15ac7e1e",
            ),
            // m/0/2147483647'
            Bip32Vector::new(
                "2147483647'",
                "877c779ad9687164e9c2f4f0f4ff0340814392330693ce95a58fe18fd52e6e93",
            ),
            // m/0/2147483647'/1
            Bip32Vector::new(
                "1",
                "704addf544a06e5ee4bea37098463c23613da32020d604506da8c0518e1da4b7",
            ),
            // m/0/2147483647'/1/2147483646'
            Bip32Vector::new(
                "2147483646'",
                "f1c7c871a54a804afe328b4c83a1c33b8e5ff48f5087273f04efa83b247d6a2d",
            ),
            // m/0/2147483647'/1/2147483646'/2
            Bip32Vector::new(
                "2",
                "bb7d39bdb83ecf58f2fd82b6d918341cbef428661ef01ab97c28a4842125ac23",
            ),
        ];
        let secret_key =
            base16::decode(b"4b03d6fc340455b363f51020ad3ecca4f0850280cf436c70c727923f6db46c3e")
                .unwrap();
        let chain_code =
            base16::decode(b"60499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd9689")
                .unwrap();
        let mut ext_secret_key = ExtSecretKey::new(
            secret_key.try_into().unwrap(),
            chain_code.try_into().unwrap(),
            DerivationPath::master_path(),
        )
        .unwrap();

        for v in vectors {
            ext_secret_key = ext_secret_key.child(v.next_index).unwrap();
            assert_eq!(ext_secret_key.secret_key_bytes(), v.expected_secret_key);
        }
    }

    #[test]
    fn ergo_node_key_tree_derivation_from_seed() {
        // Tests against the following ergo node test vector:
        // https://github.com/ergoplatform/ergo/blob/c320810c498bca25a44197840c7c5a86440c5906/ergo-wallet/src/test/scala/org/ergoplatform/wallet/secrets/ExtendedSecretKeySpec.scala#L18-L35
        let seed_str = "edge talent poet tortoise trumpet dose";
        let seed = Mnemonic::to_seed(seed_str, "");
        let expected_root = "4rEDKLd17LX4xNR8ss4ithdqFRc3iFnTiTtQbanWJbCT";
        let cases: Vec<(&str, ChildIndex)> = vec![
            (
                "CLdMMHxNtiPzDnWrVuZQr22VyUx8deUG7vMqMNW7as7M",
                ChildIndexNormal::normal(1).unwrap().into(),
            ),
            (
                "9icjp3TuTpRaTn6JK6AHw2nVJQaUnwmkXVdBdQSS98xD",
                ChildIndexNormal::normal(2).unwrap().into(),
            ),
            (
                "DWMp3L9JZiywxSb5gSjc5dYxPwEZ6KkmasNiHD6VRcpJ",
                ChildIndexHardened::from_31_bit(2).unwrap().into(),
            ),
        ];

        let mut ext_secret_key = ExtSecretKey::derive_master(seed).unwrap();
        let ext_secret_key_b58 = bs58::encode(ext_secret_key.secret_key_bytes()).into_string();

        assert_eq!(expected_root, ext_secret_key_b58);

        for (expected_key, idx) in cases {
            ext_secret_key = ext_secret_key.child(idx).unwrap();
            let ext_secret_key_b58 = bs58::encode(ext_secret_key.secret_key_bytes()).into_string();

            assert_eq!(expected_key, ext_secret_key_b58);
        }
    }

    #[test]
    fn ergo_node_path_derivation() {
        // Tests against the following ergo node test vector:
        // https://github.com/ergoplatform/ergo/blob/c320810c498bca25a44197840c7c5a86440c5906/ergo-wallet/src/test/scala/org/ergoplatform/wallet/secrets/ExtendedSecretKeySpec.scala#L37-L50
        let seed_str = "edge talent poet tortoise trumpet dose";
        let seed = Mnemonic::to_seed(seed_str, "");
        let cases: Vec<(&str, &str)> = vec![
            ("CLdMMHxNtiPzDnWrVuZQr22VyUx8deUG7vMqMNW7as7M", "m/1"),
            ("9icjp3TuTpRaTn6JK6AHw2nVJQaUnwmkXVdBdQSS98xD", "m/1/2"),
            ("DWMp3L9JZiywxSb5gSjc5dYxPwEZ6KkmasNiHD6VRcpJ", "m/1/2/2'"),
        ];

        let root = ExtSecretKey::derive_master(seed).unwrap();

        for (expected_key, path) in cases {
            let derived = root.derive(path.parse().unwrap()).unwrap();
            let ext_secret_key_b58 = bs58::encode(derived.secret_key_bytes()).into_string();

            assert_eq!(expected_key, ext_secret_key_b58);
        }
    }

    #[test]
    fn ergo_wallet_incorrect_bip32_derivation() {
        // test vector triggering ergo-wallet's incorrect BIP32 key derivation
        // see https://github.com/ergoplatform/ergo/issues/1627
        let seed_str = "race relax argue hair sorry riot there spirit ready fetch food hedgehog hybrid mobile pretty";
        let seed = Mnemonic::to_seed(seed_str, "");

        // in ergo-wallet the above mnemonic produces "9ewv8sxJ1jfr6j3WUSbGPMTVx3TZgcJKdnjKCbJWhiJp5U62uhP";
        let expected_p2pk = "9eYMpbGgBf42bCcnB2nG3wQdqPzpCCw5eB1YaWUUen9uCaW3wwm";
        let path = "m/44'/429'/0'/0/0";

        let root = ExtSecretKey::derive_master(seed).unwrap();

        let derived = root.derive(path.parse().unwrap()).unwrap();
        let p2pk: Address = derived.public_key().unwrap().into();
        let mainnet_p2pk =
            NetworkAddress::new(ergotree_ir::chain::address::NetworkPrefix::Mainnet, &p2pk);

        assert_eq!(expected_p2pk, mainnet_p2pk.to_base58());
    }

    #[test]
    fn appkit_test_vector() {
        // from https://github.com/ergoplatform/ergo-appkit/blob/b77b6910bb36a26d5d46d41ae3af8ae1167c902c/common/src/test/scala/org/ergoplatform/appkit/AppkitTestingCommon.scala#L4-L21
        let seed_str = "slow silly start wash bundle suffer bulb ancient height spin express remind today effort helmet";
        let seed = Mnemonic::to_seed(seed_str, "");
        let root = ExtSecretKey::derive_master(seed).unwrap();

        let mainnet_p2pk0 = NetworkAddress::new(
            ergotree_ir::chain::address::NetworkPrefix::Mainnet,
            &root
                .derive("m/44'/429'/0'/0/0".parse().unwrap())
                .unwrap()
                .public_key()
                .unwrap()
                .into(),
        );
        let expected_p2pk0 = "9eatpGQdYNjTi5ZZLK7Bo7C3ms6oECPnxbQTRn6sDcBNLMYSCa8";

        assert_eq!(expected_p2pk0, mainnet_p2pk0.to_base58());

        let mainnet_p2pk1 = NetworkAddress::new(
            ergotree_ir::chain::address::NetworkPrefix::Mainnet,
            &root
                .derive("m/44'/429'/0'/0/1".parse().unwrap())
                .unwrap()
                .public_key()
                .unwrap()
                .into(),
        );
        let expected_p2pk1 = "9iBhwkjzUAVBkdxWvKmk7ab7nFgZRFbGpXA9gP6TAoakFnLNomk";

        assert_eq!(expected_p2pk1, mainnet_p2pk1.to_base58());
    }
}
