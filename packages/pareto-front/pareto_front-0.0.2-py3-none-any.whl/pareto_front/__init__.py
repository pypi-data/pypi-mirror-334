"""Pareto-front calculation functions."""

from typing import Union

import numpy as np
import pandas as pd
from multipledispatch import dispatch


def pareto_indices(data: pd.DataFrame) -> pd.Index:
    """
    Return the Pareto efficient row subset of a columnar dataset.

    Inspired from: https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python

    :param data: A numpy array of shape (n_samples, n_dims).
    :returns: All samples which lie on the pareto front considering all dimensions.
    """
    pareto_front_indices = data.sum(axis=1).sort_values(ascending=False).index
    data = data.loc[pareto_front_indices]
    undominated = np.ones(data.shape[0], dtype=bool)
    for i in range(data.shape[0]):
        n = data.shape[0]
        if i >= n:
            break
        # We use `.iloc` here b/c the sorted order of values is important.
        undominated[i + 1 : n] = (data.iloc[i + 1 :] > data.iloc[i]).any(axis=1)
        pareto_front_indices = pareto_front_indices[undominated[:n]]
        data = data.loc[undominated[:n]]
    return pareto_front_indices


@dispatch(np.ndarray)
def pareto_front(data: np.ndarray) -> pd.DataFrame:
    """Return pareto front of a NumPy array.

    :param data: n-dimensional NumPy array of shape (n_samples, n_dimensions).
        n_dimensions should be >= 2.
    :returns: The subset of samples that correspond to the pareto front.
    """
    data = pd.DataFrame(data)
    return pareto_front(data)


@dispatch(pd.DataFrame)
def pareto_front(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate pareto front points from a pandas DataFrame.

    :param data: pandas DataFrame of shape (n_samples, n_dimensions).
        n_dimensions should be >= 2.
    :returns: The subset of samples that correspond to the pareto front.
    """
    idxs = pareto_indices(data)
    return data.loc[idxs]


def pareto_collection(data: Union[np.ndarray, pd.DataFrame], n: int) -> pd.DataFrame:
    """Recursively collect pareto fronts up till n samples.

    :param data: Data on which to progressively collect pareto fronts.
    :param n: Number of samples to collected.
    :returns: A pandas DataFrame of length `n`.
    """
    in_consideration = data.copy()
    samples = pd.DataFrame()

    while len(samples) < n:
        pfront = pareto_front(in_consideration)
        samples = pd.concat([samples, pfront])
        remaining_index = in_consideration.index.difference(pfront.index)
        in_consideration = in_consideration.loc[remaining_index]

    samples = samples.head(n)
    return samples
