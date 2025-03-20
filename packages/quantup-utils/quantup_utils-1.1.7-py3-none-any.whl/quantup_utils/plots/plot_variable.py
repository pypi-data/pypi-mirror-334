#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Diagnostic plots for one variable
version: 1.0
type: module
keywords: [plot, variable, numeric, factor]
description: |
    Custom diagnostic plots for one variable;
    For numeric:
        - histogram
        - cloud
        - density
        - distribution
        - sum vs counts (wrt to groups from histogram)
        - boxplot
    or just:
        - barplot
    for categorical.
    Any configuration of the above types of plots are possible via `what` parameter.
    The idea is to make it automated wrt different types of variables
    (numeric / categorical);
    maximum flexibility (lots of parameters) but with sensible defaults.
    This allows to do well with difficult cases like numeric variables with
    small nr of different values (better to plot it as categorical)
    or categorical variables with large number of different values
    (better to (bar)plot only most common values), etc.
content:
remarks:
todo:
sources:
file:
    date: 2021-10-30
    authors:
        - fullname: Arkadiusz Kasprzyk
          email:
              - arkadiusz.kasprzyk@quantup.pl
"""

# %%
import numpy as np
import pandas as pd

from ..builtin import coalesce
from .plot_numeric import plot_numeric
from .plot_factor import plot_factor
from . import helpers as h

from typing import Union, Sequence, List, Tuple, Literal, Callable, Optional, MutableMapping
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]
Transformation = Callable[[Numeric], Numeric]
Aggregate = Callable[[Numeric], float]
PlotType = Literal["hist", "cloud", "density", "agg", "boxplot", "distr"]
ListPlotType = List[PlotType] | List[List[PlotType]] | NDArray[PlotType]  # type: ignore  # cannot be PlotType but it MUST be PlotType (and works!)  # noqa
Scale = Literal["linear", "log"]


# %%
def plot_variable(
        variable: str | Variable,
        data: Optional[pd.DataFrame] = None,
        varname: Optional[str] = None,
        as_factor: Optional[bool] = None,
        factor_threshold: int = 13,  # datetime=False,  # ! TODO
        # Size parameters
        # # common – works if respective param for num/fac (below) is None
        # ## for the whole figure
        figsize: Optional[Tuple[float, float]] = None,
        figwidth: Optional[float] = None,
        figheight: Optional[float] = None,
        # ## for separate axes (subplots) but for all of them
        width: Optional[float] = None,
        height: Optional[float] = None,
        size: float = 5,
        width_adjust: float = 1.2,
        # # for numerics – overwrites 'common' params (above)
        num_figsize: Optional[Tuple[float, float]] = None,
        num_figwidth: Optional[float] = None,
        num_figheight: Optional[float] = None,
        num_width: Optional[float] = None,
        num_height: Optional[float] = None,
        num_size: float = 5,
        num_width_adjust: float = 1.2,
        # # for factors – overwrites 'common' params (above)
        fac_figsize: Optional[Tuple[float, float]] = None,
        fac_figwidth: Optional[float] = None,
        fac_figheight: Optional[float] = None,
        fac_width: Optional[float] = None,
        fac_height: Optional[float] = None,
        fac_size: float = 5,
        fac_width_adjust: float = 1.2,
        # all the other params passed to plot_numeric() and plot_factor()
        *args, **kwargs
) -> Optional[MutableMapping]:
    """
    This function is only a dispatcher between
    - plot_numeric() for numeric data
    and
    - plot_factor() for categorical data (factors).
    All arguments for these specific functions are properly passed to them.
    Which specific version of `plot_` to use is decided according to two additional parameters:

    as_factor : bool = None
        If None then type of variable (thus which `plot_` to use) is decided according to `variable.dtype` argument;
        if it belongs to ["category", "object", "str", "datetime64[s]", "datetime64[ns]", "datetime64"]
        then we consider variable as categorical, a factor, thus `plot_factor()` is used;
        otherwise variable is considered numeric and `plot_numeric()` is used,
        ! however, before that it is also checked if the number of distinct values is less then `factor_threshold`
        – if so then we consider variable as factor anyway.
        One may also force to treat a variable as factor passig `True`
        and then `plot_factor()` is always used (makes sense for numerics with few distinc values).
        On the other hand, passing `False` will always launch `plot_numeric()`
        what will result with almost certain crush for data which are really not numeric (thus beware).
    factor_threshold : int = 13
        if numeric variable has less then `factor_threshold` then it will be treated as factor;
        however, if it's set to 1 or less then effectively it's turned off.

    Size parameters
    ----------------
    The parameters for size of the figure and axes may be passed in the form common for both types of variables,
    i.e.

    ## for the whole figure
    figsize: Optional[Tuple[float, float]] = None,
    figwidth: Optional[float] = None,
    figheight: Optional[float] = None,

    ## for separate axes (subplots) but for all of them
    width: Optional[float] = None,
    height: Optional[float] = None,
    size: float = 5,
    width_adjust: float = 1.2,

    For description of these params see help on plot_numeric() and plot_factor().

    Notice though that these parameters are overwritten by the form specific to the variable type:

    # for numerics

    num_figsize: Optional[Tuple[float, float]] = None,
    num_figwidth: Optional[float] = None,
    num_figheight: Optional[float] = None,
    num_width: Optional[float] = None,
    num_height: Optional[float] = None,
    num_size: float = 5,
    num_width_adjust: float = 1.2,

    # for factors

    fac_figsize: Optional[Tuple[float, float]] = None,
    fac_figwidth: Optional[float] = None,
    fac_figheight: Optional[float] = None,
    fac_width: Optional[float] = None,
    fac_height: Optional[float] = None,
    fac_size: float = 5,
    fac_width_adjust: float = 1.2,

    These form of size params allows to automate reports when the exact type of variable is unknown in advance
    (while the plots for numerics and factors are quite different
     thus in general their size should not be set to commmon values).
    """
    # -----------------------------------------------------
    variable, varname = h.get_var_and_name(variable, data, varname, "X")

    # -----------------------------------------------------

    if as_factor is None:
        as_factor = variable.dtype in ["category", "object", "str", "datetime64[s]", "datetime64[ns]", "datetime64"]
        if not as_factor and factor_threshold > 1:
            as_factor = variable.unique().shape[0] < factor_threshold

    # -----------------------------------------------------

    if as_factor:
        result = plot_factor(
            variable, data=data, varname=varname,
            # for the whole figure
            figsize=coalesce(figsize, fac_figsize),
            figwidth=coalesce(figwidth, fac_figwidth),
            figheight=coalesce(figheight, fac_figheight),
            # for separate axes (subplots) but for all of them
            width=coalesce(width, fac_width),
            height=coalesce(height, fac_height),
            size=coalesce(size, fac_size),
            width_adjust=coalesce(size, fac_width_adjust),
            *args, **kwargs)
    else:
        result = plot_numeric(
            variable, data=data, varname=varname,
            # for the whole figure
            figsize=coalesce(figsize, num_figsize),
            figwidth=coalesce(figwidth, num_figwidth),
            figheight=coalesce(figheight, num_figheight),
            # for separate axes (subplots) but for all of them
            width=coalesce(width, num_width),
            height=coalesce(height, num_height),
            size=coalesce(size, num_size),
            width_adjust=coalesce(width_adjust, num_width_adjust),
            *args, **kwargs)

    if result:
        result['as_factor'] = as_factor

    return result

# %%
