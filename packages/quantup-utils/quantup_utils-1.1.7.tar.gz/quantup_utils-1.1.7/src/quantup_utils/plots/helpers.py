#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Helper plot functions
version: 1.0
type: sub-module
keywords: [plot, preprocessing]
description: |
content:
remarks:
todo:
sources:
"""

# %%
import numpy as np
import pandas as pd
import math as m

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes, Figure

from ..builtin import flatten, coalesce, reorder, get_optimal_division, adaptive_round
from ..transformations import power_transformer

from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from typing import cast, Union, Sequence, Tuple, Literal, Callable, Optional
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]
Transformation = Callable[[Numeric], Numeric]
Aggregate = Callable[[Numeric], float]

Data = Union[pd.DataFrame, pd.Series]
ColorMap = Union[LinearSegmentedColormap, ListedColormap]

AxisOff = Literal["both", "x", "y"]

# %%  leveled luminosity from  TABLEAU_COLORS  (which is default cycler)
"""this colormap has well leveled luminosity
what is a big problem for all other predifined colormaps (in  mpl.cm)
see https://matplotlib.org/stable/tutorials/colors/colormaps.html#lightness-of-matplotlib-colormaps
"""
default_cycler = [
    (0.0, '#17becf'),   # tab:cyan  (~teal)
    (0.1, '#2ca02c'),   # tab:green
    (0.2, '#7f7f7f'),   # tab:grey  (medium dark)
    (0.35, '#ff7f0e'),  # tab:orange
    (0.5, '#bcbd22'),   # tab:olive (green-yellow-grey)
    (0.65, '#d62728'),  # tab:red
    (0.75, '#9467bd'),  # tab:purple (violet)
    # '#8c564b',  # tab:brown   # too dark
    (0.85, '#e377c2'),  # tab:pink
    (1.0, '#1f77b4'),   # tab:blue
]

mpl.colormaps.register(LinearSegmentedColormap.from_list("ak01", default_cycler), name="ak01", force=True)  # type: ignore # noqa
# follows this example: https://matplotlib.org/stable/users/explain/colors/colormap-manipulation.html#directly-creating-a-segmented-colormap-from-a-list # noqa
# agrees with spec: https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list # noqa

mpl.colormaps.register(ListedColormap(["red", "beige", "green"]), name="bool0", force=True)  # type: ignore
mpl.colormaps.register(ListedColormap(["green", "beige", "red"]), name="bool1", force=True)  # type: ignore


# %%
def is_mpl_color(color: str) -> bool:
    """checking if given name is valid matplotlib color name"""
    res = color in set().union(
        mpl.colors.BASE_COLORS.keys(),
        mpl.colors.TABLEAU_COLORS.keys(),
        mpl.colors.CSS4_COLORS.keys(),
        mpl.colors.XKCD_COLORS.keys()
    )
    return res


# %%
def get_var_and_name(
        variable: Union[str, Variable],
        data: Optional[pd.DataFrame] = None,
        varname: Optional[str] = None,
        default_name: str = "variable",
) -> Tuple[pd.Series, str]:
    """
    Returns `variable` as pd.Series and it's name as separate str object `varname`.
    If `variable` is str then it means column name from `data` which in this case cannot be None.
    `varname` overwrites `variable.name` and if both are None then `varname` is set to `default_name`.
    """
    if isinstance(variable, str):
        if data is not None:
            variable = data[variable].copy()
        else:
            raise Exception(
                'If `variable` is str then `data` must be proper DataFrame containing column named `variable`.')
    else:
        if isinstance(variable, pd.Series):
            pass
        elif isinstance(variable, np.ndarray):
            variable = pd.Series(variable)
        else:
            variable = pd.Series(np.array(variable))
            # for Sequences like lists, tuples, np.array(.) prevents from turning int to float in presence of `None`s

    variable.name = varname = coalesce(varname, variable.name, default_name).replace(" ", "_")

    return variable, cast(str, varname)


# %%
def distribution(variable: Numeric) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Empirical distribution of a `variable`: (x, F(x)) where x is sorted `variable`.
    variable: list/pd.series of floats/integers
        interpreted as n samples of one numeric variable
    """
    n = len(variable)

    variable = pd.Series(variable).sort_values().to_numpy()

    return variable, np.arange(n + 1)[1:] / n


