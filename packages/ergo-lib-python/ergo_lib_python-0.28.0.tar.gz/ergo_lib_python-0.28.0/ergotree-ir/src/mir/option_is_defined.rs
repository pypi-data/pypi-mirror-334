use alloc::boxed::Box;

use super::expr::Expr;
use super::expr::InvalidArgumentError;
use super::unary_op::OneArgOp;
use super::unary_op::OneArgOpTryBuild;
use crate::has_opcode::HasStaticOpCode;
use crate::serialization::op_code::OpCode;
use crate::types::stype::SType;

/// Returns false if the option is None, true otherwise.
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct OptionIsDefined {
    /// Object of SOption type
    pub input: Box<Expr>,
}

impl OptionIsDefined {
    /// Type
    pub fn tpe(&self) -> SType {
        SType::SBoolean
    }
}

impl HasStaticOpCode for OptionIsDefined {
    const OP_CODE: OpCode = OpCode::OPTION_IS_DEFINED;
}

impl OneArgOp for OptionIsDefined {
    fn input(&self) -> &Expr {
        &self.input
    }
    fn input_mut(&mut self) -> &mut Expr {
        &mut self.input
    }
}

impl OneArgOpTryBuild for OptionIsDefined {
    fn try_build(input: Expr) -> Result<Self, InvalidArgumentError>
    where
        Self: Sized,
    {
        match input.post_eval_tpe() {
            SType::SOption(_) => Ok(OptionIsDefined {
                input: Box::new(input),
            }),
            _ => Err(InvalidArgumentError(format!(
                "expected OptionIsDefined::input type to be SOption, got: {0:?}",
                input.tpe(),
            ))),
        }
    }
}

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::unwrap_used)]
mod tests {
    use super::*;
    use crate::mir::expr::Expr;
    use crate::mir::extract_reg_as::ExtractRegisterAs;
    use crate::mir::global_vars::GlobalVars;
    use crate::serialization::sigma_serialize_roundtrip;
    use crate::types::stype::SType;

    #[test]
    fn ser_roundtrip() {
        let get_reg_expr: Expr = ExtractRegisterAs::new(
            GlobalVars::SelfBox.into(),
            0,
            SType::SOption(SType::SLong.into()),
        )
        .unwrap()
        .into();
        let e: Expr = OptionIsDefined::try_build(get_reg_expr).unwrap().into();
        assert_eq![sigma_serialize_roundtrip(&e), e];
    }
}
