//! Evaluating predefined `Header` (or SHeader) type properties

use alloc::sync::Arc;
use core::convert::TryInto;

use alloc::vec::Vec;
use ergo_chain_types::Header;
use ergotree_ir::{bigint256::BigInt256, mir::constant::TryExtractInto};

use super::{EvalError, EvalFn};

pub(crate) static VERSION_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok((header.version as i8).into())
};

pub(crate) static ID_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.id).into())
};

pub(crate) static PARENT_ID_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.parent_id).into())
};

pub(crate) static AD_PROOFS_ROOT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.ad_proofs_root).into())
};

pub(crate) static STATE_ROOT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.state_root).into())
};

pub(crate) static TRANSACTION_ROOT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.transaction_root).into())
};

pub(crate) static EXTENSION_ROOT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<i8>>::into(header.extension_root).into())
};

pub(crate) static TIMESTAMP_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok((header.timestamp as i64).into())
};

pub(crate) static N_BITS_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok((header.n_bits as i64).into())
};

pub(crate) static HEIGHT_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok((header.height as i32).into())
};

pub(crate) static MINER_PK_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Arc::new(*header.autolykos_solution.miner_pk).into())
};

pub(crate) static POW_ONETIME_PK_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok((*header.autolykos_solution.pow_onetime_pk.unwrap_or_default()).into())
};

pub(crate) static POW_NONCE_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(header.autolykos_solution.nonce.into())
};

pub(crate) static POW_DISTANCE_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    let pow_distance: BigInt256 = header
        .autolykos_solution
        .pow_distance
        .unwrap_or_default()
        .try_into()
        .map_err(EvalError::Misc)?;
    Ok(pow_distance.into())
};

pub(crate) static VOTES_EVAL_FN: EvalFn = |_mc, _env, _ctx, obj, _args| {
    let header = obj.try_extract_into::<Header>()?;
    Ok(Into::<Vec<u8>>::into(header.votes).into())
};

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::expect_used, clippy::panic, clippy::unwrap_used)]
mod tests {
    use core::convert::{TryFrom, TryInto};

    use alloc::{boxed::Box, vec::Vec};
    use ergo_chain_types::{BlockId, Digest, Digest32, EcPoint, Votes};
    use ergotree_ir::{
        bigint256::BigInt256,
        chain::context::Context,
        mir::{coll_by_index::ByIndex, expr::Expr, property_call::PropertyCall},
        types::{scontext, sheader, smethod::SMethod},
    };
    use sigma_test_util::force_any_val;
    use sigma_util::AsVecU8;

    use crate::eval::tests::{eval_out, try_eval_out_wo_ctx};

    // Index in Context.headers array
    const HEADER_INDEX: usize = 0;

    // Evaluates `Header.minerPk`, `Header.powOnetimePk`
    fn eval_header_pks(ctx: &Context<'static>) -> [Box<EcPoint>; 2] {
        let miner_pk = eval_out::<EcPoint>(
            &create_get_header_property_expr(sheader::MINER_PK_PROPERTY.clone()),
            ctx,
        );
        let pow_onetime_pk = eval_out::<EcPoint>(
            &create_get_header_property_expr(sheader::POW_ONETIME_PK_PROPERTY.clone()),
            ctx,
        );
        [miner_pk, pow_onetime_pk].map(Box::new)
    }

    // Evaluates `Header.AdProofsRoot`, `Header.transactionRoot`, `Header.extensionRoot`
    fn eval_header_roots(ctx: &Context<'static>) -> [Digest32; 3] {
        vec![
            sheader::AD_PROOFS_ROOT_PROPERTY.clone(),
            sheader::TRANSACTIONS_ROOT_PROPERTY.clone(),
            sheader::EXTENSION_ROOT_PROPERTY.clone(),
        ]
        .into_iter()
        .map(|smethod| eval_out::<Vec<i8>>(&create_get_header_property_expr(smethod), ctx))
        .map(digest_from_bytes_signed::<32>)
        .collect::<Vec<_>>()
        .try_into()
        .expect("internal error: smethods vector length is not equal to 3")
    }

    // Evaluates `Header.id` and `Header.parentId`
    fn eval_header_ids(ctx: &Context<'static>) -> [BlockId; 2] {
        let id = eval_out::<Vec<i8>>(
            &create_get_header_property_expr(sheader::ID_PROPERTY.clone()),
            ctx,
        );
        let parent_id = eval_out::<Vec<i8>>(
            &create_get_header_property_expr(sheader::PARENT_ID_PROPERTY.clone()),
            ctx,
        );
        [id, parent_id].map(block_id_from_bytes_signed)
    }

    fn create_get_header_property_expr(method: SMethod) -> Expr {
        let get_headers_expr = create_get_header_by_index_expr();
        create_header_property_call_expr(get_headers_expr, method)
    }

