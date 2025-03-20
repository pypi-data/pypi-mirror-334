//! Code to implement `TokenAmount` JSON encoding

use core::convert::TryFrom;

use alloc::string::String;

use crate::chain::token::TokenAmount;

/// Helper struct to serialize/deserialize `TokenAmount`.
///
/// We use `serde_json::Number` below due to a known `serde_json` bug described here:
/// <https://github.com/serde-rs/json/issues/740>. Basically we can't deserialise any integer types
/// directly within untagged enums when the `arbitrary_precision` feature is used. The workaround is
/// to deserialize as `serde_json::Number` first, then manually convert the type.
///
/// Tries to decode as `BigInt` first, then fallback to string. Encodes as `BigInt` always.
/// see details - <https://docs.rs/serde_with/1.9.4/serde_with/struct.PickFirst.html>
#[cfg(feature = "json")]
#[serde_with::serde_as]
#[derive(serde::Serialize, serde::Deserialize)]
pub(crate) struct TokenAmountJson(
    #[serde_as(as = "serde_with::PickFirst<(_, serde_with::DisplayFromStr)>")] serde_json::Number,
);

impl TryFrom<TokenAmountJson> for TokenAmount {
    type Error = String;

    fn try_from(value: TokenAmountJson) -> Result<Self, Self::Error> {
        if let Some(n) = value.0.as_u64() {
            Ok(TokenAmount(n))
        } else {
            Err(String::from(
                "can't convert `TokenAmountJson` into `TokenAmount`",
            ))
        }
    }
}

impl From<TokenAmount> for TokenAmountJson {
    fn from(value: TokenAmount) -> Self {
        TokenAmountJson(serde_json::Number::from(value.0))
    }
}
