use alloc::{sync::Arc, vec::Vec};

use ergo_chain_types::PreHeader;
use ergotree_ir::mir::constant::TryExtractInto;

use super::EvalFn;

pub(crate) static VERSION_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok((preheader.version as i8).into())
};

pub(crate) static PARENT_ID_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok(Into::<Vec<i8>>::into(preheader.parent_id).into())
};

pub(crate) static TIMESTAMP_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok((preheader.timestamp as i64).into())
};

pub(crate) static N_BITS_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok((preheader.n_bits as i64).into())
};

pub(crate) static HEIGHT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok((preheader.height as i32).into())
};

pub(crate) static MINER_PK_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok(Arc::new(*preheader.miner_pk).into())
};

pub(crate) static VOTES_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let preheader = obj.try_extract_into::<PreHeader>()?;
    Ok(Into::<Vec<u8>>::into(preheader.votes).into())
};

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::expect_used)]
mod tests {
    use core::convert::{TryFrom, TryInto};

    use ergo_chain_types::{BlockId, EcPoint, Votes};
    use ergotree_ir::{
        mir::{expr::Expr, property_call::PropertyCall},
        types::{scontext, smethod::SMethod, spreheader},
    };
    use sigma_test_util::force_any_val;
    use sigma_util::AsVecU8;

    use crate::eval::tests::{eval_out, try_eval_out_wo_ctx};
    use ergotree_ir::chain::context::Context;

    fn create_get_preheader_property_expr(method: SMethod) -> Expr {
        let get_preheader_expr = create_get_preheader_expr();
        create_get_preheader_property_expr_impl(get_preheader_expr, method)
    }

    // An `Expr` for such code in ErgoScript: `CONTEXT.preHeader`
    fn create_get_preheader_expr() -> Expr {
        PropertyCall::new(Expr::Context, scontext::PRE_HEADER_PROPERTY.clone())
            .expect("internal error: invalid preheader property call of Context")
            .into()
    }

    fn create_get_preheader_property_expr_impl(headers_expr: Expr, method: SMethod) -> Expr {
        PropertyCall::new(headers_expr, method)
            .expect("internal error: invalid property call of PreHeader")
            .into()
    }

    fn block_id_from_bytes_signed(bytes: Vec<i8>) -> BlockId {
        let arr32 = bytes
            .as_vec_u8()
            .try_into()
            .expect("internal error: bytes buffer length is not equal to 32");
        BlockId(arr32)
    }

    #[test]
    fn test_eval_version() {
        let expr = create_get_preheader_property_expr(spreheader::VERSION_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.version as i8;
        assert_eq!(expected, eval_out::<i8>(&expr, &ctx));
    }

    #[test]
    fn test_eval_parent_id() {
        let expr = create_get_preheader_property_expr(spreheader::PARENT_ID_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.parent_id;
        let actual = {
            let bs = eval_out::<Vec<i8>>(&expr, &ctx);
            block_id_from_bytes_signed(bs)
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_timestamp() {
        let expr = create_get_preheader_property_expr(spreheader::TIMESTAMP_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.timestamp as i64;
        let actual = eval_out::<i64>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_n_bits() {
        let expr = create_get_preheader_property_expr(spreheader::N_BITS_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.n_bits as i64;
        let actual = eval_out::<i64>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_height() {
        let expr = create_get_preheader_property_expr(spreheader::HEIGHT_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.height as i32;
        let actual = eval_out::<i32>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_miner_pk() {
        let expr = create_get_preheader_property_expr(spreheader::MINER_PK_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.miner_pk.clone();
        let actual = {
            let pk = eval_out::<EcPoint>(&expr, &ctx);
            Box::new(pk)
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_votes() {
        let expr = create_get_preheader_property_expr(spreheader::VOTES_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.pre_header.votes.clone();
        let actual = {
            let votes_bytes = eval_out::<Vec<i8>>(&expr, &ctx).as_vec_u8();
            Votes::try_from(votes_bytes)
                .expect("internal error: votes bytes buffer length isn't equal to 3")
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_failed_invalid_obj() {
        // calling for PreHeader property on Context obj
        let expr: Expr = PropertyCall {
            obj: Box::new(Expr::Context),
            method: spreheader::VERSION_PROPERTY.clone(),
        }
        .into();
        assert!(try_eval_out_wo_ctx::<i8>(&expr).is_err());
    }

    #[test]
    fn test_eval_failed_unknown_property() {
        let unknown_property = {
            use ergotree_ir::types::{
                smethod::{MethodId, SMethodDesc},
                stype::SType,
                stype_companion::STypeCompanion,
            };
            let method_desc =
                SMethodDesc::property(SType::SPreHeader, "unknown", SType::SByte, MethodId(100));
            SMethod::new(STypeCompanion::PreHeader, method_desc)
        };
        let expr = create_get_preheader_property_expr(unknown_property);
        assert!(try_eval_out_wo_ctx::<i8>(&expr).is_err());
    }
}
