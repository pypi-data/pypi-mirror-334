//! Substitution of constants in serialized sigma expression
use alloc::boxed::Box;

use super::expr::Expr;
use crate::has_opcode::HasStaticOpCode;
use crate::mir::expr::InvalidArgumentError;
use crate::serialization::op_code::OpCode;
use crate::serialization::sigma_byte_reader::SigmaByteRead;
use crate::serialization::sigma_byte_writer::SigmaByteWrite;
use crate::serialization::SigmaParsingError;
use crate::serialization::SigmaSerializable;
use crate::serialization::SigmaSerializeResult;
use crate::traversable::impl_traversable_expr;
use crate::types::stype::SType;

#[derive(PartialEq, Eq, Debug, Clone)]
/// Substitute constants in the serialized representation of sigma script. Returns
/// original scriptBytes array where only specified constants are replaced and all
/// other bytes remain exactly the same.
pub struct SubstConstants {
    /// Serialized ergo tree with ConstantSegregationFlag set to 1.
    pub script_bytes: Box<Expr>,
    /// Zero based indexes in ErgoTree.constants array which should be
    /// replaced with new values.
    pub positions: Box<Expr>,
    /// New values to be injected into the corresponding positions in ErgoTree.constants
    /// array.
    pub new_values: Box<Expr>,
}

impl SubstConstants {
    /// Create new object, returning error if requirements failed
    pub fn new(
        script_bytes: Expr,
        positions: Expr,
        new_values: Expr,
    ) -> Result<Self, InvalidArgumentError> {
        script_bytes.check_post_eval_tpe(&SType::SColl(SType::SByte.into()))?;
        positions.check_post_eval_tpe(&SType::SColl(SType::SInt.into()))?;
        match new_values.post_eval_tpe() {
            SType::SColl(_) => Ok(SubstConstants {
                script_bytes: script_bytes.into(),
                positions: positions.into(),
                new_values: new_values.into(),
            }),
            e => Err(InvalidArgumentError(format!(
                "SubstConstants: expected new_values type to be SColl[T], got {:?}",
                e
            ))),
        }
    }
    /// Type of returned value
    pub fn tpe(&self) -> SType {
        SType::SColl(SType::SByte.into())
    }
}

impl HasStaticOpCode for SubstConstants {
    const OP_CODE: OpCode = OpCode::SUBST_CONSTANTS;
}

impl SigmaSerializable for SubstConstants {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.script_bytes.sigma_serialize(w)?;
        self.positions.sigma_serialize(w)?;
        self.new_values.sigma_serialize(w)
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        let script_bytes = Expr::sigma_parse(r)?;
        let positions = Expr::sigma_parse(r)?;
        let new_values = Expr::sigma_parse(r)?;
        Ok(SubstConstants::new(script_bytes, positions, new_values)?)
    }
}

impl_traversable_expr!(SubstConstants, boxed script_bytes, boxed positions, boxed new_values);

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::panic)]
mod tests {
    use super::*;
    use crate::mir::expr::arbitrary::ArbExprParams;
    use crate::mir::expr::Expr;
    use crate::serialization::sigma_serialize_roundtrip;
    use proptest::prelude::*;

    impl Arbitrary for SubstConstants {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = ();

        fn arbitrary_with(_args: Self::Parameters) -> Self::Strategy {
            (
                any_with::<Expr>(ArbExprParams {
                    tpe: SType::SColl(SType::SByte.into()),
                    depth: 0,
                }),
                any_with::<Expr>(ArbExprParams {
                    tpe: SType::SColl(SType::SInt.into()),
                    depth: 0,
                }),
                prop_oneof![
                    Just(SType::SByte),
                    Just(SType::SBoolean),
                    Just(SType::SShort),
                    Just(SType::SInt),
                    Just(SType::SLong),
                ]
                .prop_flat_map(|ty| {
                    any_with::<Expr>(ArbExprParams {
                        tpe: SType::SColl(ty.into()),
                        depth: 0,
                    })
                }),
            )
                .prop_map(|(script_bytes, positions, new_values)| Self {
                    script_bytes: script_bytes.into(),
                    positions: positions.into(),
                    new_values: new_values.into(),
                })
                .boxed()
        }
    }

    proptest! {

        #![proptest_config(ProptestConfig::with_cases(16))]

        #[test]
        fn ser_roundtrip(v in any::<SubstConstants>()) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }
    }
}
