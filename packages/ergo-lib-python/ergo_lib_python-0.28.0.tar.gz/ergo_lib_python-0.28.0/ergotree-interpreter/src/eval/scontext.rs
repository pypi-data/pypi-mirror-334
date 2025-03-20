use alloc::boxed::Box;
use alloc::string::ToString;
use alloc::sync::Arc;

use ergotree_ir::mir::avl_tree_data::AvlTreeData;
use ergotree_ir::mir::avl_tree_data::AvlTreeFlags;
use ergotree_ir::mir::value::CollKind;
use ergotree_ir::mir::value::Value;
use ergotree_ir::reference::Ref;
use ergotree_ir::serialization::SigmaSerializable;
use ergotree_ir::types::stype::SType;

use super::EvalError;
use super::EvalFn;

pub(crate) static DATA_INPUTS_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.dataInputs: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    Ok(Value::Coll(CollKind::WrappedColl {
        items: ctx.data_inputs.clone().map_or(Arc::new([]), |d| {
            d.iter().map(|&di| Ref::from(di)).map(Value::CBox).collect()
        }),
        elem_tpe: SType::SBox,
    }))
};

pub(crate) static SELF_BOX_INDEX_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.selfBoxIndex: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    let box_index = ctx
        .inputs
        .iter()
        .position(|it| *it == ctx.self_box)
        .ok_or_else(|| EvalError::NotFound("Context.selfBoxIndex: box not found".to_string()))?;
    Ok(Value::Int(box_index as i32))
};

pub(crate) static HEADERS_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.headers: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    Ok(Value::Coll(CollKind::WrappedColl {
        items: Arc::new(ctx.headers.clone().map(Box::new).map(Value::Header)),
        elem_tpe: SType::SHeader,
    }))
};

pub(crate) static PRE_HEADER_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.preHeader: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    Ok(Box::from(ctx.pre_header.clone()).into())
};

pub(crate) static LAST_BLOCK_UTXO_ROOT_HASH_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.LastBlockUtxoRootHash: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    let digest = ctx.headers[0].state_root;
    let tree_flags = AvlTreeFlags::new(true, true, true);
    Ok(Value::AvlTree(Box::from(AvlTreeData {
        digest,
        tree_flags,
        key_length: 32,
        value_length_opt: None,
    })))
};

pub(crate) static MINER_PUBKEY_EVAL_FN: EvalFn = |_mc, _env, ctx, obj, _args| {
    if obj != Value::Context {
        return Err(EvalError::UnexpectedValue(format!(
            "Context.preHeader: expected object of Value::Context, got {:?}",
            obj
        )));
    }
    Ok(ctx
        .pre_header
        .miner_pk
        .clone()
        .sigma_serialize_bytes()?
        .into())
};

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use crate::eval::tests::eval_out;
    use ergo_chain_types::{Header, PreHeader};
    use ergotree_ir::chain::context::Context;
    use ergotree_ir::chain::ergo_box::ErgoBox;
    use ergotree_ir::mir::avl_tree_data::{AvlTreeData, AvlTreeFlags};
    use ergotree_ir::mir::expr::Expr;
    use ergotree_ir::mir::property_call::PropertyCall;
    use ergotree_ir::serialization::SigmaSerializable;
    use ergotree_ir::types::scontext;
    use sigma_test_util::force_any_val;

    fn make_ctx_inputs_includes_self_box() -> Context<'static> {
        let ctx = force_any_val::<Context>();
        let self_box = &*Box::leak(Box::new(force_any_val::<ErgoBox>()));
        let inputs = vec![&*Box::leak(Box::new(force_any_val::<ErgoBox>())), self_box]
            .try_into()
            .unwrap();
        Context {
            height: 0u32,
            self_box,
            inputs,
            ..ctx
        }
    }

    #[test]
    fn eval_self_box_index() {
        let expr: Expr =
            PropertyCall::new(Expr::Context, scontext::SELF_BOX_INDEX_PROPERTY.clone())
                .unwrap()
                .into();
        let context = make_ctx_inputs_includes_self_box();
        assert_eq!(eval_out::<i32>(&expr, &context), 1);
    }

    #[test]
    fn eval_headers() {
        let expr: Expr = PropertyCall::new(Expr::Context, scontext::HEADERS_PROPERTY.clone())
            .expect("internal error: `headers` method has parameters length != 1")
            .into();
        let ctx = force_any_val::<Context>();
        assert_eq!(eval_out::<[Header; 10]>(&expr, &ctx), ctx.headers);
    }

    #[test]
    fn eval_preheader() {
        let expr: Expr = PropertyCall::new(Expr::Context, scontext::PRE_HEADER_PROPERTY.clone())
            .unwrap()
            .into();
        let ctx = force_any_val::<Context>();
        assert_eq!(eval_out::<PreHeader>(&expr, &ctx), ctx.pre_header);
    }

    #[test]
    fn eval_miner_pubkey() {
        let expr: Expr = PropertyCall::new(Expr::Context, scontext::MINER_PUBKEY_PROPERTY.clone())
            .unwrap()
            .into();
        let ctx = force_any_val::<Context>();
        assert_eq!(
            eval_out::<Vec<u8>>(&expr, &ctx),
            ctx.pre_header.miner_pk.sigma_serialize_bytes().unwrap()
        );
    }

    #[test]
    fn eval_last_block_utxo_root_hash() {
        let expr: Expr = PropertyCall::new(
            Expr::Context,
            scontext::LAST_BLOCK_UTXO_ROOT_HASH_PROPERTY.clone(),
        )
        .unwrap()
        .into();
        let ctx = force_any_val::<Context>();
        let digest = ctx.headers[0].state_root;
        let tree_flags = AvlTreeFlags::new(true, true, true);
        let avl_tree_data = AvlTreeData {
            digest,
            tree_flags,
            key_length: 32,
            value_length_opt: None,
        };
        assert_eq!(eval_out::<AvlTreeData>(&expr, &ctx), avl_tree_data);
    }
}