# %%
def agg_for_bins(variable: Numeric, bins: Optional[int] = None, agg: Aggregate = sum) -> tuple[Numeric, Numeric]:
    """
    variable  list/series of floats/integers
        interpreted as n samples of one numeric variable
    """
    variable.dropna(inplace=True)

    if bins is None:
        bins = 5

    if isinstance(bins, int):
        bins = np.linspace(min(variable), max(variable), bins + 1)

    rng = max(variable) - min(variable)

    bins[0] -= rng * .01

    aggs = [agg(variable.loc[(variable > bins[k]) & (variable <= bins[k + 1])]) for k in range(len(bins) - 1)]

    return aggs, bins   # list of agg values for each bin, list of bins borders


# %%  exactly the same in df.helpers
def sample(
        data: Data,
        n: int, shuffle: bool, random_state: int
) -> Union[pd.DataFrame, pd.Series]:
    """"""
    if n and n < len(data):
        data = data.sample(int(n), ignore_index=False, random_state=random_state)
    if shuffle:
        data = data.sample(frac=1, ignore_index=True, random_state=random_state)
    else:
        data = data.sort_index()  # it is usually original order (but not sure...)
    return data


# %%
def clip_transform(
        x: pd.Series,
        lower: Optional[float] = None,
        upper: Optional[float] = None,
        exclude: Optional[Sequence[float] | float] = None,
        transformation: Optional[bool | Transformation] = None,
        lower_t: Optional[float] = None,
        upper_t: Optional[float] = None,
        exclude_t: Optional[Sequence[float] | float] = None,
        transname: Optional[str] = "T",
) -> tuple[pd.Series, str | None]:
    """
    `x` is clipped to interval `[lower, upper]`
    then transformed and the result is clipped again to `[lower_t, upper_t]`.
    Additionally some values may be excluded:
    those from `exclude` before transformation
    and those from `exclude_t` after transformation.
    """
    if lower is not None:
        x = x[x >= lower]
    if upper is not None:
        x = x[x <= upper]
    if exclude is not None:
        x = x[~ x.isin(flatten([exclude]))]

    if transformation:

        if isinstance(transformation, bool):
            x, transformation = power_transformer(x)
        else:
            x = pd.Series(transformation(x))

        transname = transformation.__name__ or transname

        if lower_t is not None:
            x = x[x >= lower_t]
        if upper_t is not None:
            x = x[x <= upper_t]
        if exclude_t is not None:
            x = x[~ x.isin(flatten([exclude_t]))]
    else:
        transname = None

    return x, transname


