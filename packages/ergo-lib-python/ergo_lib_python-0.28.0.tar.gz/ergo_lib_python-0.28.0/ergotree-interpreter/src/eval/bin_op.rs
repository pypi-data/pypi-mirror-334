//! Operators in ErgoTree

use ergotree_ir::bigint256::BigInt256;
use ergotree_ir::mir::bin_op::BinOpKind;
use ergotree_ir::mir::bin_op::RelationOp;
use ergotree_ir::mir::bin_op::{ArithOp, LogicalOp};
use ergotree_ir::mir::bin_op::{BinOp, BitOp};
use ergotree_ir::mir::constant::TryExtractFrom;
use ergotree_ir::mir::constant::TryExtractInto;
use ergotree_ir::mir::value::Value;
use num_traits::CheckedAdd;
use num_traits::CheckedDiv;
use num_traits::CheckedMul;
use num_traits::CheckedRem;
use num_traits::CheckedSub;
use num_traits::Num;

use crate::eval::env::Env;
use crate::eval::Context;
use crate::eval::EvalError;
use crate::eval::Evaluable;

fn arithmetic_err<T: core::fmt::Display>(
    op: &str,
    lv_raw: T,
    rv_raw: T,
    err_str: &str,
) -> EvalError {
    EvalError::ArithmeticException(format!(
        "({0}) {1} ({2}) resulted in {3}",
        lv_raw, op, rv_raw, err_str
    ))
}

fn eval_plus<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + CheckedAdd + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    lv_raw
        .checked_add(&rv_raw)
        .ok_or_else(|| arithmetic_err("+", lv_raw, rv_raw, "overflow"))
        .map(|t| t.into()) // convert T to Value
}

fn eval_minus<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + CheckedSub + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    lv_raw
        .checked_sub(&rv_raw)
        .ok_or_else(|| arithmetic_err("-", lv_raw, rv_raw, "overflow"))
        .map(|t| t.into()) // convert T to Value
}

fn eval_mul<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + CheckedMul + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    lv_raw
        .checked_mul(&rv_raw)
        .ok_or_else(|| arithmetic_err("*", lv_raw, rv_raw, "overflow"))
        .map(|t| t.into()) // convert T to Value
}

fn eval_div<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + CheckedDiv + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    lv_raw
        .checked_div(&rv_raw)
        .ok_or_else(|| arithmetic_err("/", lv_raw, rv_raw, "exception"))
        .map(|t| t.into()) // convert T to Value
}

fn eval_mod<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + CheckedRem + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    lv_raw
        .checked_rem(&rv_raw)
        .ok_or_else(|| arithmetic_err("%", lv_raw, rv_raw, "exception"))
        .map(|t| t.into()) // convert T to Value
}

fn eval_bit_op<'ctx, T, F>(lv_raw: T, rv: Value<'ctx>, op: F) -> Result<Value<'ctx>, EvalError>
where
    T: Num + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>> + core::fmt::Display,
    F: FnOnce(T, T) -> T,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    Ok(op(lv_raw, rv_raw).into())
}

fn eval_ge<'ctx>(lv: Value<'ctx>, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError> {
    match lv {
        Value::Byte(lv_raw) => Ok((lv_raw >= rv.try_extract_into::<i8>()?).into()),
        Value::Short(lv_raw) => Ok((lv_raw >= rv.try_extract_into::<i16>()?).into()),
        Value::Int(lv_raw) => Ok((lv_raw >= rv.try_extract_into::<i32>()?).into()),
        Value::Long(lv_raw) => Ok((lv_raw >= rv.try_extract_into::<i64>()?).into()),
        Value::BigInt(lv_raw) => Ok((lv_raw >= rv.try_extract_into::<BigInt256>()?).into()),
        _ => Err(EvalError::UnexpectedValue(format!(
            "expected BinOp::left to be numeric value, got {0:?}",
            lv
        ))),
    }
}

fn eval_gt<'ctx>(lv: Value<'ctx>, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError> {
    match lv {
        Value::Byte(lv_raw) => Ok((lv_raw > rv.try_extract_into::<i8>()?).into()),
        Value::Short(lv_raw) => Ok((lv_raw > rv.try_extract_into::<i16>()?).into()),
        Value::Int(lv_raw) => Ok((lv_raw > rv.try_extract_into::<i32>()?).into()),
        Value::Long(lv_raw) => Ok((lv_raw > rv.try_extract_into::<i64>()?).into()),
        Value::BigInt(lv_raw) => Ok((lv_raw > rv.try_extract_into::<BigInt256>()?).into()),
        _ => Err(EvalError::UnexpectedValue(format!(
            "expected BinOp::left to be numeric value, got {0:?}",
            lv
        ))),
    }
}

