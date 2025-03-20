#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Helper functions for pd.DataFrame
version: 1.0
type: module
keywords: [data frame, align, NaN, count levels factors, datetime, ]
description: |
    Aligning series and data frames safely passing other types.
    Converting to proper datetime format.
    Readable memory usage for data frame.
content:
remarks:
todo:
sources:
file:
"""

# %%
import numpy as np
import pandas as pd

from typing import List, Union, Optional, Any, TypeVar

Data = Union[pd.DataFrame, pd.Series]
DataVar = TypeVar('DataVar', pd.DataFrame, pd.Series)

NUMS = {"float", "float64", "int", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8"}


# %%
def get_column_or_except(
        colname: str, data: Optional[pd.DataFrame], error_suffix: str = ""
) -> pd.Series:
    """
    Returns `data[colname]` or
    throws specific exception if `data` is None or there is no `colname` in `data.columns`.
    `error_suffix` allows to add additional information to error message.
    """
    if data is not None:
        if colname in data.columns:
            res = data[colname]
        else:
            error = f"There is no column '{colname}' in `data`. " + error_suffix
            raise Exception(error)
    else:
        raise Exception("`data` is None. " + error_suffix)
    return res


# %%  exactly the same in plots.helpers
def sample(
        data: Data, n: int, shuffle: bool, random_state: int,
        extremes: Optional[int | float] = .02,
) -> Data:
    """
    extremes: Optional[int | float] = None
        e.g. 200 means: take 100 lowest and 100 greatest values of each of numeric variable from `data`
        before sampling `n - 200` of other values;
        if float then it's translated into `n * extremes` whith the same meaning as above;
        if None or 0 then sampling is done directly without caring for extreme values to be always chosen;
    """
    N = len(data)
    np.random.seed(random_state)
    if n and n < N:
        if extremes:
            if isinstance(extremes, float):
                extremes = n * extremes
            m = int(round(min(max(extremes, 2), n - 4) / 2))    # always between [1, n/2 - 1]
            if isinstance(data, pd.Series) and str(data.dtype) in NUMS:
                data = data.sort_values()
                idx = data.iloc[:m].index.union(data.iloc[-m:].index)
                r = n - 2 * m
            if isinstance(data, pd.DataFrame):
                idx = pd.Index([])
                for c in data.columns:
                    if str(data[c].dtype) in NUMS:
                        zz = data[c].sort_values()
                        idx_c = zz.iloc[:m].index.union(zz.iloc[-m:].index)
                        idx = idx.union(idx_c)
                        if len(idx) >= n:
                            break
                    else:
                        continue
                r = n - len(idx)
            if r > 0:
                idx_rest = data.index.difference(idx)
                idx_rest = np.random.choice(idx_rest, size=r, replace=False)
            idx = idx.union(idx_rest)
        else:
            idx = np.random.choice(data.index, size=n, replace=False)
        data = data.loc[idx]
    if shuffle:
        data = data.sample(frac=1, random_state=random_state)
    else:
        data = data.sort_index()  # it is usually original order (but not for sure...)
    return data


# %%
def align_indices(data: DataVar, *args: pd.Series | Any | None) -> List[DataVar | Any | None]:
    """
    Replace indices of all pd.Series passed to `args` with index of `data`.
    It will work only if all the series have the same length.

    Arguments
    ---------
    data: pd.Series | pd.DataFrame;
        main data (pd.Series or pd.DataFrame)
        the index of which will replace index of every pd.Series from `args`;
    args: arguments of any type;
        all the pd.Series from `args` will have their indices replaced
        with the index of `data`;
        objects of other types are ignored, and returned intact.

    Returns
    -------
    [data, *args]
    with changes to the `args` elements as described above.
    """
    idx = data.index
    result: List[DataVar | Any | None] = [data]
    for item in args:
        if isinstance(item, pd.Series):
            item.index = idx
            result.append(item)
        else:
            result.append(item)

    return result


# %%
def align_nonas(data: DataVar, **kwargs: pd.Series | Any | None) -> List[DataVar | Any | None]:
    """
    Align (all the pd.Series passed) wrt no-NaN values, i.e.
    merging all the series from `kwargs` __using their indices__
    and removing all records with NaN (or None, etc.);

    Arguments
    ---------
    data: pd.Series | pd.DataFrame;
        main data (pd.Series or pd.DataFrame),
        a data to which all the other arguments from `kwargs`
        are tried to be aligned with __using their indices__;
    kwargs: key-value pairs where values are of Any type
        all values being pd.Series will be processed as described above;
        values of other types are ignored, and returned intact.

    Returns
    -------
    [data, *kwargs.values()]
    with changes to the `kwargs.values()` elements as described above.
    """
    length = len(data)
    df = pd.DataFrame(data)
    used_keys_dict = dict()  # recording proper pd.Series entries of kwargs
    k0 = df.shape[1]
    k = k0 - 1

    for name, ss in kwargs.items():
        if isinstance(ss, pd.Series):
            k += 1
            used_keys_dict[k] = name
            ss = ss.dropna()
            df = pd.merge(df, ss, left_index=True, right_index=True, how='inner')     # 'inner' is default
            if len(df) < length:
                print(f"WARNING! There were empty entries for `{name}` or it does not align with data",
                       "-- data was pruned accordingly!\n",
                      f"Only {len(df)} records left.")
                length = len(df)

    if len(used_keys_dict) > 0:
        data = df.iloc[:, :k0] if isinstance(data, pd.DataFrame) else df.iloc[:, 0]  # .iloc[:,0] –> Series, .iloc[:,:1] –> DataFrame  # noqa
        for k, name in used_keys_dict.items():
            kwargs[name] = df.iloc[:, k]

    result = [data, *kwargs.values()]     # !!! order of input preserved !!!

    return result


# %%
def align_sample(
        data: DataVar,
        n_obs: int = int(1e4), shuffle: bool = False, random_state: int = 2, extremes: Optional[int | float] = .02,
        **kwargs: pd.Series | Any | None
) -> List[DataVar | Any | None]:
    """
    Similar to `align_nonas` but here we only sample and shuffle `data`
    and try to shuffle all the other pd.Series from `kwargs` in the same way.
    Other (non pd.Series) arguments from `kwargs` are returned intact.

    Arguments
    ---------
    data: pd.Series | pd.DataFrame;
        main data (pd.Series or pd.DataFrame),
        which are subject to sampling with optional shuffling;
        after this all the other arguments from `kwargs`
        are tried to be aligned with `data` __using their indices__;
    n_obs: int = int(1e4),
        number of observations to sample;
    shuffle: bool = False,
        do shuffle `data` or not?
    random_state: int = 2,
        seed for random sampling and shuffling;
    extremes: Optional[int | float] = .02
        in not 0 or None then this is number of extreme values for each numeric variable to be sampled;
        when float then it means portion of `n_obs`;
    kwargs: key-value pairs where values are of Any type
        all values being pd.Series will be processed as described above;
        values of other types are ignored, and returned intact.

    Returns
    -------
    [data, *kwargs.values()]
    with changes to the `kwargs.values()` elements as described above.
    """
    df = pd.DataFrame(data)  # spurious pd.DataFrame only to please mypy...
    df = sample(df, n_obs, shuffle, random_state, extremes)

    used_keys_dict = dict()  # recording proper pd.Series entries of kwargs
    k0 = df.shape[1]
    k = k0 - 1

    for name, ss in kwargs.items():
        if isinstance(ss, pd.Series):
            k += 1
            used_keys_dict[k] = name
            df = pd.merge(df, ss, left_index=True, right_index=True, how='left')  # 'inner' is default

    if shuffle:
        df.index = range(len(df))

    data = df.iloc[:, :k0] if isinstance(data, pd.DataFrame) else df.iloc[:, 0]  # .iloc[:,0] –> Series, .iloc[:,:1] –> DataFrame  # noqa
    if len(used_keys_dict) > 0:
        for k, name in used_keys_dict.items():
            kwargs[name] = df.iloc[:, k]

    result = [data, *kwargs.values()]     # !!! order of input preserved !!!

    return result


# %%