# %%
def prepare_factor(
        x: pd.Series,
        most_common: int = 13,
        fillna: Optional[str] = '<NA>',
        sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
        ascending: Optional[bool] = None,
        precision: int = 3,
) -> tuple[pd.Series, pd.Series]:
    """
    Arguments
    ---------
    x : pd.Series
    most_common : int = 13,
        how many of the most common levels we want to consider
        later on (e.g. in plot_covariates()) to be taken into consideration;
        this limits the size of the value counts table:
        `x.value_counts()[:most_common]` see (*) in the code;
        notice that the `x` is then pruned to only these most common levels;
        if <= 1 then there is no selection of most common levels (all are left).
    fillna : Optional[str] = '<NA>',
        string which will replace all NAs (of any type: None, np.nan, ...);
        in case there are NAs in data they are all converted to `str`
        (because of problems with `ax.barh(labels_var, ...)` when `labels_var` are not of uniform type
         – v. strange indeed);
        pass `None` to not fill NAs – they will not appear in the resulting values table `x_vc`.
    sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
        when factor is plotted it's levels may be shown in one of three possible orders:
        - given in the factor definition (may be checked with `x.cat.categories`) – pass `None` the retain this order;
        - given by the levels (categories) frequency – pass "frequency" (or any starting sequence) for this order;
        - given by names of levels i.e. alphabetical order – pass "alphabetical" (or any starting sequence).
    ascending: Optional[bool] = None,
        when sorting factor levels we need to decide if the sorting should be ascending or descending;
        when left `None` (default) then direction of sorting is set according to type of sorting:
        - for sorting given by `x.cat.categories` `ascending` is set to True,
        - for frequency sorting `ascending` is set to False;
        - for alphabetical sorting `ascending` is set to True.
    precision: int = 3,
        nr of significant digits to factor level names which are obtained from floats;

    Returns
    -------
    x: pd.Series
        (factorised) variable
    x_vc: pd.Series
        `x.value_counts()[:most_common]` ordered according to `sort_levels` and `ascending`.
    """
    x = x.astype("category")    # idempotent; cats order preserved
    x = x.cat.remove_unused_categories()
    if x.isna().any() and fillna is not None:
        x = x.cat.add_categories([fillna]).fillna(fillna)

    #  necessary for numerics turned to factors:
    x = x.cat.rename_categories(str(adaptive_round(c, precision)) for c in x.cat.categories)
    # madness but other way (oneliner) None (and any other NAs) may end as 'None' category;
    # also, leaving numeric as numeric has bad effect on the look of axes

    x_vc = x.value_counts()     # frequency order, descending

    if most_common > 1 and most_common < len(x_vc):
        x_vc = x_vc.iloc[:most_common]

    if sort_levels is None:
        # order of categories – the same as is given by x.cat.categories (is it ordered or not is not important)
        ascending = coalesce(ascending, True)
        x_vc = x_vc.sort_index(ascending=ascending)
    elif 'frequency'.startswith(sort_levels):
        # this is default order of .value_counts()
        ascending = coalesce(ascending, False)
        x_vc = x_vc[::-1] if ascending else x_vc
    elif 'alphabetical'.startswith(sort_levels):
        ascending = coalesce(ascending, True)
        x_vc = x_vc[sorted(x_vc.index, reverse=not ascending)]
    else:
        raise Exception(
            "`sort_levels` must be one of 'frequency' or 'alphabetical' (or any starting sequence)\n"
            "or pass `None` to get order given by `x.cat.categories`."
        )

    x = x[x.isin(x_vc.index)].cat.remove_unused_categories()
    x = x.cat.reorder_categories(x_vc.index.tolist(), True)

    return x, x_vc


def to_factor(
        x: pd.Series,
        as_factor: Optional[bool] = None,
        factor_threshold: int = 13,
        most_common: int = 13,
        fillna: Optional[str] = '<NA>',
        sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
        ascending: Optional[bool] = None,
        precision: int = 3,
        factor_types: tuple[str, ...] = ("category", "object", "str", "datetime64[s]", "datetime64[ns]", "datetime64"),
) -> tuple[bool, pd.Series, pd.Series | None]:
    """
    Determining if the `x` is factor or not;
    if determined as factor its dtype is turned to 'category'.
    NaNs are treated as separate category.

    Arguments
    ---------
    x : pd.Series
    as_factor : bool | None = None,
        if not None then this is the value returned,
        i.e. x is forced to be factor or not;
        if None then decison is made automatically depending on the `x` type and `factor_threshold`.
    factor_threshold : int = 13,
        if `x` has less then `factor_threshold` unique values
        then it is assessed as factor.
    factor_types : tuple[str] = ("category", "object", "str", "datetime64[s]", "datetime64[ns]", "datetime64"),
        which data types to consider as factor types.

    The following parameters are passed to `prepare_fator()` – look there for help on them:

    most_common : int = 13,
    fillna : str = '<NA>',
    sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
    ascending: Optional[bool] = None,
    precision: int = 3,

    Returns
    -------
    as_factor: bool
    x: pd.Series
        (factorised) variable
    x_vc: pd.Series
        `x.value_counts()[:most_common]`
    """
    if as_factor is None:
        as_factor = x.dtype in factor_types
        if not as_factor and factor_threshold > 1:
            as_factor = x.unique().shape[0] < factor_threshold

    if as_factor:
        x, x_vc = prepare_factor(
            x, most_common=most_common, fillna=fillna,
            sort_levels=sort_levels, ascending=ascending, precision=precision
        )

    else:
        x_vc = None

    return as_factor, x, x_vc


