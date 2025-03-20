#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
# This is YAML, see: https://yaml.org/spec/1.2/spec.html#Preview
# !!! YAML message always begin with ---

title: Transformators according to instructions
version: 1.0
type: module
keywords: [transformer, variables, instructions]
description: |
    Variables transformers according to instructions from some config lists/dicts/etc.
remarks:
todo:
sources:
"""
# %%
import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin  # type: ignore
from sklearn.preprocessing import PowerTransformer  # type: ignore
from sklearn.exceptions import NotFittedError  # type: ignore

from typing import Callable, Sequence, Union, Tuple, Optional, cast
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]

Transformation = Callable[[Numeric], Numeric]
Standardised = Callable[[pd.Series], Tuple[pd.Series, Callable]]


# %%
def _process_ss(ss: Variable, name: Optional[str] = None) -> tuple[np.ndarray, str, list]:
    """
    Basic preprocessing of vector data into a format acceptable by sklearn transformers
    which accept only np.arrays.
    I.e. turns variable data contained in a sequence (list, tuple, np.array, pd.Series)
    into np.array of shape (N, 1) where N is `ss` length/size.
    Additionally returns name of the data (taken from `ss.name` if `ss` is pd.String
    or set by user or default) and index of it (which is preserved index from pd.Series or
    just `list(range(N))`).
    """
    if isinstance(ss, np.ndarray):
        ss = np.array(ss).reshape(-1, 1)
        idx = list(range(ss.shape[0]))
        sname = name or "no_name"
    else:
        ss = pd.Series(ss)
        idx = ss.index.to_list()
        sname = str(ss.name) if ss.name else name or "no_name"
        ss = np.array(ss).reshape(-1, 1)

    return ss, sname, idx


def from_sklearn_inverse(transformer: TransformerMixin, name: str = "T_inverse") -> Callable:
    """
    transformer: sklearn transformer with .inverse_transform(), .transform() and .fit_transform() methods;
    name: name to be given to standardised version of a transformer.inverse_transform();

    Returns `standardised` version of a sklearn `transformer.inverse_transform()` i.e.
    which works as ordinary function -- not as class with methods.
    Instead of running
    `transformer.inverse_transform(y)` where `y` is necessarily np.array
    one may now run
    `standardised(x)` where `y` may be also a pd.Series for which the result will retain its index.

    `standardised` return pd.Series
    """
    t_inverse = transformer.inverse_transform

    # make it idempotent
    if t_inverse.__qualname__ == 'from_sklearn_inverse.<locals>.standardised':
        inverse = t_inverse

    else:
        if not name:
            name = transformer.__name__ + "_inverse"

        def inverse(ss: pd.Series) -> pd.Series:
            _ss, sname, idx = _process_ss(ss)
            _ss = t_inverse(_ss)[:, 0]
            ss = pd.Series(_ss, index=idx)
            ss.name = sname
            return ss

        inverse.__name__ = name

    return cast(Callable, inverse)  # mypy claims `inverse` returns Any what is obviously not true


# more general
def from_sklearn(transformer: TransformerMixin, name: str = "T") -> Standardised:
    """
    transformer: sklearn transformer with .transform() and .fit_transform() methods;
    name: name to be given to standardised version of a transformer;

    Returns `standardised` version of a sklearn `transformer` i.e.
    which works as ordinary function – not as class with methods.
    Instead of running
    `transformer.transform(x)` or `transformer.fit_transform(x)`
    where `x` is necessarily np.array
    one may now run
    `standardised(x)` where `x` may be also a pd.Series for which the result will retain its index.

    Moreover `standardised` inherits `.inverse_transform()` from fitted `transformer`
    as its method, hence one may run `standardised.inverse_transform(y)` to get `x` back,
    where `y = standardised(x)`.

    ! However, `standardised(x)` returns tuple:
    (y, standardised_fitted)
    where `y` is pd.Series with a value returned from `transformer.fit_transform(x)`
    and `standardised_fitted` is `standardised` with all params fitted.
    """

    # make it idempotent
    if hasattr(transformer, "__qualname__"):
        # it's a trick: we should rather check
        #  transformer.__qualname__ == 'from_sklearn.<locals>.standardised'
        # but sklearn transformers just don't have `__qualname__` attribute
        # so it's enough to check it's existence
        standardised = transformer

    else:
        def standardised(ss: pd.Series) -> tuple[pd.Series, Callable]:
            _ss, sname, idx = _process_ss(ss)

            try:
                _ss = transformer.transform(_ss)[:, 0]
            except NotFittedError:
                print(f"! fitting parameters for {name} on variable {sname}")
                _ss = transformer.fit_transform(_ss)[:, 0]

            ss = pd.Series(_ss, index=idx)
            ss.name = sname

            return ss, from_sklearn(transformer, name)

        standardised.__name__ = name
        standardised.inverse_transform = from_sklearn_inverse(transformer, name + "_inverse")

    return cast(Callable, standardised)  # mypy claims `standardised` returns Any what is obviously not true


def power_transformer(ss: Variable) -> tuple[pd.Series, Callable]:
    """
    Version of from_sklearn() dedicated to sklearn.PowerTransformer solely,
    only to have a good name of the function (used later in some important plots).
    """
    transformer = PowerTransformer()

    _ss, sname, idx = _process_ss(ss)

    try:
        _ss = transformer.transform(_ss)[:, 0]
    except NotFittedError:
        print(f"! fitting parameters for PowerTransformer on variable {sname}")
        _ss = transformer.fit_transform(_ss)[:, 0]

    ss = pd.Series(_ss, index=idx)
    ss.name = sname

    lambda_ = round(transformer.lambdas_[0], 2)
    t_name = transformer.get_params()['method'].title().replace("-", "") + f"_{{\\lambda = {lambda_}}}"

    return ss, from_sklearn(transformer, t_name)