    // An `Expr` for such code in ErgoScript `CONTEXT.headers(0)`
    fn create_get_header_by_index_expr() -> Expr {
        let prop_call = PropertyCall::new(Expr::Context, scontext::HEADERS_PROPERTY.clone())
            .expect("internal error: invalid headers property call of Context")
            .into();
        ByIndex::new(prop_call, Expr::Const((HEADER_INDEX as i32).into()), None)
            .expect("internal error: invalid types of ByIndex expression")
            .into()
    }

    fn create_header_property_call_expr(headers_expr: Expr, method: SMethod) -> Expr {
        PropertyCall::new(headers_expr, method)
            .expect("internal error: invalid header property call")
            .into()
    }

    fn block_id_from_bytes_signed(bytes: Vec<i8>) -> BlockId {
        let arr32 = digest_from_bytes_signed::<32>(bytes);
        BlockId(arr32)
    }

    fn digest_from_bytes_signed<const N: usize>(bytes: Vec<i8>) -> Digest<N> {
        let arr = arr_from_bytes_signed::<N>(bytes);
        arr.into()
    }

    fn arr_from_bytes_signed<const N: usize>(bytes: Vec<i8>) -> [u8; N] {
        bytes
            .as_vec_u8()
            .try_into()
            .unwrap_or_else(|_| panic!("internal error: bytes buffer length is not equal to {}", N))
    }

    #[test]
    fn test_eval_version() {
        let expr = create_get_header_property_expr(sheader::VERSION_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let version = ctx.headers[HEADER_INDEX].version as i8;
        assert_eq!(version, eval_out::<i8>(&expr, &ctx));
    }

    #[test]
    fn test_eval_ids() {
        let ctx = force_any_val::<Context>();
        let expected = ctx
            .headers
            .get(HEADER_INDEX)
            .map(|h| [h.id, h.parent_id])
            .expect("internal error: empty headers array");
        let actual = eval_header_ids(&ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_roots() {
        let ctx = force_any_val::<Context>();
        let expected = ctx
            .headers
            .get(HEADER_INDEX)
            .map(|h| [h.ad_proofs_root, h.transaction_root, h.extension_root])
            .expect("internal error: empty headers array");
        let actual = eval_header_roots(&ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_state_root() {
        let expr = create_get_header_property_expr(sheader::STATE_ROOT_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].state_root;
        let actual = digest_from_bytes_signed::<33>(eval_out::<Vec<i8>>(&expr, &ctx));
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_timestamp() {
        let expr = create_get_header_property_expr(sheader::TIMESTAMP_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].timestamp as i64;
        let actual = eval_out::<i64>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_n_bits() {
        let expr = create_get_header_property_expr(sheader::N_BITS_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].n_bits as i64;
        let actual = eval_out::<i64>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_height() {
        let expr = create_get_header_property_expr(sheader::HEIGHT_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].height as i32;
        let actual = eval_out::<i32>(&expr, &ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_pks() {
        let ctx = force_any_val::<Context>();
        let expected = ctx
            .headers
            .get(HEADER_INDEX)
            .map(|h| {
                [
                    h.autolykos_solution.miner_pk.clone(),
                    h.autolykos_solution
                        .pow_onetime_pk
                        .clone()
                        .unwrap_or_default(),
                ]
            })
            .expect("internal error: empty headers array");
        let actual = eval_header_pks(&ctx);
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_pow_distance() {
        let expr = create_get_header_property_expr(sheader::POW_DISTANCE_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX]
            .autolykos_solution
            .pow_distance
            .clone()
            .unwrap_or_default();
        let actual = {
            let bi = eval_out::<BigInt256>(&expr, &ctx);
            bi.into()
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_pow_nonce() {
        let expr = create_get_header_property_expr(sheader::POW_NONCE_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].autolykos_solution.nonce.clone();
        let actual = eval_out::<Vec<i8>>(&expr, &ctx).as_vec_u8();
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_votes() {
        let expr = create_get_header_property_expr(sheader::VOTES_PROPERTY.clone());
        let ctx = force_any_val::<Context>();
        let expected = ctx.headers[HEADER_INDEX].votes.clone();
        let actual = {
            let votes_bytes = eval_out::<Vec<i8>>(&expr, &ctx).as_vec_u8();
            Votes::try_from(votes_bytes)
                .expect("internal error: votes bytes buffer length isn't equal to 3")
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_eval_failed_invalid_obj() {
        // calling for Header property on Context obj
        let expr: Expr = PropertyCall {
            obj: Box::new(Expr::Context),
            method: sheader::VERSION_PROPERTY.clone(),
        }
        .into();
        assert!(try_eval_out_wo_ctx::<i8>(&expr).is_err());
    }

    #[test]
    fn test_eval_failed_unknown_property() {
        let unknown_property = {
            use ergotree_ir::types::{
                smethod::{MethodId, SMethod, SMethodDesc},
                stype::SType,
                stype_companion::STypeCompanion,
            };
            let method_desc =
                SMethodDesc::property(SType::SHeader, "unknown", SType::SByte, MethodId(100));
            SMethod::new(STypeCompanion::Header, method_desc)
        };
        let expr = create_get_header_property_expr(unknown_property);
        assert!(try_eval_out_wo_ctx::<i8>(&expr).is_err());
    }
}