# %%
def cats_and_colors(most_common: pd.Series, cmap: ColorMap | str) -> tuple[list[str], np.ndarray, ListedColormap]:
    """
    For categorical variable with given table of its most common values and frequencies
    (passed via `most_common` and obtained basically from `x.value_counts()[:most_common]`
     but here usually from `to_factor(..., most_common: int, sort_levels: ...)`
     which allows for sorting other then by frequency)
    returns
    - list of these most common categories (in the same order as in `most_common.index`),
    - list of colors for each of them and
    - ListedColormap derived from them.

    most_common: None; pd.Series
        table of most common value counts `= variable.value_counts[:most_common]`
        got from  to_factor(..., most_common: int)
    cmap: ColorMap | str
        matplotlib's ListedColormap, LinearSegmentedColormap or colormap name;
        for coloring wrt to categories of the categorical (levels of factor);

    Returns
    -------
    cats : categories (most common) of a factor
    cat_colors : list of colors of length `len(cats)`
    cmap : ListedColormap as defined in matplotlib
    """
    cats = most_common.index.tolist()
    #
    if isinstance(cmap, str):
        cmap = plt.colormaps[cmap]
    cat_colors = cmap(np.linspace(0.03, 0.97, len(cats)))
    cmap_ = ListedColormap(cat_colors)
    return cats, cat_colors, cmap_


# %%
def make_title(
        varname: str,
        lower: Optional[str | float] = None,
        upper: Optional[str | float] = None,
        transname: Optional[str] = None,
        lower_t: Optional[str | float] = None,
        upper_t: Optional[str | float] = None,
        tex: bool = False,
) -> str:
    """
    transname(varname_[lower, upper])_[lowetr_t, upper_t]

    varname : str
    lower : str | float | None = None,
    upper : str | float | None = None,
        lower/upper limit before transformation (if any)
    transname str | None = None,
        if str this string is taken as transformation name;
        if None then it's assumed that no transformation is done;
           then lower_t and upper_t are ignored;
    lower_t : str | float | None = None,
    upper_t : str | float | None = None,
        lower/upper limit after transformation (if any)
    tex: bool = False
        wheather or not the the final string will be processed by TeX;
    """
    if isinstance(varname, tuple):      # in case of MultiIndex
        varname = ".".join(varname)

    if not tex:
        varname = varname.replace("_", "\\_")

    if lower or upper:
        lower = f"[{lower}, " if lower else "(-\\infty, "
        upper = f"{upper}]" if upper else "\\infty)"
        lims = lower + upper
        #
        title = f"{varname}_{{{lims}}}"
    else:
        title = varname

    if transname is not None:
        if lower_t or upper_t:
            lower_t = f"[{lower_t}, " if lower_t else "(-\\infty, "
            upper_t = f"{upper_t}]" if upper_t else "\\infty)"
            lims_t = lower_t + upper_t
            #
            title = f"{transname}\\left(\\ {title}\\ \\right)_{{{lims_t}}}"
        else:
            title = f"{transname}\\left(\\ {title}\\ \\right)"

    return f"${title}$"


# %%
def style_affairs(
        style: Optional[str | bool],
        color: Optional[str | pd.Series],
        grid: Optional[bool | dict],
        axescolor: Optional[str],
        suptitlecolor: Optional[str],
        titlecolor: Optional[str],
        brightness: Optional[float],
        alpha: Optional[float | pd.Series],
        N: float,
) -> tuple[
        str | bool,
        str | pd.Series,
        dict[str, str | float] | bool,
        str,
        str,
        str,
        float,
        float | pd.Series]:
    """"""
    DARK_COLORS = ['black', 'gray', 'darkgrey']

    if style:
        if isinstance(style, str):
            plt.style.use(style)
        else:
            pass
            # use graphic params set externally
    else:
        style = 'dark_background'
        plt.style.use(style)

    if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
        brightness = 2.5 if brightness is None else brightness
    else:
        brightness = 1. if brightness is None else brightness

    if color is None:
        if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
            color = 'y'
        else:
            color = 'k'

    if grid:
        mpl.rc('axes', grid=True)
        if isinstance(grid, bool):
            if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
                grid = dict(color='darkgray', alpha=.3)
    else:
        grid = False

    if axescolor is None:
        if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
            axescolor = 'dimgray'
        else:
            axescolor = 'gray'
    mpl.rc('axes', edgecolor=axescolor)     # ?

    if titlecolor is None:
        if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
            titlecolor = 'gray'
            mpl.rc('axes', titlecolor=titlecolor)
        else:
            titlecolor = 'dimgray'
            mpl.rc('axes', titlecolor=titlecolor)

    if suptitlecolor is None:
        if mpl.rcParams['axes.facecolor'] in DARK_COLORS:
            suptitlecolor = 'lightgray'
        else:
            suptitlecolor = 'k'

    if alpha is None:
        # N = len(variable)
        a = 0.00023   # = m.log(10)/(1e4 - 1)
        alpha = max(m.exp(-a * (N - 1)), .05)

    return style, color, grid, axescolor, suptitlecolor, titlecolor, brightness, alpha


