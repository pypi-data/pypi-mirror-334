use alloc::boxed::Box;

use crate::serialization::op_code::OpCode;
use crate::serialization::sigma_byte_reader::SigmaByteRead;
use crate::serialization::sigma_byte_writer::SigmaByteWrite;
use crate::serialization::SigmaParsingError;
use crate::serialization::SigmaSerializable;
use crate::serialization::SigmaSerializeResult;
use crate::traversable::impl_traversable_expr;
use crate::types::sfunc::SFunc;
use crate::types::stype::SType;

use super::expr::Expr;
use super::expr::InvalidArgumentError;
use crate::has_opcode::HasStaticOpCode;

/// Builds a new collection by applying a function to all elements of this collection.
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct Map {
    /// Collection
    pub input: Box<Expr>,
    /// Function (lambda) to apply to each element
    pub mapper: Box<Expr>,
    /// Type signature of the function(mapper)
    pub mapper_sfunc: SFunc,
}

impl Map {
    /// Create new object, returns an error if any of the requirements failed
    pub fn new(input: Expr, mapper: Expr) -> Result<Self, InvalidArgumentError> {
        let input_elem_type = match input.post_eval_tpe() {
            SType::SColl(elem_type) => Ok(elem_type),
            _ => Err(InvalidArgumentError(format!(
                "Expected Map input to be SColl, got {0:?}",
                input.tpe()
            ))),
        }?;
        match mapper.tpe() {
            SType::SFunc(sfunc) if sfunc.t_dom.len() == 1 && sfunc.t_dom[0] == *input_elem_type => {
                Ok(Map {
                    input: input.into(),
                    mapper: mapper.into(),
                    mapper_sfunc: sfunc,
                })
            }
            _ => Err(InvalidArgumentError(format!(
                "Invalid mapper tpe: {0:?}",
                mapper.tpe()
            ))),
        }
    }

    /// Type
    pub fn tpe(&self) -> SType {
        SType::SColl(self.mapper_sfunc.t_range.clone().into())
    }

    /// Type of the element in the resulted collection
    pub fn out_elem_tpe(&self) -> SType {
        *self.mapper_sfunc.t_range.clone()
    }
}

impl HasStaticOpCode for Map {
    const OP_CODE: OpCode = OpCode::MAP;
}

impl SigmaSerializable for Map {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.input.sigma_serialize(w)?;
        self.mapper.sigma_serialize(w)
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        let input = Expr::sigma_parse(r)?;
        let mapper = Expr::sigma_parse(r)?;
        Ok(Map::new(input, mapper)?)
    }
}

impl_traversable_expr!(Map, boxed input, boxed mapper);

#[cfg(feature = "arbitrary")]
/// Arbitrary impl
#[allow(clippy::unwrap_used)]
mod arbitrary {
    use super::*;
    use crate::mir::expr::arbitrary::ArbExprParams;
    use alloc::vec;
    use proptest::prelude::*;

    impl Arbitrary for Map {
        type Strategy = BoxedStrategy<Self>;
        type Parameters = ();

        fn arbitrary_with(_args: Self::Parameters) -> Self::Strategy {
            (
                any_with::<Expr>(ArbExprParams {
                    tpe: SType::SColl(SType::SBoolean.into()),
                    depth: 1,
                }),
                any_with::<Expr>(ArbExprParams {
                    tpe: SType::SFunc(SFunc {
                        t_dom: vec![SType::SBoolean],
                        t_range: SType::SBoolean.into(),
                        tpe_params: vec![],
                    }),
                    depth: 0,
                }),
            )
                .prop_map(|(input, mapper)| Map::new(input, mapper).unwrap())
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

        #![proptest_config(ProptestConfig::with_cases(16))]

        #[test]
        fn ser_roundtrip(v in any::<Map>()) {
            let expr: Expr = v.into();
            prop_assert_eq![sigma_serialize_roundtrip(&expr), expr];
        }
    }
}
