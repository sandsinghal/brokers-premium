"""
src/graph_metrics.py
--------------------
Reusable graph-metric functions used by main_notebook.ipynb.

Exposes:
    participation_coefficient(G, partition)
    fit_logit_with_inference(X, y, feature_names)
    compute_vif(X_df)

These are identical to the in-notebook definitions, extracted here so that
downstream work (other notebooks, a future paper, course portfolio) can import
them cleanly.
"""
from collections import Counter
from typing import Dict, Hashable, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats as scistats
from sklearn.linear_model import LogisticRegression


def participation_coefficient(G, partition: Dict[Hashable, Hashable]) -> Dict[Hashable, float]:
    """
    Guimerà & Amaral (2005) participation coefficient.

        P_i = 1 - sum_s (k_is / k_i)^2

    Measures how evenly a node's edges are distributed across the groups of
    `partition`. P=0 means all edges fall in a single group (embedded);
    values near 1 mean edges are spread evenly across groups (bridge).

    Parameters
    ----------
    G : networkx.Graph
        Undirected graph.
    partition : dict
        Mapping from node id -> group id.

    Returns
    -------
    dict
        Mapping from node id -> participation coefficient in [0, 1).
    """
    pc: Dict[Hashable, float] = {}
    for node in G.nodes():
        nbrs = list(G.neighbors(node))
        if not nbrs:
            pc[node] = 0.0
            continue
        counts = Counter(partition.get(nb) for nb in nbrs if nb in partition)
        total = sum(counts.values())
        if total == 0:
            pc[node] = 0.0
            continue
        pc[node] = 1.0 - sum((c / total) ** 2 for c in counts.values())
    return pc


def fit_logit_with_inference(
    X: np.ndarray, y: np.ndarray, feature_names: Sequence[str]
) -> Tuple[pd.DataFrame, float]:
    """
    Fit an unpenalized logistic regression and return Wald inference + McFadden pseudo-R².

    The coefficient covariance matrix is estimated via the observed Fisher information:

        Cov(beta) = (X' W X)^-1

    where W = diag(p * (1 - p)) and p are fitted probabilities. This reproduces
    the inferential machinery of `statsmodels.api.Logit` while avoiding its
    binary-compatibility issues on some Colab environments.

    Parameters
    ----------
    X : array of shape (n, k)
        Design matrix without intercept column.
    y : array of shape (n,)
        Binary outcome in {0, 1}.
    feature_names : sequence of str
        Names of the k features (in column order of X).

    Returns
    -------
    summary : pandas.DataFrame
        One row per coefficient (incl. intercept) with columns:
        feature, coef, OR, CI_lo, CI_hi, p_value.
    pseudo_r2 : float
        McFadden's pseudo-R².
    """
    model = LogisticRegression(penalty=None, max_iter=2000, solver="lbfgs").fit(X, y)
    coefs = np.concatenate([model.intercept_, model.coef_[0]])

    X_design = np.column_stack([np.ones(len(X)), X])
    names_full = ["intercept"] + list(feature_names)

    p = model.predict_proba(X)[:, 1]
    W = p * (1 - p)
    fisher = X_design.T @ (W[:, None] * X_design)
    try:
        cov = np.linalg.inv(fisher)
        se = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        se = np.full(len(coefs), np.nan)

    z = coefs / se
    p_vals = 2 * (1 - scistats.norm.cdf(np.abs(z)))
    ci_lo = coefs - 1.96 * se
    ci_hi = coefs + 1.96 * se

    null_ll = np.sum(y * np.log(y.mean()) + (1 - y) * np.log(1 - y.mean()))
    model_ll = np.sum(
        y * np.log(np.clip(p, 1e-10, 1 - 1e-10))
        + (1 - y) * np.log(np.clip(1 - p, 1e-10, 1 - 1e-10))
    )
    pseudo_r2 = 1 - (model_ll / null_ll)

    summary = pd.DataFrame(
        {
            "feature": names_full,
            "coef": coefs,
            "OR": np.exp(coefs),
            "CI_lo": np.exp(ci_lo),
            "CI_hi": np.exp(ci_hi),
            "p_value": p_vals,
        }
    )
    return summary, float(pseudo_r2)


def compute_vif(X_df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute variance-inflation factors for a design matrix.

    VIF_j = 1 / (1 - R²_j), where R²_j is from regressing column j on all other columns.

    Parameters
    ----------
    X_df : pd.DataFrame
        Design matrix (features as columns, no intercept).

    Returns
    -------
    dict
        Mapping from column name -> VIF.
    """
    vifs: Dict[str, float] = {}
    cols = list(X_df.columns)
    X_np = X_df.values
    for i, col in enumerate(cols):
        y_i = X_np[:, i]
        X_others = np.delete(X_np, i, axis=1)
        X_des = np.column_stack([np.ones(len(X_others)), X_others])
        beta, *_ = np.linalg.lstsq(X_des, y_i, rcond=None)
        pred = X_des @ beta
        ss_res = ((y_i - pred) ** 2).sum()
        ss_tot = ((y_i - y_i.mean()) ** 2).sum()
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        vifs[col] = 1 / (1 - r2) if r2 < 1 else float("inf")
    return vifs


__all__ = [
    "participation_coefficient",
    "fit_logit_with_inference",
    "compute_vif",
]
