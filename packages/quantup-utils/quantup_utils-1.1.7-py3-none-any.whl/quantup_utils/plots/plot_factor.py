#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Diagnostic plots for one variable
version: 1.0
type: module
keywords: [plot, factor, categorical, barplot]
description: |
    Custom diagnostic plots for one categorical (factor) variable:
        - barplot.
    Maximum flexibility (lots of parameters) but with sensible defaults.
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

# import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from .. import df as udf
from . import helpers as h

# plt.switch_backend('Agg')  # useful for pycharm debugging

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

# ColorMap = Union[LinearSegmentedColormap, ListedColormap]


# %%
def plot_factor(
        variable: str | Variable,
        data: Optional[pd.DataFrame] = None,
        varname: Optional[str] = None,
        title: Optional[str] = None, title_suffix: Optional[str] = None,
        # Variable modifications (before plotting)
        # # transformations
        fillna: Optional[str] = '<NA>',
        sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
        ascending: Optional[bool] = None,
        # # sampling
        most_common: int = 13,
        # Graphical parameters
        # ## for the whole figure
        figsize: Optional[Tuple[float, float]] = None,
        figwidth: Optional[float] = None, figheight: Optional[float] = None,
        suptitlecolor: Optional[str] = None, suptitlesize: float = 1.,  # multiplier of 15
        # ## for the axis (subplot)
        width: Optional[float] = None, height: Optional[float] = None,
        size: float = 5, width_adjust: float = 1.2,
        barwidth: float = .5,
        scale: Scale = "linear",
        style: str | bool = True, grid: bool | dict = True,
        axescolor: Optional[str] = None,
        titlecolor: Optional[str] = None,
        # # elements and attributes of plots (artists)
        color=None,     # ???
        horizontal: Optional[bool] = None,
        labelrotation: float = 75.,
        # Output
        print_info: bool = True,
        print_levels: bool = False,  # prints all levels regardless of `most_common`
        precision: int = 3,
        res: bool = False,
        *args, **kwargs
) -> Optional[MutableMapping]:
    """
    Remarks
    -------
    - Currently the only plot type for factor variable is "barplot" visualising number of each factor level
      (unique category value); thus there is only one axis (subplot) in the figure (using matplotlib terminology)
      unlike fot the `plot_numeric()` where there are 6 possible plot types each having separate axis;
    - May be used also for numerics (but be careful when they have a lot of different values).
    - `most_common` applied before `sort_levels` -- good!

    Basic params
    ------------
    variable: str or pd.Series;
        if `str` then it indicates column of `data`;
        else `pd.Series` of data to be plotted;
    data: None; pd.DataFrame;
        if None then `variable` must be `pd.Series` with data to plot;
    varname: Optional[str] = None,
        variable name to be used in title, etc.; if None then taken from
        .name attr of `variable`;
    title: Optional[str] = None,
        title of a plot; if None then generated automaticaly;
    title_suffix: Optional[str] = None,
        makes possible to distinguish plots for which automatic title would be the same;

    Variable modifications (before plotting)
    ----------------------------------------

    fillna: Optional[str] = '<NA>',
        string for filling NA values (None, np.nan, ...) for categorical data (only!);
        this allows to include them into data as one of the categories (levels) thus they appear on the plot
        – usually better option as provides more information (yet it's impossible for numeric variables);
        passing `None` will leave NA values unchanged thus they will be removed before making plot.
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
    most_common: int = 13,
        if <= 1 then all bars for all factor levels will be plotted;
        this is dangerous if not sure how many levels there are;
        it's better to set big integer but no bigger then 100;
        otherwise plot may not be rendered at all if there are thousands of levels;
        `most_common` is applied before `sort_levels`.

    Graphical parameters
    --------------------
    Currently there is only one plot in a figure for factors.
    It means that fig-size params are spurious but they are kept for
    consistency with plot_numeric() and for future development
    (other then bars plots for factors).

    # figure and axes parameters

    ## for the whole figure
    If `figsize`, `figwidth`, `figheight` are None then they are calculated based on sizes of a single subplot (axis)
    which are set directly via `width` and `height` or indirectly from `size` and `width_adjust` params.
    Otherwise `figsize` overrides `figwidth`, `figheight` and they in turn override all the other size params.
    Notice that "the other" params, especially `size` and `width_adjust` do not work perfectly
    when translating them into figure size so some experimantation may be necessary to achive desired look of a plot.

    figsize: Optional[Tuple[float, float]] = None,
        `(width, height)` passed to `plt.figure(figsize=.)`;
    figwidth: Optional[float] = None,
        if `figsize` is None then it is created from `figwidth` and `figheight`;
    figheight: Optional[float] = None,
        if `figsize` is None then it is created from `figwidth` and `figheight`;
    suptitlecolor: Optional[str] = None,
        color of the whole title plot (`fig.suptitle`)
        if None then set automatically according to style;
    suptitlesize: float = 1.,
        multiplier of 15 for the whole title plot (`fig.suptitle`)

    ## for the axis (subplot)

    width: Optional[float] = None,
        width of a single subplot (axis);
    height: Optional[float] = None,
        height of a single subplot (axis);
    size: float = 5,
        if `width` or `height` are None then they are calculated from `size` and `width_adjust` roughly like:
            height = size
            width = size * width_adjust
    width_adjust: float = 1.2,
        see help on `size`;
    barwidth : .5; numeric
        width of the single bar;
        if not None then width of the final plot is dependent on the number of levels
        and equals to `barwidth * nr_of_levels`;
    scale: Scale = "linear",
        scale for the values (length) of bars;
        possible values are "linear" and "log";
    style: True; bool or str
        if True takes all the graphic parameters set externally (uses style from environment);
        if False then is set to "dark_background";
        str must be a name of one of available styles: see `plt.style.available`.
        set style via `plt.style.use("style_name")` e.g. `plt.style.use("ggplot")`.
    grid: False; bool or dict;
        if False then no grid is plotted (regardless of style);
        if True then grid is plotted as ascribed to given style;
        in case of "black_background" it is dict(color='gray', alpha=.3)
        if dict then values from this dict will be applied as described in
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.grid.html
        Most general form (example values):
        { 'alpha': 1.0,  'color': '#b0b0b0',  'linestyle': '-',  'linewidth': 0.8  }
    axescolor: Optional[str] = None,
        color of the main axes (or rather the frame) of the subplot;
        if None then set automatically according to style;
    titlecolor: Optional[str] = None,
        color of axes titles;
        if None then set automatically according to style;

    # elements and attributes of plots (artists)

    color : None; str
        color of lines for edge of bars;
        if None then set to "yellow" for style "black_background", else to "black";
    horizontal: Optional[bool] = None,
        if True then bars are horizontal; otherwise they are vertical;
        if None (default) then it set to True if there is less then 10 distinct levels;
        otherwise is set to False.
    labelrotation: float = 75.,
        in case of vertical bars level names are usually to long to be printed horizontally
        (as normal text) as they overlap;
        thus they are rotated `labelrotation` degrees from horizontal line, i.e.
        if set to 90 they are printed vertically;

    Output
    ------

    print_info: bool = True,
        print df.info(variable) (after all transformations)
    print_levels: bool = False,
        if True prints all levels regardless of `most_common`
        what is "dangerous" in case of large number of levels;
    precision: int = 3,
        precision of floats as variable levels; more or less significant digits (however only for fractions);
        when turning numeric float variable into factor (makes sense when there are only few distinct values)
        then it's better to round the values to get nice factor level lables;
    res: bool = False,
        do return result of all the calculations?
        default is False and then None is returned;
        otherwise (if True) dictionary is returned with the following structure:

    Returns
    -------
    If required (`res=True`) it is dictionary "of everything":

    result = {
        "title": title,                 # title of the plot (suptitle)
        "variable": variable,           # processed – after all prunings and transformations
        "info": info_raw,               # info on raw data
        "variation": info_proc,         # statistics for processed variable
        "distribution": summary_proc,   # more statistics for processed data
        "plot": {           # plot objects
            "barplot": {
                "ax": <Axes objects>,
                "bars": <data plotted>,
                }
            < currently there are no other subplot objects but they are possible in the future >
            "fig": <Figure of a plot>
            }
    }

    """
    # -----------------------------------------------------
    variable, varname = h.get_var_and_name(variable, data, varname, "X")

    # -----------------------------------------------------
    #  info on raw variable
    var_info = udf.info(pd.DataFrame(variable), stats=["dtype", "oks", "oks_ratio", "nans_ratio", "nans", "uniques"])

    # -------------------------------------------------------------------------
    #  preparing data
    variable, variable_vc = h.prepare_factor(
        variable, most_common=most_common, fillna=fillna,
        sort_levels=sort_levels, ascending=ascending, precision=precision
    )
    levels = variable_vc.index.tolist()
    n_levels = len(levels)
    counts = variable_vc.values.tolist()

    if most_common and most_common < n_levels:
        most_common_info = f"(most common {most_common} levels)"
        if title is None:
            title = f"{varname} \n most common {most_common} of {n_levels} values"  # ! 2 lines !
        levels_info_header = f" {varname} " + most_common_info
    else:
        most_common = n_levels
        most_common_info = f"(all {n_levels} levels)"
        if title is None:
            title = varname
        levels_info_header = f" {varname} " + most_common_info

    if title_suffix:
        title = title + title_suffix

    var_variation = udf.info(
        pd.DataFrame(variable),
        stats=["oks", "uniques", "most_common", "most_common_ratio", "most_common_value", "dispersion"])

    if print_info:
        print(" 1. info on raw variable")
        print(var_info)
        print()
        print(" 2. statistics for processed variable " + most_common_info)
        print(var_variation)
        print()

    if print_levels:
        # printing all levels is "dangerous" (may be a lot of them) and it's out of this function scope
        print(levels_info_header)
        print(variable_vc)

    # ----------------------------------------------------
    #  !!! result !!!

    result = {
        "title": title,
        "variable": variable,
        "info": var_info,
        "variation": var_variation,
        "distribution": variable_vc,  # variable after all prunings and transformations
        "plot": dict(),
    }

    # ---------------------------------------------------------------------------------------------
    #  plotting

    # -------------------------------------------------------------------------
    #  style affairs

    style, color, grid, axescolor, suptitlecolor, titlecolor, _brightness, alpha = \
        h.style_affairs(style, color, grid, axescolor, suptitlecolor, titlecolor, None, None, len(variable))

    # -------------------------------------------------------------------------
    #  sizes
    if figsize is None:

        n = min(most_common, n_levels)

        if figheight is None:
            height = size if height is None else height
            figheight = height

        if figwidth is None:
            if barwidth:
                width = barwidth * n if width is None else width
            else:
                width = size * width_adjust if width is None else width
            figwidth = width

        if horizontal is None:
            horizontal = len(levels) < 10

        if horizontal:
            figsize = figheight, figwidth + .8 * n / (n + 2)
            #
            levels = levels[::-1]
            counts = counts[::-1]
        else:
            figsize = figwidth, figheight

    fig, ax = plt.subplots(figsize=figsize)

    # -------------------------------------------------------------------------
    #  plot

    if horizontal:
        bars = ax.barh(levels, counts, edgecolor=color, color='darkgray')
        #  ----------------------------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="y", grid=grid)
        # h.set_axescolor(ax, axescolor)
    else:
        bars = ax.bar(levels, counts, edgecolor=color, color='darkgray')
        #  ----------------------------
        h.set_yscale(ax, scale)
        h.set_grid(ax, off="x", grid=grid)
        # h.set_axescolor(ax, axescolor)
        ax.tick_params(axis='x', labelrotation=labelrotation)

    result['plot']['barplot'] = dict(ax=ax, bars=bars)

    # -----------------------------------------------------
    #  final

    h.set_figtitle(fig, title, suptitlecolor, suptitlesize)

    fig.tight_layout()
    # plt.show()

    result['plot']["fig"] = fig

    return None if not res else result


# %% alias
plot_cat = plot_factor
