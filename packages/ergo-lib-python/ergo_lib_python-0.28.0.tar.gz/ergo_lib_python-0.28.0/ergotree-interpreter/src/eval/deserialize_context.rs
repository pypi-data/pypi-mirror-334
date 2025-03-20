#[allow(clippy::unwrap_used)]
#[cfg(test)]
mod tests {
    use ergotree_ir::ergo_tree::{ErgoTree, ErgoTreeHeader};
    use ergotree_ir::mir::constant::Constant;
    use ergotree_ir::mir::deserialize_context::DeserializeContext;
    use ergotree_ir::mir::expr::Expr;
    use ergotree_ir::mir::global_vars::GlobalVars;
    use ergotree_ir::mir::value::Value;
    use ergotree_ir::serialization::SigmaSerializable;
    use ergotree_ir::types::stype::SType;
    use sigma_test_util::force_any_val;

    use crate::eval::reduce_to_crypto;
    use crate::eval::tests::try_eval_with_deserialize;
    use ergotree_ir::chain::context::Context;
    use ergotree_ir::chain::context_extension::ContextExtension;

    #[test]
    fn eval() {
        let expr: Expr = Expr::from(DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        });
        let inner_expr: Expr = true.into();
        let ctx_ext = ContextExtension {
            values: [(1u8, inner_expr.sigma_serialize_bytes().unwrap().into())]
                .iter()
                .cloned()
                .collect(),
        };
        let ctx = force_any_val::<Context>().with_extension(ctx_ext);
        assert!(try_eval_with_deserialize::<bool>(&expr, &ctx).unwrap());
    }

    // Verify that reduce_to_crypto performs deserialize substitution
    #[test]
    fn eval_reduction() {
        let expr: Expr = Expr::from(DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        });
        let inner_expr: Expr = true.into();
        let ctx_ext = ContextExtension {
            values: [(1u8, inner_expr.sigma_serialize_bytes().unwrap().into())]
                .iter()
                .cloned()
                .collect(),
        };
        let ctx = force_any_val::<Context>().with_extension(ctx_ext);
        assert_eq!(
            reduce_to_crypto(
                &ErgoTree::new(ErgoTreeHeader::v1(false), &expr).unwrap(),
                &ctx,
            )
            .unwrap()
            .sigma_prop,
            true.into()
        );
    }

    #[test]
    fn eval_id_not_found() {
        let expr: Expr = DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        }
        .into();
        let ctx = force_any_val::<Context>().with_extension(ContextExtension::empty());
        assert!(try_eval_with_deserialize::<bool>(&expr, &ctx).is_err());
    }

    #[test]
    fn eval_context_extension_wrong_type() {
        let expr: Expr = DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        }
        .into();
        // should be byte array
        let ctx_ext_val: Constant = 1i32.into();
        let ctx_ext = ContextExtension {
            values: [(1u8, ctx_ext_val)].iter().cloned().collect(),
        };
        let ctx = force_any_val::<Context>().with_extension(ctx_ext);
        assert!(try_eval_with_deserialize::<bool>(&expr, &ctx).is_err());
    }

    #[test]
    fn evaluated_expr_wrong_type() {
        let expr: Expr = DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        }
        .into();
        // should be SBoolean
        let inner_expr: Expr = GlobalVars::Height.into();
        let ctx_ext = ContextExtension {
            values: [(1u8, inner_expr.sigma_serialize_bytes().unwrap().into())]
                .iter()
                .cloned()
                .collect(),
        };
        let ctx = force_any_val::<Context>().with_extension(ctx_ext);
        assert!(try_eval_with_deserialize::<Value>(&expr, &ctx).is_err());
    }

    #[test]
    fn eval_recursive() {
        let expr: Expr = DeserializeContext {
            tpe: SType::SBoolean,
            id: 1,
        }
        .into();
        let ctx_ext = ContextExtension {
            values: [(1u8, expr.sigma_serialize_bytes().unwrap().into())]
                .iter()
                .cloned()
                .collect(),
        };
        let ctx = force_any_val::<Context>().with_extension(ctx_ext);
        // Evaluating executeFromVar(1) with ctx[1] being executeFromVar(1) should fail during evaluation
        assert!(try_eval_with_deserialize::<bool>(&expr, &ctx).is_err());
    }
}
