//! Extracts Context variable by id and type
use crate::has_opcode::HasStaticOpCode;
use crate::serialization::op_code::OpCode;
use crate::serialization::sigma_byte_reader::SigmaByteRead;
use crate::serialization::sigma_byte_writer::SigmaByteWrite;
use crate::serialization::SigmaParsingError;
use crate::serialization::SigmaSerializable;
use crate::serialization::SigmaSerializeResult;
use crate::traversable::impl_traversable_expr;
use crate::types::stype::SType;

use super::expr::Expr;

/// Extract value of variable from context by its ID.
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct GetVar {
    /// ID of variable
    pub var_id: u8,
    /// Expected type of variable
    pub var_tpe: SType,
}

impl GetVar {
    /// Type
    pub fn tpe(&self) -> SType {
        SType::SOption(self.var_tpe.clone().into())
    }
}

impl HasStaticOpCode for GetVar {
    const OP_CODE: OpCode = OpCode::GET_VAR;
}

impl SigmaSerializable for GetVar {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        w.put_u8(self.var_id)?;
        self.var_tpe.sigma_serialize(w)
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        let var_id = r.get_u8()?;
        let var_tpe = SType::sigma_parse(r)?;
        Ok(Self { var_id, var_tpe })
    }
}

impl_traversable_expr!(GetVar);

/// Arbitrary impl
#[cfg(feature = "arbitrary")]
mod arbitrary {
    use super::*;
    use proptest::prelude::*;

    impl Arbitrary for GetVar {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = usize;

        fn arbitrary_with(_: Self::Parameters) -> Self::Strategy {
            (any::<u8>(), any::<SType>())
                .prop_map(|(var_id, var_tpe)| Self { var_id, var_tpe })
                .boxed()
        }
    }
}

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::panic)]
mod tests {
    use super::*;
    use crate::mir::expr::Expr;
    use crate::serialization::sigma_serialize_roundtrip;

    use proptest::prelude::*;

    proptest! {

        #[test]
        fn ser_roundtrip(v in any::<GetVar>()) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }

    }
}
