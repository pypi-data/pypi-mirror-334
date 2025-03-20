use alloc::boxed::Box;

use super::expr::Expr;
use super::unary_op::OneArgOp;
use crate::has_opcode::HasStaticOpCode;
use crate::serialization::op_code::OpCode;
use crate::serialization::sigma_byte_reader::SigmaByteRead;
use crate::serialization::sigma_byte_writer::SigmaByteWrite;
use crate::serialization::SigmaParsingError;
use crate::serialization::SigmaSerializable;
use crate::serialization::SigmaSerializeResult;
use crate::types::stype::SType;

/// Logical OR op on collection of SBoolean values
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct Or {
    /// Input collection
    pub input: Box<Expr>,
}

impl Or {
    /// Type
    pub fn tpe(&self) -> SType {
        SType::SBoolean
    }
}

impl HasStaticOpCode for Or {
    const OP_CODE: OpCode = OpCode::OR;
}

impl SigmaSerializable for Or {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.input.sigma_serialize(w)
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        Ok(Self {
            input: Expr::sigma_parse(r)?.into(),
        })
    }
}

impl OneArgOp for Or {
    fn input(&self) -> &Expr {
        &self.input
    }

    fn input_mut(&mut self) -> &mut Expr {
        &mut self.input
    }
}

#[cfg(feature = "arbitrary")]
/// Arbitrary impl
mod arbitrary {
    use crate::mir::expr::arbitrary::ArbExprParams;

    use super::*;

    use proptest::prelude::*;

    impl Arbitrary for Or {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = usize;

        fn arbitrary_with(args: Self::Parameters) -> Self::Strategy {
            any_with::<Expr>(ArbExprParams {
                tpe: SType::SColl(SType::SBoolean.into()),
                depth: args,
            })
            .prop_map(|input| Self {
                input: input.into(),
            })
            .boxed()
        }
    }
}

#[cfg(test)]
#[allow(clippy::panic)]
#[cfg(feature = "arbitrary")]
mod tests {
    use super::*;
    use crate::mir::expr::Expr;
    use crate::serialization::sigma_serialize_roundtrip;
    use proptest::prelude::*;

    proptest! {

        #[test]
        fn ser_roundtrip(v in any_with::<Or>(1)) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }

    }
}
