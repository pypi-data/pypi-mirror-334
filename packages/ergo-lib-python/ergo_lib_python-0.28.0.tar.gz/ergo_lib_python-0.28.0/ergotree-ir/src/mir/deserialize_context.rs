//! Extracts context variable as byte array

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

/// Extracts context variable as `Coll[Byte]`, deserializes it to script and then executes
/// this script in the current context. The original `Coll[Byte]` of the script is
/// available as `getVar[Coll[Byte]](id)` On evaluation returns the result of the
/// script execution in the current context
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct DeserializeContext {
    /// Result type of the deserialized script
    pub tpe: SType,
    /// identifier of the context variable
    pub id: u8,
}
impl DeserializeContext {
    /// Type of value
    pub fn tpe(&self) -> SType {
        self.tpe.clone()
    }
}

impl HasStaticOpCode for DeserializeContext {
    const OP_CODE: OpCode = OpCode::DESERIALIZE_CONTEXT;
}

impl SigmaSerializable for DeserializeContext {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.tpe.sigma_serialize(w)?;
        w.put_u8(self.id)?;
        Ok(())
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        r.set_deserialize(true);
        let tpe = SType::sigma_parse(r)?;
        let id = r.get_u8()?;
        Ok(Self { tpe, id })
    }
}

impl_traversable_expr!(DeserializeContext);

#[cfg(feature = "arbitrary")]
/// Arbitrary impl
mod arbitrary {
    use super::*;

    use proptest::prelude::*;

    impl Arbitrary for DeserializeContext {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = ();

        fn arbitrary_with(_: Self::Parameters) -> Self::Strategy {
            (0_u8..9, any::<SType>())
                .prop_map(|(id, tpe)| Self { tpe, id })
                .boxed()
        }
    }
}

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::panic)]
mod tests {
    use crate::mir::expr::Expr;
    use crate::serialization::sigma_serialize_roundtrip;

    use super::*;

    use proptest::prelude::*;

    proptest! {
        #![proptest_config(ProptestConfig::with_cases(16))]

        #[test]
        fn ser_roundtrip(v in any::<DeserializeContext>()) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }
    }
}
