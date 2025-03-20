//! Convert byte array to SLong
use alloc::boxed::Box;
use alloc::sync::Arc;

use crate::serialization::op_code::OpCode;
use crate::types::stype::SType;

use super::expr::Expr;
use super::expr::InvalidArgumentError;
use super::unary_op::OneArgOp;
use super::unary_op::OneArgOpTryBuild;
use crate::has_opcode::HasStaticOpCode;

/// Convert byte array to SLong
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct ByteArrayToLong {
    /// Byte array with SColl(SByte) expr type
    pub input: Box<Expr>,
}

impl ByteArrayToLong {
    /// Type
    pub fn tpe(&self) -> SType {
        SType::SLong
    }
}

impl HasStaticOpCode for ByteArrayToLong {
    const OP_CODE: OpCode = OpCode::BYTE_ARRAY_TO_LONG;
}

impl OneArgOp for ByteArrayToLong {
    fn input(&self) -> &Expr {
        &self.input
    }
    fn input_mut(&mut self) -> &mut Expr {
        &mut self.input
    }
}

impl OneArgOpTryBuild for ByteArrayToLong {
    fn try_build(input: Expr) -> Result<Self, InvalidArgumentError> {
        input.check_post_eval_tpe(&SType::SColl(Arc::new(SType::SByte)))?;
        Ok(ByteArrayToLong {
            input: Box::new(input),
        })
    }
}

#[cfg(feature = "arbitrary")]
/// Arbitrary impl
mod arbitrary {
    use crate::mir::expr::arbitrary::ArbExprParams;

    use super::*;
    use proptest::prelude::*;

    impl Arbitrary for ByteArrayToLong {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = ();

        fn arbitrary_with(_args: Self::Parameters) -> Self::Strategy {
            any_with::<Expr>(ArbExprParams {
                tpe: SType::SColl(SType::SByte.into()),
                depth: 0,
            })
            .prop_map(|input| Self {
                input: input.into(),
            })
            .boxed()
        }
    }
}

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::panic)]
mod tests {
    use super::*;
    use crate::serialization::sigma_serialize_roundtrip;

    use proptest::prelude::*;

    proptest! {

        #[test]
        fn ser_roundtrip(v in any::<ByteArrayToLong>()) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }
    }
}
