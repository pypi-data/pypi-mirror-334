//! Sigma serialization

#![cfg_attr(not(feature = "std"), no_std)]
// Coding conventions
#![forbid(unsafe_code)]
#![deny(non_upper_case_globals)]
#![deny(non_camel_case_types)]
#![deny(non_snake_case)]
#![deny(unused_mut)]
#![deny(dead_code)]
#![deny(unused_imports)]
#![deny(missing_docs)]
#![deny(clippy::unwrap_used)]
#![deny(clippy::expect_used)]
#![deny(clippy::todo)]
#![deny(clippy::unimplemented)]
#![deny(clippy::panic)]
#![deny(clippy::wildcard_enum_match_arm)]

extern crate alloc;

/// ScoreX Serialization
mod scorex_serialize;
pub use scorex_serialize::{
    scorex_serialize_roundtrip, ScorexParsingError, ScorexSerializable, ScorexSerializationError,
    ScorexSerializeResult,
};
/// VLQ encoder
pub mod vlq_encode;
/// ZigZag encoder
pub mod zig_zag_encode;
