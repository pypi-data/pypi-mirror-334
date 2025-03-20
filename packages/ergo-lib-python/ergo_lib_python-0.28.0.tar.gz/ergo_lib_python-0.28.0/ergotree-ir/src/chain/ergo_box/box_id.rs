//! Box id type
use core::convert::TryFrom;
use derive_more::FromStr;

use crate::serialization::SigmaSerializeResult;
use alloc::string::String;
use alloc::vec::Vec;
use sigma_ser::ScorexSerializable;

use crate::serialization::{
    sigma_byte_reader::SigmaByteRead, sigma_byte_writer::SigmaByteWrite, SigmaParsingError,
    SigmaSerializable,
};
use derive_more::From;
use derive_more::Into;
use ergo_chain_types::{Digest32, DigestNError};
use sigma_util::AsVecI8;

/// newtype for box ids
#[derive(PartialEq, Eq, PartialOrd, Ord, Hash, Debug, Copy, Clone, From, FromStr, Into)]
#[cfg_attr(feature = "json", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "arbitrary", derive(proptest_derive::Arbitrary))]
pub struct BoxId(Digest32);

impl BoxId {
    /// Size in bytes
    pub const SIZE: usize = Digest32::SIZE;

    /// All zeros
    pub fn zero() -> BoxId {
        BoxId(Digest32::zero())
    }
}

impl AsRef<[u8]> for BoxId {
    fn as_ref(&self) -> &[u8] {
        self.0.as_ref()
    }
}

impl From<BoxId> for String {
    fn from(v: BoxId) -> Self {
        v.0.into()
    }
}

impl TryFrom<String> for BoxId {
    type Error = DigestNError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Ok(Digest32::try_from(value)?.into())
    }
}

impl From<BoxId> for Vec<i8> {
    fn from(b: BoxId) -> Self {
        let bytes: Vec<u8> = b.0.into();
        bytes.as_vec_i8()
    }
}

impl core::fmt::Display for BoxId {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl SigmaSerializable for BoxId {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.0.scorex_serialize(w)?;
        Ok(())
    }
    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        Ok(Self(Digest32::scorex_parse(r)?))
    }
}

#[allow(clippy::unwrap_used)]
#[allow(clippy::panic)]
#[cfg(test)]
#[cfg(feature = "arbitrary")]
mod tests {
    use super::*;
    use crate::serialization::sigma_serialize_roundtrip;

    use proptest::prelude::*;

    proptest! {

        #[test]
        fn ser_roundtrip(v in any::<BoxId>()) {
            prop_assert_eq![sigma_serialize_roundtrip(&v), v];
        }
    }
}
