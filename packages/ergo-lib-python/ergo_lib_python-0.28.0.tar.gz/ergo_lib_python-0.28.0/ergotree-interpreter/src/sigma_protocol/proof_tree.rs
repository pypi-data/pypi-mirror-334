//! ProofTree

extern crate derive_more;

use core::fmt::Debug;

use derive_more::From;
use derive_more::TryInto;
use ergotree_ir::sigma_protocol::sigma_boolean::SigmaBoolean;
use ergotree_ir::sigma_protocol::sigma_boolean::SigmaConjectureItems;

use crate::sigma_protocol::unproven_tree::CandUnproven;
use crate::sigma_protocol::unproven_tree::UnprovenConjecture;
use crate::sigma_protocol::UncheckedSchnorr;
use crate::sigma_protocol::UnprovenSchnorr;

use super::challenge::Challenge;
use super::prover::ProverError;
use super::unchecked_tree::UncheckedConjecture;
use super::unchecked_tree::UncheckedDhTuple;
use super::unchecked_tree::UncheckedTree;
use super::unproven_tree::CorUnproven;
use super::unproven_tree::CthresholdUnproven;
use super::unproven_tree::UnprovenDhTuple;
use super::unproven_tree::UnprovenLeaf;
use super::unproven_tree::UnprovenTree;
use super::FirstProverMessage;

/// Proof tree
#[derive(PartialEq, Debug, Clone, From, TryInto)]
pub(crate) enum ProofTree {
    /// Unchecked tree
    UncheckedTree(UncheckedTree),
    /// Unproven tree
    UnprovenTree(UnprovenTree),
}

impl ProofTree {
    /// Create a new proof tree with a new challenge
    pub(crate) fn with_challenge(&self, challenge: Challenge) -> ProofTree {
        match self {
            ProofTree::UncheckedTree(uc) => uc.clone().with_challenge(challenge).into(),
            ProofTree::UnprovenTree(ut) => ut.clone().with_challenge(challenge).into(),
        }
    }

    pub(crate) fn as_tree_kind(&self) -> ProofTreeKind {
        match self {
            ProofTree::UncheckedTree(unch) => unch.as_tree_kind(),
            ProofTree::UnprovenTree(unp) => unp.as_tree_kind(),
        }
    }

    pub(crate) fn challenge(&self) -> Option<Challenge> {
        match self {
            ProofTree::UncheckedTree(unch) => Some(unch.challenge()),
            ProofTree::UnprovenTree(unp) => unp.challenge(),
        }
    }
}

impl From<UncheckedSchnorr> for ProofTree {
    fn from(v: UncheckedSchnorr) -> Self {
        UncheckedTree::UncheckedLeaf(v.into()).into()
    }
}

impl From<UncheckedDhTuple> for ProofTree {
    fn from(v: UncheckedDhTuple) -> Self {
        UncheckedTree::UncheckedLeaf(v.into()).into()
    }
}

impl From<UnprovenSchnorr> for ProofTree {
    fn from(v: UnprovenSchnorr) -> Self {
        UnprovenTree::UnprovenLeaf(v.into()).into()
    }
}

impl From<UnprovenDhTuple> for ProofTree {
    fn from(v: UnprovenDhTuple) -> Self {
        UnprovenTree::UnprovenLeaf(v.into()).into()
    }
}

impl From<CandUnproven> for ProofTree {
    fn from(v: CandUnproven) -> Self {
        UnprovenTree::UnprovenConjecture(v.into()).into()
    }
}

impl From<CorUnproven> for ProofTree {
    fn from(v: CorUnproven) -> Self {
        UnprovenTree::UnprovenConjecture(v.into()).into()
    }
}

impl From<UnprovenConjecture> for ProofTree {
    fn from(v: UnprovenConjecture) -> Self {
        UnprovenTree::UnprovenConjecture(v).into()
    }
}

impl From<UnprovenLeaf> for ProofTree {
    fn from(v: UnprovenLeaf) -> Self {
        UnprovenTree::UnprovenLeaf(v).into()
    }
}

impl From<UncheckedConjecture> for ProofTree {
    fn from(v: UncheckedConjecture) -> Self {
        UncheckedTree::UncheckedConjecture(v).into()
    }
}

impl From<CthresholdUnproven> for ProofTree {
    fn from(v: CthresholdUnproven) -> Self {
        UnprovenTree::UnprovenConjecture(v.into()).into()
    }
}

/// Proof tree leaf
pub trait ProofTreeLeaf: Debug {
    /// Get proposition
    fn proposition(&self) -> SigmaBoolean;

    /// Get commitment
    fn commitment_opt(&self) -> Option<FirstProverMessage>;
}

pub(crate) enum ConjectureType {
    And = 0,
    Or = 1,
    Threshold = 2,
}

pub(crate) trait ProofTreeConjecture {
    fn conjecture_type(&self) -> ConjectureType;
    fn children(&self) -> SigmaConjectureItems<ProofTree>;
}

