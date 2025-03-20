"""
Implementation of the sampling_tille methods directly to pandas dataframe.
"""

import numpy as np
import pandas as pd
from sampling_tille import (
    srswor,
    stratified_sampling,
    systematic_sampling,
    cluster_sampling,
    cube_sample,
)


def sample(
    df: pd.DataFrame,
    n: int,
    method: str = "simple",
    rng: np.random.Generator | None = None,
    columns: list[str] | None = None,
    stratification: str | None = "proportional",
    balance: list[str] | None = None,
) -> np.array:
    """
    performs pysampling on pandas dataframe.
    :param df: pd.DataFrame the dataframe containing the information of the sample
    :param n: int the number of desired elements in the sample.
    :param method: str|none
        The desired pysampling method.
        Valid values are "simple", "cluster", "stratified", "systematic" or "balanced".
        Default is simple
    :param rng: np.random.Generator|None the random number generator.
    :param columns: list(str) The columns where the stratification or the clustering is desired.
            Only used for "stratified", "cluster" or "balanced" method.
            If method is "cluster" then only the first item is considered.
            The corresponding columns are assumed converted to categorical.
    :param stratification: str|None The kind of stratification used.
            Valid values are "proportional" or "equal_size".
            The default value is "proportional".
    :param balance: list(str)|None The columns where the balancing is desired.
            Only considered if method is "balanced".
    :return: np.array(bool): The mask representing the sample.

    >>> import numpy as np
    >>> from sampling_tille.load_data import load_data
    >>> from sampling_tille.df_sample import sample
    >>> df = load_data('fertility')
    >>> rng = np.random.default_rng(42)
    >>> mask = sample(df, n=20, rng=rng)
    >>> df_out = df[mask]
    >>> df_out.head()
           rownames morekids gender1 gender2  age afam hispanic other  work
    16085     16086      yes  female  female   35   no       no    no    48
    23850     23851       no    male    male   24   no       no    no     0
    32513     32514      yes  female  female   30   no       no    no     0
    57978     57979      yes    male    male   32   no       no    no     0
    94373     94374      yes  female    male   30   no       no    no     0

    """
    mask = np.zeros(len(df))
    match method:
        case "simple":
            mask = srswor(n, len(df), rng=rng)
        case "cluster":
            mask = cluster_sampling(n, pd.Categorical(df[columns[0]]).codes, rng=rng)
        case "stratified":
            cols = np.array([pd.Categorical(df[col]).codes for col in columns]).T
            mask = stratified_sampling(n, cols, stratification, rng=rng)
        case "systematic":
            mask = systematic_sampling(n, len(df), rng=rng)
        case "balanced":
            pi0 = np.ones(len(df)) / len(df) * n
            m = np.ones(len(df))
            if columns:
                m1 = pd.get_dummies(df[columns], drop_first=True).astype(int).values
                m = np.vstack([m.T, m1.T]).T
            if balance:
                m2 = df[balance].values
                m = np.vstack([m.T, m2.T]).T
            if not balance and not columns:
                raise ValueError(
                    '''If "method" is "balanced",
                 at least one between "columns" and "balance" must be given.
                 Alternatively you can use "method"="simple"'''
                )
            mask = cube_sample(pi0, m, rng=rng)
    return mask.astype(bool)
