use hashbrown::HashMap;

use alloc::vec::Vec;

use crate::mir::expr::Expr;
use crate::mir::method_call::MethodCall;
use crate::types::smethod::MethodId;
use crate::types::smethod::SMethod;
use crate::types::stype::SType;
use crate::types::stype_param::STypeVar;

use super::sigma_byte_reader::SigmaByteRead;
use super::sigma_byte_writer::SigmaByteWrite;
use super::types::TypeCode;
use super::SigmaParsingError;
use super::SigmaSerializable;
use super::SigmaSerializeResult;

impl SigmaSerializable for MethodCall {
    fn sigma_serialize<W: SigmaByteWrite>(&self, w: &mut W) -> SigmaSerializeResult {
        self.method.obj_type.type_code().sigma_serialize(w)?;
        self.method.method_id().sigma_serialize(w)?;
        self.obj.sigma_serialize(w)?;
        self.args.sigma_serialize(w)?;
        for type_arg in &self.method.method_raw.explicit_type_args {
            // Should not fail as existence of explicit type args is checked in constructor
            let tpe = &self.explicit_type_args[type_arg];
            tpe.sigma_serialize(w)?;
        }
        Ok(())
    }

    fn sigma_parse<R: SigmaByteRead>(r: &mut R) -> Result<Self, SigmaParsingError> {
        let type_id = TypeCode::sigma_parse(r)?;
        let method_id = MethodId::sigma_parse(r)?;
        let obj = Expr::sigma_parse(r)?;
        let args = Vec::<Expr>::sigma_parse(r)?;
        let arg_types = args.iter().map(|arg| arg.tpe()).collect();
        let method = SMethod::from_ids(type_id, method_id)?.specialize_for(obj.tpe(), arg_types)?;
        if r.tree_version() < method.method_raw.min_version {
            return Err(SigmaParsingError::UnknownMethodId(
                method_id,
                type_id.value(),
            ));
        }
        let explicit_type_args = method
            .method_raw
            .explicit_type_args
            .iter()
            .cloned()
            .zip(core::iter::from_fn(|| Some(SType::sigma_parse(r))))
            .map(|(tpe, res)| -> Result<(STypeVar, SType), SigmaParsingError> { Ok((tpe, res?)) })
            .collect::<Result<HashMap<STypeVar, SType>, _>>()?;
        Ok(MethodCall::with_type_args(
            obj,
            method.with_concrete_types(&explicit_type_args),
            args,
            explicit_type_args,
        )?)
    }
}

#[cfg(test)]
#[cfg(feature = "arbitrary")]
#[allow(clippy::unwrap_used)]
mod tests {
    use alloc::vec;
    use core2::io::{Cursor, Seek, SeekFrom};

    use crate::ergo_tree::ErgoTreeVersion;
    use crate::mir::constant::Constant;
    use crate::mir::expr::Expr;
    use crate::mir::method_call::MethodCall;
    use crate::serialization::constant_store::ConstantStore;
    use crate::serialization::sigma_byte_reader::{SigmaByteRead, SigmaByteReader};
    use crate::serialization::{sigma_serialize_roundtrip, SigmaSerializable};
    use crate::types::stype::SType;
    use crate::types::stype_param::STypeVar;
    use crate::types::{scoll, sglobal};

    #[test]
    fn ser_roundtrip() {
        let mc: Expr = MethodCall::new(
            vec![1i64, 2i64].into(),
            scoll::INDEX_OF_METHOD
                .clone()
                .with_concrete_types(&[(STypeVar::t(), SType::SLong)].iter().cloned().collect()),
            vec![2i64.into(), 0i32.into()],
        )
        .unwrap()
        .into();
        assert_eq![sigma_serialize_roundtrip(&mc), mc];
    }
    // test that methodcalls that are added in later versions via soft-fork can't be parsed with older version
    #[test]
    fn versioned_roundtrip() {
        let mc: Expr = MethodCall::new(
            Expr::Global,
            sglobal::SERIALIZE_METHOD
                .clone()
                .specialize_for(SType::SGlobal, vec![SType::SInt])
                .unwrap(),
            vec![Constant::from(1i32).into()],
        )
        .unwrap()
        .into();
        let serialized = mc.sigma_serialize_bytes().unwrap();
        let mut cursor = Cursor::new(&serialized);
        let mut reader = SigmaByteReader::new(&mut cursor, ConstantStore::empty());
        for version in
            u8::from(ErgoTreeVersion::V0)..sglobal::SERIALIZE_METHOD.method_raw.min_version.into()
        {
            reader.with_tree_version(version.into(), |r| assert!(Expr::sigma_parse(r).is_err()));
            reader.seek(SeekFrom::Start(0)).unwrap();
        }
        for version in u8::from(sglobal::SERIALIZE_METHOD.method_raw.min_version)
            ..=ErgoTreeVersion::MAX_SCRIPT_VERSION.into()
        {
            assert_eq!(
                mc,
                reader
                    .with_tree_version(version.into(), Expr::sigma_parse)
                    .unwrap()
            );
            reader.seek(SeekFrom::Start(0)).unwrap();
        }
    }
}
