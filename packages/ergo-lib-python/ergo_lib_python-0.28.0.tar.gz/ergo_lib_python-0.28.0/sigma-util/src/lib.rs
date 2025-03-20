//! Ergo primitives
#![no_std]
// Coding conventions
#![forbid(unsafe_code)]
#![deny(non_upper_case_globals)]
#![deny(non_camel_case_types)]
#![deny(non_snake_case)]
#![deny(unused_mut)]
#![deny(dead_code)]
#![deny(unused_imports)]
#![deny(missing_docs)]
// Clippy exclusions
#![allow(clippy::unit_arg)]
#![deny(rustdoc::broken_intra_doc_links)]

extern crate alloc;

pub mod hash;
mod vec_ext;

pub use vec_ext::AsVecI8;
pub use vec_ext::AsVecU8;
pub use vec_ext::FromVecI8;

/// 32 byte array used in box, transaction ids (hash)
pub const DIGEST32_SIZE: usize = 32;
