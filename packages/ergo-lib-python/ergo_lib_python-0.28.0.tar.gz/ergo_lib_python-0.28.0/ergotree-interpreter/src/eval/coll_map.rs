use alloc::string::ToString;
use alloc::sync::Arc;

use alloc::vec::Vec;
use ergotree_ir::mir::coll_map::Map;
use ergotree_ir::mir::value::CollKind;
use ergotree_ir::mir::value::Value;

use crate::eval::env::Env;
use crate::eval::Context;
use crate::eval::EvalError;
use crate::eval::Evaluable;

impl Evaluable for Map {
    fn eval<'ctx>(
        &self,
        env: &mut Env<'ctx>,
        ctx: &Context<'ctx>,
    ) -> Result<Value<'ctx>, EvalError> {
        let input_v = self.input.eval(env, ctx)?;
        let mapper_v = self.mapper.eval(env, ctx)?;
        let input_v_clone = input_v.clone();
        let mut mapper_call = |arg: Value<'ctx>| match &mapper_v {
            Value::Lambda(func_value) => {
                let func_arg = func_value.args.first().ok_or_else(|| {
                    EvalError::NotFound(
                        "Map: evaluated mapper has empty arguments list".to_string(),
                    )
                })?;
                let orig_val = env.get(func_arg.idx).cloned();
                env.insert(func_arg.idx, arg);
                let res = func_value.body.eval(env, ctx);
                if let Some(orig_val) = orig_val {
                    env.insert(func_arg.idx, orig_val);
                } else {
                    env.remove(&func_arg.idx);
                }
                res
            }
            _ => Err(EvalError::UnexpectedValue(format!(
                "expected mapper to be Value::FuncValue got: {0:?}",
                input_v_clone
            ))),
        };
        let mapper_input_tpe = self
            .mapper_sfunc
            .t_dom
            .first()
            .ok_or_else(|| {
                EvalError::NotFound(
                    "Map: mapper SFunc.t_dom is empty (does not have arguments)".to_string(),
                )
            })?
            .clone();
        let normalized_input_vals: Vec<Value> = match input_v {
            Value::Coll(coll) => {
                if *coll.elem_tpe() != mapper_input_tpe {
                    return Err(EvalError::UnexpectedValue(format!(
                        "expected Map input element type to be {0:?}, got: {1:?}",
                        mapper_input_tpe,
                        coll.elem_tpe()
                    )));
                };
                Ok(coll.as_vec())
            }
            _ => Err(EvalError::UnexpectedValue(format!(
                "expected Map input to be Value::Coll, got: {0:?}",
                input_v
            ))),
        }?;
        normalized_input_vals
            .iter()
            .map(|item| mapper_call(item.clone()))
            .collect::<Result<Arc<[Value]>, EvalError>>()
            .map(|values| {
                CollKind::from_collection(self.out_elem_tpe(), values)
                    .map_err(EvalError::TryExtractFrom)
            })
            .and_then(|v| v) // flatten <Result<Result<Value, _>, _>
            .map(Value::Coll)
    }
}

#[allow(clippy::panic)]
#[allow(clippy::unwrap_used)]
#[cfg(test)]
#[cfg(feature = "arbitrary")]
mod tests {

    use crate::eval::tests::eval_out;
    use ergotree_ir::chain::context::Context;
    use ergotree_ir::chain::context::TxIoVec;
    use ergotree_ir::mir::bin_op::ArithOp;
    use ergotree_ir::mir::bin_op::BinOp;
    use ergotree_ir::mir::expr::Expr;
    use ergotree_ir::mir::extract_amount::ExtractAmount;
    use ergotree_ir::mir::func_value::FuncArg;
    use ergotree_ir::mir::func_value::FuncValue;
    use ergotree_ir::mir::property_call::PropertyCall;
    use ergotree_ir::mir::unary_op::OneArgOpTryBuild;
    use ergotree_ir::mir::val_use::ValUse;
    use ergotree_ir::types::scontext;
    use ergotree_ir::types::stype::SType;

    use super::*;

    use proptest::prelude::*;

    proptest! {

        #![proptest_config(ProptestConfig::with_cases(16))]

        #[test]
        fn eval_box_value(ctx in any::<Context>()) {
            let data_inputs: Expr = PropertyCall::new(Expr::Context, scontext::DATA_INPUTS_PROPERTY.clone()).unwrap()
            .into();
            let val_use: Expr = ValUse {
                val_id: 1.into(),
                tpe: SType::SBox,
            }
            .into();
            let mapper_body: Expr = BinOp {
                kind: ArithOp::Plus.into(),
                left: Box::new(Expr::Const(1i64.into())),
                right: Box::new(Expr::ExtractAmount(
                        ExtractAmount::try_build(val_use)
                    .unwrap(),
                )),
            }
            .into();
            let expr: Expr = Map::new(
                data_inputs,
                FuncValue::new(
                    vec![FuncArg {
                        idx: 1.into(),
                        tpe: SType::SBox,
                    }],
                    mapper_body,
                )
                .into(),
            )
            .unwrap()
            .into();
            let output = {
                let e = eval_out::<Vec<i64>>(&expr, &ctx);
                if e.is_empty() {
                  None
                } else {
                  Some(TxIoVec::from_vec(e).unwrap())
                }
            };

            assert_eq!(
                output,
                ctx.data_inputs.clone().map(|d| d.iter().map(| b| b.value.as_i64() + 1).collect::<Vec<_>>().try_into().unwrap())
            );
        }

    }
}
