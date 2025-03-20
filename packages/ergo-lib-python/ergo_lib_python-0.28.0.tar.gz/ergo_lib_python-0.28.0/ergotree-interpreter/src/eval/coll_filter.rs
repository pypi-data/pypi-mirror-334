use alloc::string::ToString;
use alloc::sync::Arc;

use alloc::vec::Vec;
use ergotree_ir::mir::coll_filter::Filter;
use ergotree_ir::mir::constant::TryExtractInto;
use ergotree_ir::mir::value::CollKind;
use ergotree_ir::mir::value::Value;

use crate::eval::env::Env;
use crate::eval::Context;
use crate::eval::EvalError;
use crate::eval::Evaluable;

impl Evaluable for Filter {
    fn eval<'ctx>(
        &self,
        env: &mut Env<'ctx>,
        ctx: &Context<'ctx>,
    ) -> Result<Value<'ctx>, EvalError> {
        let input_v = self.input.eval(env, ctx)?;
        let condition_v = self.condition.eval(env, ctx)?;
        let input_v_clone = input_v.clone();
        let mut condition_call = |arg: Value<'ctx>| match &condition_v {
            Value::Lambda(func_value) => {
                let func_arg = func_value.args.first().ok_or_else(|| {
                    EvalError::NotFound(
                        "Filter: evaluated condition has empty arguments list".to_string(),
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
                "expected Filter::condition to be Value::FuncValue got: {0:?}",
                input_v_clone
            ))),
        };
        let normalized_input_vals: Vec<Value> = match input_v {
            Value::Coll(coll) => {
                if coll.elem_tpe() != &*self.elem_tpe {
                    return Err(EvalError::UnexpectedValue(format!(
                        "expected Filter input element type to be {0:?}, got: {1:?}",
                        self.elem_tpe,
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

        let items_conditions: Vec<bool> = normalized_input_vals
            .clone()
            .into_iter()
            .map(|item| {
                condition_call(item).and_then(|res| {
                    res.try_extract_into::<bool>()
                        .map_err(EvalError::TryExtractFrom)
                })
            })
            .collect::<Result<Vec<bool>, EvalError>>()?;
        let filtered_items = normalized_input_vals
            .into_iter()
            .zip(items_conditions)
            .filter(|(_, condition)| *condition)
            .map(|(item, _)| item)
            .collect::<Arc<_>>();
        Ok(Value::Coll(CollKind::from_collection(
            (*self.elem_tpe).clone(),
            filtered_items,
        )?))
    }
}

#[allow(clippy::unwrap_used)]
#[allow(clippy::panic)]
#[cfg(test)]
#[cfg(feature = "arbitrary")]
mod tests {

    use crate::eval::tests::eval_out;
    use ergotree_ir::chain::context::Context;

    use super::*;

    use ergotree_ir::chain::ergo_box::ErgoBox;
    use ergotree_ir::mir::bin_op::BinOp;
    use ergotree_ir::mir::bin_op::RelationOp;
    use ergotree_ir::mir::expr::Expr;
    use ergotree_ir::mir::extract_amount::ExtractAmount;
    use ergotree_ir::mir::func_value::FuncArg;
    use ergotree_ir::mir::func_value::FuncValue;
    use ergotree_ir::mir::property_call::PropertyCall;
    use ergotree_ir::mir::unary_op::OneArgOpTryBuild;
    use ergotree_ir::mir::val_use::ValUse;
    use ergotree_ir::reference::Ref;
    use ergotree_ir::types::scontext;
    use ergotree_ir::types::stype::SType;
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
            let body: Expr = BinOp {
                kind: RelationOp::Le.into(),
                left: Box::new(Expr::Const(1i64.into())),
                right: Box::new(Expr::ExtractAmount(
                        ExtractAmount::try_build(val_use)
                    .unwrap(),
                )),
            }
            .into();
            let expr: Expr = Filter::new(
                data_inputs,
                FuncValue::new(
                    vec![FuncArg {
                        idx: 1.into(),
                        tpe: SType::SBox,
                    }],
                    body,
                )
                .into(),
            )
            .unwrap()
            .into();
            let expected: Vec<_> = ctx
                .data_inputs
                .clone()
                .map_or(
                     vec![],
                     |d| d
                         .iter()
                         .cloned()
                         .filter(|b| 1 <= b.value.as_i64())
                         .collect()
                );


            eval_out::<Vec<Ref<'_, ErgoBox>>>(&expr, &ctx)
                .into_iter()
                .zip(expected)
                .for_each(|(left, right)| assert_eq!(&*left, right));
       }
    }
}