pub(crate) enum ProofTreeKind<'a> {
    Leaf(&'a dyn ProofTreeLeaf),
    Conjecture(&'a dyn ProofTreeConjecture),
}

/// Traverses the tree in the bottom-up manner, calling `f` for every node/leaf and setting
/// it's returned value (if `Some`) as new node/leaf or do nothing if it's returned `None`
pub(crate) fn rewrite_bu<F>(tree: ProofTree, f: &F) -> Result<ProofTree, ProverError>
where
    F: Fn(&ProofTree) -> Result<Option<ProofTree>, ProverError>,
{
    let cast_to_ust = |children: SigmaConjectureItems<ProofTree>| {
        children.try_mapped(|c| {
            if let ProofTree::UncheckedTree(ust) = c {
                Ok(ust)
            } else {
                Err(ProverError::Unexpected(
                    "rewrite: expected UncheckedSigmaTree got UnprovenTree",
                ))
            }
        })
    };

    let tree_with_updated_children = match &tree {
        ProofTree::UnprovenTree(unp_tree) => match unp_tree {
            UnprovenTree::UnprovenLeaf(_) => tree,
            UnprovenTree::UnprovenConjecture(conj) => match conj {
                UnprovenConjecture::CandUnproven(cand) => UnprovenTree::UnprovenConjecture(
                    UnprovenConjecture::CandUnproven(CandUnproven {
                        children: cand.children.clone().try_mapped(|c| rewrite_bu(c, f))?,
                        ..cand.clone()
                    }),
                )
                .into(),
                UnprovenConjecture::CorUnproven(cor) => {
                    UnprovenTree::UnprovenConjecture(UnprovenConjecture::CorUnproven(CorUnproven {
                        children: cor.children.clone().try_mapped(|c| rewrite_bu(c, f))?,
                        ..cor.clone()
                    }))
                    .into()
                }
                UnprovenConjecture::CthresholdUnproven(ct) => {
                    UnprovenTree::UnprovenConjecture(UnprovenConjecture::CthresholdUnproven(
                        ct.clone()
                            .with_children(ct.clone().children.try_mapped(|c| rewrite_bu(c, f))?),
                    ))
                    .into()
                }
            },
        },
        ProofTree::UncheckedTree(unch_tree) => match unch_tree {
            UncheckedTree::UncheckedLeaf(_) => tree,
            UncheckedTree::UncheckedConjecture(conj) => match conj {
                UncheckedConjecture::CandUnchecked {
                    challenge,
                    children,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_bu(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CandUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                    }
                    .into()
                }
                UncheckedConjecture::CorUnchecked {
                    challenge,
                    children,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_bu(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CorUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                    }
                    .into()
                }
                UncheckedConjecture::CthresholdUnchecked {
                    challenge,
                    children,
                    k,
                    polynomial: polynomial_opt,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_bu(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CthresholdUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                        k: *k,
                        polynomial: polynomial_opt.clone(),
                    }
                    .into()
                }
            },
        },
    };
    Ok(f(&tree_with_updated_children)?.unwrap_or(tree_with_updated_children))
}

/// Traverses the tree in the top-down manner, calling `f` for every node/leaf and setting
/// it's returned value (if `Some`) as new node/leaf or do nothing if it's returned `None`
pub(crate) fn rewrite_td<F>(tree: ProofTree, f: &F) -> Result<ProofTree, ProverError>
where
    F: Fn(&ProofTree) -> Result<Option<ProofTree>, ProverError>,
{
    let cast_to_ust = |children: SigmaConjectureItems<ProofTree>| {
        children.try_mapped(|c| {
            if let ProofTree::UncheckedTree(ust) = c {
                Ok(ust)
            } else {
                Err(ProverError::Unexpected(
                    "rewrite: expected UncheckedSigmaTree got UnprovenTree",
                ))
            }
        })
    };

    let rewritten_tree = f(&tree)?.unwrap_or(tree);
    Ok(match &rewritten_tree {
        ProofTree::UnprovenTree(unp_tree) => match unp_tree {
            UnprovenTree::UnprovenLeaf(_) => rewritten_tree,
            UnprovenTree::UnprovenConjecture(conj) => match conj {
                UnprovenConjecture::CandUnproven(cand) => UnprovenTree::UnprovenConjecture(
                    UnprovenConjecture::CandUnproven(CandUnproven {
                        children: cand.children.clone().try_mapped(|c| rewrite_td(c, f))?,
                        ..cand.clone()
                    }),
                )
                .into(),
                UnprovenConjecture::CorUnproven(cor) => {
                    UnprovenTree::UnprovenConjecture(UnprovenConjecture::CorUnproven(CorUnproven {
                        children: cor.children.clone().try_mapped(|c| rewrite_td(c, f))?,
                        ..cor.clone()
                    }))
                    .into()
                }
                UnprovenConjecture::CthresholdUnproven(ct) => {
                    UnprovenTree::UnprovenConjecture(UnprovenConjecture::CthresholdUnproven(
                        ct.clone()
                            .with_children(ct.clone().children.try_mapped(|c| rewrite_td(c, f))?),
                    ))
                    .into()
                }
            },
        },
        ProofTree::UncheckedTree(unch_tree) => match unch_tree {
            UncheckedTree::UncheckedLeaf(_) => rewritten_tree,
            UncheckedTree::UncheckedConjecture(conj) => match conj {
                UncheckedConjecture::CandUnchecked {
                    challenge,
                    children,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_td(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CandUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                    }
                    .into()
                }
                UncheckedConjecture::CorUnchecked {
                    challenge,
                    children,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_td(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CorUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                    }
                    .into()
                }
                UncheckedConjecture::CthresholdUnchecked {
                    challenge,
                    children,
                    k,
                    polynomial: polynomial_opt,
                } => {
                    let rewritten_children =
                        children.clone().try_mapped(|c| rewrite_td(c.into(), f))?;
                    let casted_children = cast_to_ust(rewritten_children)?;
                    UncheckedConjecture::CthresholdUnchecked {
                        children: casted_children,
                        challenge: challenge.clone(),
                        k: *k,
                        polynomial: polynomial_opt.clone(),
                    }
                    .into()
                }
            },
        },
    })
}
