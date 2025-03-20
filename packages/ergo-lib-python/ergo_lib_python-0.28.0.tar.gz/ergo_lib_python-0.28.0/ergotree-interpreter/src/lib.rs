//! ErgoTree interpreter

#![cfg_attr(not(feature = "std"), no_std)]
// Coding conventions
#![forbid(unsafe_code)]
#![allow(clippy::needless_lifetimes)]
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
#![deny(clippy::unwrap_used)]
#![deny(clippy::expect_used)]
#![deny(clippy::todo)]
#![deny(clippy::unimplemented)]
#![deny(clippy::unreachable)]
#![deny(clippy::panic)]

#[macro_use]
extern crate alloc;

mod contracts;

pub mod eval;
pub mod sigma_protocol;

#[cfg(feature = "json")]
pub mod json;