# %%
def set_xscale(ax: Axes, scale: str | tuple | dict) -> None:
    """setting the scale type on x axis
    scale may be str or tuple or dict
    each is passed to ax.set_scale() and unpacked (except str)
    hence the elements of `scale` must be as described in
    https://matplotlib.org/3.5.1/api/_as_gen/matplotlib.axes.Axes.set_xscale.html?highlight=set_xscale#matplotlib.axes.Axes.set_xscale
    https://matplotlib.org/3.5.1/api/scale_api.html#matplotlib.scale.ScaleBase
    etc.
    example:
    https://matplotlib.org/3.5.1/gallery/scales/scales.html#sphx-glr-gallery-scales-scales-py
    """
    if isinstance(scale, str):
        ax.set_xscale(scale)
    elif isinstance(scale, tuple):
        ax.set_xscale(*scale)
    elif isinstance(scale, dict):
        ax.set_xscale(**scale)


# %%
def set_yscale(ax: Axes, scale: str | tuple | dict) -> None:
    """setting the scale type on y axis
    scale may be str or tuple or dict
    each is passed to ax.set_scale() and unpacked (except str)
    ... see set_xscale()
    """
    if isinstance(scale, str):
        ax.set_yscale(scale)
    elif isinstance(scale, tuple):
        ax.set_yscale(*scale)
    elif isinstance(scale, dict):
        ax.set_yscale(**scale)


# %%
def set_grid(ax: Axes, off: AxisOff = "both", grid: Optional[bool | dict] = None) -> None:
    """
    off: "both" / "x" / "y"
        axis to be always turned off if not stated otherwise
    grid: False; bool or dict;
        if False then no grid is plotted (regardless of style);
        if True then grid is plotted as ascribed to given style;   !!! some styles do not print grid !
        in case of "black_background" it is dict(color='gray', alpha=.3)
        if dict then values from this dict will be applied as described in
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.grid.html
    """

    if grid:
        if not isinstance(grid, bool):
            ax.grid(**grid)
    else:
        second_axis = {"x": "y", "y": "x", "both": "both"}[off]
        ax.grid(visible=False, axis=cast(AxisOff, second_axis))

    if off != "both":
        ax.grid(visible=False, axis=off)


# %%
def set_title(ax: Axes, title: Optional[str], color: Optional[str]) -> None:
    """this is for axis (subplot) title
    """
    if title:
        if color:
            ax.set_title(title, color=color)
        else:
            ax.set_title(title)


def set_figtitle(
        fig: Figure,
        title: Optional[str],
        suptitlecolor: Optional[str],
        suptitlesize: float,
        fontweight: int | str = 'normal',
) -> None:
    """
    this is for the main figure title
    see https://matplotlib.org/stable/users/explain/text/text_props.html
    """
    if title:
        if suptitlecolor:
            fig.suptitle(title, fontweight=fontweight, color=suptitlecolor, fontsize=15 * suptitlesize)
        else:
            fig.suptitle(title, fontweight=fontweight, fontsize=15 * suptitlesize)


# %%
def horizontal_legend(ax: Axes, title: str, thresh: int, extra: int) -> Axes:
    """"""
    h, l = ax.get_legend_handles_labels()
    l_len = list(map(len, l))
    ncol = get_optimal_division(l_len, thresh=thresh, penalty=extra)[1]

    ax.legend(
        reorder(h, ncol), reorder(l, ncol), ncol=ncol,
        bbox_to_anchor=(.5, 0),
        loc='upper center',
        fontsize='small',
        title=title
    )
    return ax