fn eval_lt<'ctx>(lv: Value<'ctx>, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError> {
    match lv {
        Value::Byte(lv_raw) => Ok((lv_raw < rv.try_extract_into::<i8>()?).into()),
        Value::Short(lv_raw) => Ok((lv_raw < rv.try_extract_into::<i16>()?).into()),
        Value::Int(lv_raw) => Ok((lv_raw < rv.try_extract_into::<i32>()?).into()),
        Value::Long(lv_raw) => Ok((lv_raw < rv.try_extract_into::<i64>()?).into()),
        Value::BigInt(lv_raw) => Ok((lv_raw < rv.try_extract_into::<BigInt256>()?).into()),
        _ => Err(EvalError::UnexpectedValue(format!(
            "expected BinOp::left to be numeric value, got {0:?}",
            lv
        ))),
    }
}

fn eval_le<'ctx>(lv: Value<'ctx>, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError> {
    match lv {
        Value::Byte(lv_raw) => Ok((lv_raw <= rv.try_extract_into::<i8>()?).into()),
        Value::Short(lv_raw) => Ok((lv_raw <= rv.try_extract_into::<i16>()?).into()),
        Value::Int(lv_raw) => Ok((lv_raw <= rv.try_extract_into::<i32>()?).into()),
        Value::Long(lv_raw) => Ok((lv_raw <= rv.try_extract_into::<i64>()?).into()),
        Value::BigInt(lv_raw) => Ok((lv_raw <= rv.try_extract_into::<BigInt256>()?).into()),
        _ => Err(EvalError::UnexpectedValue(format!(
            "expected BinOp::left to be numeric value, got {0:?}",
            lv
        ))),
    }
}

fn eval_max<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + Ord + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>>,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    Ok((lv_raw.max(rv_raw)).into())
}

fn eval_min<'ctx, T>(lv_raw: T, rv: Value<'ctx>) -> Result<Value<'ctx>, EvalError>
where
    T: Num + Ord + TryExtractFrom<Value<'ctx>> + Into<Value<'ctx>>,
{
    let rv_raw = rv.try_extract_into::<T>()?;
    Ok((lv_raw.min(rv_raw)).into())
}

