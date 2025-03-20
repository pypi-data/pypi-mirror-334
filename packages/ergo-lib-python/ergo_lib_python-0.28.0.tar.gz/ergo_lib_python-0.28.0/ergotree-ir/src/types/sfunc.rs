use hashbrown::HashMap;

use alloc::boxed::Box;
use alloc::vec;
use alloc::vec::Vec;

use super::stype::SType;
use super::stype_param::STypeParam;
use super::stype_param::STypeVar;

/// Function signature type
#[derive(PartialEq, Eq, Debug, Clone)]
pub struct SFunc {
    /// Function parameter types
    pub t_dom: Vec<SType>,
    /// Result type
    pub t_range: Box<SType>,
    /// Type parameters if the function is generic
    pub tpe_params: Vec<STypeParam>,
}

impl core::fmt::Display for SFunc {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "(")?;
        for (i, item) in self.t_dom.iter().enumerate() {
            if i > 0 {
                write!(f, ", ")?;
            }
            item.fmt(f)?;
        }
        write!(f, ") => ")?;
        self.t_range.fmt(f)
    }
}

impl SFunc {
    /// Create new SFunc
    pub fn new(t_dom: Vec<SType>, t_range: SType) -> Self {
        Self {
            t_dom,
            t_range: t_range.into(),
            tpe_params: vec![],
        }
    }

    pub(crate) fn with_subst(&self, subst: &HashMap<STypeVar, SType>) -> Self {
        let remaining_vars = self
            .tpe_params
            .iter()
            .filter(|v| !subst.contains_key(&v.ident))
            .cloned()
            .collect();
        SFunc {
            t_dom: self
                .t_dom
                .iter()
                .map(|a| a.clone().with_subst(subst))
                .collect(),
            t_range: Box::new(self.t_range.with_subst(subst)),
            tpe_params: remaining_vars,
        }
    }

    /// Returns function parameter types (t_dom) with added result type (t_range)
    pub fn t_dom_plus_range(&self) -> Vec<SType> {
        let mut res = self.t_dom.clone();
        res.push(*self.t_range.clone());
        res
    }
}
