//! Traits for IR nodes with one input value(expr)

use crate::serialization::sigma_byte_reader::SigmaByteRead;
use crate::serialization::sigma_byte_writer::SigmaByteWrite;
use crate::serialization::SigmaParsingError;
use crate::serialization::SigmaSerializable;
use crate::serialization::SigmaSerializeResult;

use super::expr::Expr;
use super::expr::InvalidArgumentError;

/// IR nodes with one input value(expr)
pub trait OneArgOp {
    /// Input value(expr) of the IR node
    fn input(&self) -> &Expr;
    /// Mutable reference to input value(expr) of the IR node
    fn input_mut(&mut self) -> &mut Expr;
}

/// Constructor for unary IR nodes that check the validity of the argument
pub trait OneArgOpTryBuild: Sized {
    /// Create new IR node, returns an error if any of the requirements failed
    fn try_build(input: Expr) -> Result<Self, InvalidArgumentError>;
}

impl<T: OneArgOp + OneArgOpTryBuild> SigmaSerializable for T {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.input().sigma_serialize(w)
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        let input = Expr::sigma_parse(r)?;
        let r = T::try_build(input)?;
        Ok(r)
    }
}