impl Evaluable for BinOp {
    fn eval<'ctx>(
        &self,
        env: &mut Env<'ctx>,
        ctx: &Context<'ctx>,
    ) -> Result<Value<'ctx>, EvalError> {
        //ctx.cost_accum.add(Costs::DEFAULT.eq_const_size)?;
        let lv = self.left.eval(env, ctx)?;
        // using closure to keep right value from evaluation (for lazy AND, OR, XOR)
        let mut rv = || self.right.eval(env, ctx);
        match self.kind {
            BinOpKind::Logical(op) => match op {
                LogicalOp::And => Ok(Value::Boolean(if lv.try_extract_into::<bool>()? {
                    rv()?.try_extract_into::<bool>()?
                } else {
                    false
                })),
                LogicalOp::Or => Ok(Value::Boolean(if !lv.try_extract_into::<bool>()? {
                    rv()?.try_extract_into::<bool>()?
                } else {
                    true
                })),
                LogicalOp::Xor => Ok(Value::Boolean(
                    lv.try_extract_into::<bool>()? ^ rv()?.try_extract_into::<bool>()?,
                )),
            },
            BinOpKind::Relation(op) => match op {
                RelationOp::Eq => Ok(Value::Boolean(lv == rv()?)),
                RelationOp::NEq => Ok(Value::Boolean(lv != rv()?)),
                RelationOp::Gt => eval_gt(lv, rv()?),
                RelationOp::Lt => eval_lt(lv, rv()?),
                RelationOp::Ge => eval_ge(lv, rv()?),
                RelationOp::Le => eval_le(lv, rv()?),
            },
            BinOpKind::Arith(op) => match op {
                ArithOp::Plus => match lv {
                    Value::Byte(lv_raw) => eval_plus(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_plus(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_plus(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_plus(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_plus(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Minus => match lv {
                    Value::Byte(lv_raw) => eval_minus(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_minus(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_minus(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_minus(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_minus(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Multiply => match lv {
                    Value::Byte(lv_raw) => eval_mul(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_mul(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_mul(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_mul(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_mul(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Divide => match lv {
                    Value::Byte(lv_raw) => eval_div(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_div(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_div(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_div(lv_raw, rv()?),
                    // MIN / -1  can actually overflow
                    Value::BigInt(lv_raw) => eval_div(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Max => match lv {
                    Value::Byte(lv_raw) => eval_max(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_max(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_max(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_max(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_max(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Min => match lv {
                    Value::Byte(lv_raw) => eval_min(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_min(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_min(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_min(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_min(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                ArithOp::Modulo => match lv {
                    Value::Byte(lv_raw) => eval_mod(lv_raw, rv()?),
                    Value::Short(lv_raw) => eval_mod(lv_raw, rv()?),
                    Value::Int(lv_raw) => eval_mod(lv_raw, rv()?),
                    Value::Long(lv_raw) => eval_mod(lv_raw, rv()?),
                    Value::BigInt(lv_raw) => eval_mod(lv_raw, rv()?),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
            },
            BinOpKind::Bit(op) => match op {
                BitOp::BitAnd => match lv {
                    Value::Byte(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l & r),
                    Value::Short(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l & r),
                    Value::Int(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l & r),
                    Value::Long(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l & r),
                    Value::BigInt(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l & r),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                BitOp::BitOr => match lv {
                    Value::Byte(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l | r),
                    Value::Short(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l | r),
                    Value::Int(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l | r),
                    Value::Long(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l | r),
                    Value::BigInt(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l | r),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
                BitOp::BitXor => match lv {
                    Value::Byte(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l ^ r),
                    Value::Short(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l ^ r),
                    Value::Int(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l ^ r),
                    Value::Long(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l ^ r),
                    Value::BigInt(lv_raw) => eval_bit_op(lv_raw, rv()?, |l, r| l ^ r),
                    _ => Err(EvalError::UnexpectedValue(format!(
                        "expected BinOp::left to be numeric value, got {0:?}",
                        lv
                    ))),
                },
            },
        }
    }
}

#[allow(clippy::panic)]
#[cfg(test)]
#[allow(clippy::unwrap_used)]
mod tests {
    use super::*;
    use crate::eval::tests::eval_out_wo_ctx;
    use crate::eval::tests::try_eval_out_wo_ctx;
    use alloc::boxed::Box;
    use ergotree_ir::mir::constant::Constant;
    use ergotree_ir::mir::expr::Expr;
    use num_traits::Bounded;
    use proptest::prelude::*;

    fn check_eq_neq(left: Constant, right: Constant) -> bool {
        let eq_op: Expr = BinOp {
            kind: BinOpKind::Relation(RelationOp::Eq),
            left: Box::new(left.clone().into()),
            right: Box::new(right.clone().into()),
        }
        .into();
        let neq_op: Expr = BinOp {
            kind: BinOpKind::Relation(RelationOp::NEq),
            left: Box::new(left.into()),
            right: Box::new(right.into()),
        }
        .into();
        eval_out_wo_ctx::<bool>(&eq_op) && !eval_out_wo_ctx::<bool>(&neq_op)
    }

    #[test]
    fn num_eq() {
        assert!(check_eq_neq(1i64.into(), 1i64.into()));
    }

    #[test]
    fn num_neq() {
        assert!(!check_eq_neq(2i64.into(), 1i64.into()));
    }

    #[test]
    fn option_eq() {
        assert!(check_eq_neq(Some(1i64).into(), Some(1i64).into()));
        let none: Option<i64> = None;
        assert!(check_eq_neq(none.into(), none.into()));
        // Option<Vec<i8>>
        assert!(check_eq_neq(
            Some(vec![1i8, 2i8]).into(),
            Some(vec![1i8, 2i8]).into()
        ));
        // Vec<Option<i64>>
        assert!(check_eq_neq(
            vec![Some(1i64), Some(1i64)].into(),
            vec![Some(1i64), Some(1i64)].into()
        ));
    }

    #[test]
    fn option_neq() {
        assert!(!check_eq_neq(Some(2i64).into(), Some(1i64).into()));
        let none: Option<i64> = None;
        assert!(!check_eq_neq(none.into(), Some(1i64).into()));
        // Option<Vec<i8>>
        assert!(!check_eq_neq(
            Some(vec![1i8, 2i8]).into(),
            Some(vec![2i8, 2i8]).into()
        ));
        // Vec<Option<i64>>
        assert!(!check_eq_neq(
            vec![Some(1i64), Some(1i64)].into(),
            vec![Some(2i64), Some(1i64)].into()
        ));
    }

    #[test]
    fn tuple_eq() {
        assert!(check_eq_neq((1i64, true).into(), (1i64, true).into()));
    }

    #[test]
    fn bin_or_eval_laziness() {
        let e: Expr = BinOp {
            kind: BinOpKind::Logical(LogicalOp::Or),
            left: Box::new(Expr::Const(true.into())),
            // something that should blow-up the evaluation
            right: Box::new(
                BinOp {
                    kind: ArithOp::Divide.into(),
                    left: Box::new(Expr::Const(1i32.into())),
                    right: Box::new(Expr::Const(0i32.into())),
                }
                .into(),
            ),
        }
        .into();
        assert!(eval_out_wo_ctx::<bool>(&e));
    }

    #[test]
    fn bin_and_eval_laziness() {
        let e: Expr = BinOp {
            kind: BinOpKind::Logical(LogicalOp::And),
            left: Box::new(Expr::Const(false.into())),
            // something that should blow-up the evaluation
            right: Box::new(
                BinOp {
                    kind: ArithOp::Divide.into(),
                    left: Box::new(Expr::Const(1i32.into())),
                    right: Box::new(Expr::Const(0i32.into())),
                }
                .into(),
            ),
        }
        .into();
        assert!(!eval_out_wo_ctx::<bool>(&e));
    }

    fn eval_arith_op<T: TryExtractFrom<Value<'static>> + Into<Constant> + 'static>(
        op: ArithOp,
        left: T,
        right: T,
    ) -> Result<T, EvalError> {
        let expr: Expr = BinOp {
            kind: BinOpKind::Arith(op),
            left: Box::new(left.into().into()),
            right: Box::new(right.into().into()),
        }
        .into();
        try_eval_out_wo_ctx::<T>(&expr)
    }

    fn eval_bit_op<T: TryExtractFrom<Value<'static>> + Into<Constant> + 'static>(
        op: BitOp,
        left: T,
        right: T,
    ) -> Result<T, EvalError> {
        let expr: Expr = BinOp {
            kind: BinOpKind::Bit(op),
            left: Box::new(left.into().into()),
            right: Box::new(right.into().into()),
        }
        .into();
        try_eval_out_wo_ctx::<T>(&expr)
    }

    fn eval_relation_op<T: Into<Constant>>(op: RelationOp, left: T, right: T) -> bool {
        let expr: Expr = BinOp {
            kind: BinOpKind::Relation(op),
            left: Box::new(left.into().into()),
            right: Box::new(right.into().into()),
        }
        .into();
        eval_out_wo_ctx::<bool>(&expr)
    }

    fn eval_logical_op<T: Into<Constant>>(op: LogicalOp, left: T, right: T) -> bool {
        let expr: Expr = BinOp {
            kind: BinOpKind::Logical(op),
            left: Box::new(left.into().into()),
            right: Box::new(right.into().into()),
        }
        .into();
        eval_out_wo_ctx::<bool>(&expr)
    }

    #[test]
    fn test_bigint_extremes() {
        let b = BigInt256::from;
        // Our BigInt should behave like a 256 bit signed (two's complement) integer according to
        // the language spec. These are the max and min values representable:
        let max = BigInt256::max_value;
        let min = BigInt256::min_value;

        assert!(eval_arith_op(ArithOp::Multiply, max(), b(2)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Multiply, max(), b(1)), Ok(max()));
        assert!(eval_arith_op(ArithOp::Multiply, min(), b(2)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Multiply, min(), b(1)), Ok(min()));

        assert!(eval_arith_op(ArithOp::Divide, min(), b(-1)).is_err());
        assert_eq!(
            eval_arith_op(ArithOp::Divide, min() + b(1), b(-1)),
            Ok(max())
        );
        assert!(eval_arith_op(ArithOp::Divide, b(20), b(0)).is_err());

        assert!(eval_arith_op(ArithOp::Modulo, b(20), b(-1)).is_err());
        assert!(eval_arith_op(ArithOp::Modulo, b(20), b(0)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Modulo, max(), b(1)), Ok(b(0)));
        assert_eq!(eval_arith_op(ArithOp::Modulo, min(), b(1)), Ok(b(0)));

        assert!(eval_arith_op(ArithOp::Plus, max(), b(1)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Plus, max(), b(0)), Ok(max()));
        assert!(eval_arith_op(ArithOp::Plus, min(), b(-1)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Plus, min(), b(0)), Ok(min()));

        assert!(eval_arith_op(ArithOp::Minus, max(), b(-1)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Minus, max(), b(0)), Ok(max()));
        assert!(eval_arith_op(ArithOp::Minus, min(), b(1)).is_err());
        assert_eq!(eval_arith_op(ArithOp::Minus, min(), b(0)), Ok(min()));

        assert_eq!(eval_bit_op(BitOp::BitAnd, max(), min()), Ok(b(0)));
        assert_eq!(eval_bit_op(BitOp::BitOr, max(), min()), Ok(b(-1)));
        assert_eq!(eval_bit_op(BitOp::BitXor, max(), min()), Ok(b(-1)));
    }

    proptest! {

        #![proptest_config(ProptestConfig::with_cases(32))]

        #[test]
        fn test_eq(v in any::<Constant>()) {
            prop_assert![check_eq_neq(v.clone(), v)];
        }

        #[test]
        fn test_num_slong(l in any::<i64>(), r in any::<i64>()) {
            prop_assert_eq!(eval_arith_op(ArithOp::Plus, l, r).ok(), l.checked_add(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Minus, l, r).ok(), l.checked_sub(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Multiply, l, r).ok(), l.checked_mul(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Divide, l, r).ok(), l.checked_div(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Modulo, l, r).ok(), l.checked_rem(r));
            prop_assert_eq!(eval_arith_op::<i64>(ArithOp::Max, l, r).unwrap(), l.max(r));
            prop_assert_eq!(eval_arith_op::<i64>(ArithOp::Min, l, r).unwrap(), l.min(r));

            prop_assert_eq!(eval_bit_op(BitOp::BitAnd, l, r), Ok(l & r));
            prop_assert_eq!(eval_bit_op(BitOp::BitOr, l, r), Ok(l | r));
            prop_assert_eq!(eval_bit_op(BitOp::BitXor, l, r), Ok(l ^ r));

            prop_assert_eq!(eval_relation_op(RelationOp::Gt, l, r), l > r);
            prop_assert_eq!(eval_relation_op(RelationOp::Lt, l, r), l < r);
            prop_assert_eq!(eval_relation_op(RelationOp::Ge, l, r), l >= r);
            prop_assert_eq!(eval_relation_op(RelationOp::Le, l, r), l <= r);
        }

        #[test]
        fn test_num_sint(l in any::<i32>(), r in any::<i32>()) {
            prop_assert_eq!(eval_arith_op(ArithOp::Plus, l, r).ok(), l.checked_add(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Minus, l, r).ok(), l.checked_sub(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Multiply, l, r).ok(), l.checked_mul(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Divide, l, r).ok(), l.checked_div(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Modulo, l, r).ok(), l.checked_rem(r));
            prop_assert_eq!(eval_arith_op::<i32>(ArithOp::Max, l, r).unwrap(), l.max(r));
            prop_assert_eq!(eval_arith_op::<i32>(ArithOp::Min, l, r).unwrap(), l.min(r));

            prop_assert_eq!(eval_bit_op(BitOp::BitAnd, l, r), Ok(l & r));
            prop_assert_eq!(eval_bit_op(BitOp::BitOr, l, r), Ok(l | r));
            prop_assert_eq!(eval_bit_op(BitOp::BitXor, l, r), Ok(l ^ r));

            prop_assert_eq!(eval_relation_op(RelationOp::Gt, l, r), l > r);
            prop_assert_eq!(eval_relation_op(RelationOp::Lt, l, r), l < r);
            prop_assert_eq!(eval_relation_op(RelationOp::Ge, l, r), l >= r);
            prop_assert_eq!(eval_relation_op(RelationOp::Le, l, r), l <= r);
        }

        #[test]
        fn test_num_sshort(l in any::<i16>(), r in any::<i16>()) {
            prop_assert_eq!(eval_arith_op(ArithOp::Plus, l, r).ok(), l.checked_add(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Minus, l, r).ok(), l.checked_sub(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Multiply, l, r).ok(), l.checked_mul(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Divide, l, r).ok(), l.checked_div(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Modulo, l, r).ok(), l.checked_rem(r));
            prop_assert_eq!(eval_arith_op::<i16>(ArithOp::Max, l, r).unwrap(), l.max(r));
            prop_assert_eq!(eval_arith_op::<i16>(ArithOp::Min, l, r).unwrap(), l.min(r));

            prop_assert_eq!(eval_bit_op(BitOp::BitAnd, l, r), Ok(l & r));
            prop_assert_eq!(eval_bit_op(BitOp::BitOr, l, r), Ok(l | r));
            prop_assert_eq!(eval_bit_op(BitOp::BitXor, l, r), Ok(l ^ r));

            prop_assert_eq!(eval_relation_op(RelationOp::Gt, l, r), l > r);
            prop_assert_eq!(eval_relation_op(RelationOp::Lt, l, r), l < r);
            prop_assert_eq!(eval_relation_op(RelationOp::Ge, l, r), l >= r);
            prop_assert_eq!(eval_relation_op(RelationOp::Le, l, r), l <= r);
        }

        #[test]
        fn test_num_sbyte(l in any::<i8>(), r in any::<i8>()) {
            prop_assert_eq!(eval_arith_op(ArithOp::Plus, l, r).ok(), l.checked_add(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Minus, l, r).ok(), l.checked_sub(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Multiply, l, r).ok(), l.checked_mul(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Divide, l, r).ok(), l.checked_div(r));
            prop_assert_eq!(eval_arith_op(ArithOp::Modulo, l, r).ok(), l.checked_rem(r));
            prop_assert_eq!(eval_arith_op::<i8>(ArithOp::Max, l, r).unwrap(), l.max(r));
            prop_assert_eq!(eval_arith_op::<i8>(ArithOp::Min, l, r).unwrap(), l.min(r));

            prop_assert_eq!(eval_bit_op(BitOp::BitAnd, l, r), Ok(l & r));
            prop_assert_eq!(eval_bit_op(BitOp::BitOr, l, r), Ok(l | r));
            prop_assert_eq!(eval_bit_op(BitOp::BitXor, l, r), Ok(l ^ r));

            prop_assert_eq!(eval_relation_op(RelationOp::Gt, l, r), l > r);
            prop_assert_eq!(eval_relation_op(RelationOp::Lt, l, r), l < r);
            prop_assert_eq!(eval_relation_op(RelationOp::Ge, l, r), l >= r);
            prop_assert_eq!(eval_relation_op(RelationOp::Le, l, r), l <= r);
        }

        #[test]
        fn test_num_bigint(l_long in any::<i64>(), r_long in any::<i64>()) {
            let l = BigInt256::from(l_long);
            let r = BigInt256::from(r_long);
            prop_assert_eq!(eval_arith_op(ArithOp::Plus, l, r).ok(), l.checked_add(&r));
            prop_assert_eq!(eval_arith_op(ArithOp::Minus, l, r).ok(), l.checked_sub(&r));
            prop_assert_eq!(eval_arith_op(ArithOp::Multiply, l, r).ok(), l.checked_mul(&r));
            prop_assert_eq!(eval_arith_op(ArithOp::Divide, l, r).ok(), l.checked_div(&r));
            prop_assert_eq!(eval_arith_op(ArithOp::Modulo, l, r).ok(), l.checked_rem(&r));
            prop_assert_eq!(eval_arith_op::<BigInt256>(ArithOp::Max, l,
                    r).unwrap(), l.max(r));
            prop_assert_eq!(eval_arith_op::<BigInt256>(ArithOp::Min, l,
                    r).unwrap(), l.min(r));

            prop_assert_eq!(eval_bit_op(BitOp::BitAnd, l, r), Ok(l & r));
            prop_assert_eq!(eval_bit_op(BitOp::BitOr, l, r), Ok(l | r));
            prop_assert_eq!(eval_bit_op(BitOp::BitXor, l, r), Ok(l ^ r));

            prop_assert_eq!(eval_relation_op(RelationOp::Gt, l, r), l > r);
            prop_assert_eq!(eval_relation_op(RelationOp::Lt, l, r), l < r);
            prop_assert_eq!(eval_relation_op(RelationOp::Ge, l, r), l >= r);
            prop_assert_eq!(eval_relation_op(RelationOp::Le, l, r), l <= r);
        }

        #[test]
        fn test_and_or_xor(l in any::<bool>(), r in any::<bool>()) {
            prop_assert_eq!(eval_logical_op(LogicalOp::And, l, r), l && r);
            prop_assert_eq!(eval_logical_op(LogicalOp::Or, l, r), l || r);
            prop_assert_eq!(eval_logical_op(LogicalOp::Xor, l, r), l ^ r);
        }
    }
}
