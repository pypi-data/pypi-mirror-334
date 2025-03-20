#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Diagnostic plots for one numeric variable
version: 1.0
type: module
keywords: [plot, numeric, continuous, histogram, density, distribution, cloud, boxplot,]
description: |
    Custom diagnostic plots for one numeric variable:
        - histogram
        - cloud
        - density
        - distribution
        - sum vs counts (wrt to groups from histogram)
        - boxplot
    Any configuration of the above types of plots are possible via `what` parameter.
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
from scipy.stats import gaussian_kde

# import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from .. import df as udf
from . import helpers as h

# plt.switch_backend('Agg')  # useful for pycharm debugging

from typing import cast, Any, Union, Iterable, Sequence, List, Tuple, Literal, Callable, Optional, MutableMapping
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]
Transformation = Callable[[Numeric], Numeric]
Aggregate = Callable[[Numeric], float]
PlotType = Literal["hist", "cloud", "density", "agg", "boxplot", "distr"]
ListPlotType = List[PlotType] | List[List[PlotType]] | NDArray[PlotType]  # type: ignore  # cannot be PlotType but it MUST be PlotType (and works!)  # noqa
Scale = Literal["linear", "log"]

ColorMap = Union[LinearSegmentedColormap, ListedColormap]


# %%
def plot_numeric(
        variable: str | Variable,
        data: Optional[pd.DataFrame] = None,
        stats: ListPlotType = cast(ListPlotType, [["hist", "cloud", "density"], ["agg", "boxplot", "distr"]]),
        what: ListPlotType = cast(ListPlotType, []),
        varname: Optional[str] = None,
        title: Optional[str] = None, title_suffix: Optional[str] = None,
        # Variable modifications (before plotting)
        # # transformations
        lower: Optional[float] = None, upper: Optional[float] = None,
        exclude: Optional[Sequence[float] | float] = None,
        transform: Optional[bool | Transformation] = None,
        lower_t: Optional[float] = None, upper_t: Optional[float] = None,
        exclude_t: Optional[Sequence[float] | float] = None,
        # # histogram
        bins: int | List[float] = 7, agg: Aggregate = sum,
        # # sampling
        n_obs: int = int(1e4),
        shuffle: bool = False, random_state: int = 2222,
        extremes: Optional[int | float] = .02,
        # Graphical parameters
        # # Figure and axes parameters
        # ## for the whole figure
        figsize: Optional[Tuple[float, float]] = None,
        figwidth: Optional[float] = None, figheight: Optional[float] = None,
        suptitlecolor: Optional[str] = None, suptitlesize: float = 1.,  # multiplier of 15
        # ## for separate axes (subplots) but for all of them
        width: Optional[float] = None, height: Optional[float] = None,
        size: float = 5, width_adjust: float = 1.2,
        scale: Scale = "linear",
        style: str | bool = True, grid: bool | dict = True,
        axescolor: Optional[str] = None,
        titlecolor: Optional[str] = None,
        # # elements and attributes of plots (artists)
        lines: bool = True,
        cmap: str | ColorMap = "ak01",  # 'hsv'; for coloring wrt to categories of the categorical (levels of factor);
        color: Optional[str | pd.Series] = None,
        s: int | str | pd.Series = 9,
        alpha: Optional[float | str | pd.Series] = None,
        brightness: Optional[float] = None,  # ! TODO  # alpha, size and brightness of a data point in a "cloud"
        ignore_index: bool = False,
        # Output
        print_info: bool = True, res: bool = False,
        *args: Any, **kwargs: Any
) -> Optional[MutableMapping]:
    """
    Remarks:
        - `style` is True by default what means using style set up externally
          and it is assumed to be set to  plt.style.use('dark_background');
        - All default graphic parameters are set for best fit
          with 'dark_background' style.
        - Unfortunately changing styles is not fully reversible, i.e.
          some parameters (plt.rcParams) stays changed after reverting style;
          (eg. grid stays white after 'ggplot',
          the same for title colors after 'black_background', etc);
          Just because of this there are some parameters like `color`, `grid`, `titlecolor`
          to set up their values by hand in case of unwanted "defaults".

    Basic params
    ------------
    variable: str or pd.Series;
        if `str` then it indicates column of `data`;
        else `pd.Series` of data to be plotted;
    data: None; pd.DataFrame;
        if None then `variable` must be `pd.Series` with data to plot;
    stats: [['hist', 'cloud'], ['boxplot', 'density'], ['agg', 'distr']]; list (of lists);
        the whole list reflects the design of the whole final figure where
        each sublist represents one row of plots (axes) within a figure
        and each element of a sublist is the name of the respective plot type
        which will be rendered in a respective subplot (axis) of the figure;
        thus each sublist should be of the same length however...
        possible values of the elements of the sublist (types of the plots) are:
            "hist", "cloud", "dist", "density", "agg", "boxplot", "blank" (for empty subplot);
    what: []; list (of lists);
        alias for `stats` for backward compatibility;
    varname: Optional[str] = None,
        variable name to be used in title, etc.; if None then taken from
        .name attr of `variable`;
    title: Optional[str] = None,
        title of a plot; if None then generated automaticaly;
    title_suffix: Optional[str] = None,
        makes possible to distinguish plots for which automatic title would be the same;

    Variable modifications (before plotting)
    ----------------------------------------

    # transformations

    lower: Optional[float] = None,
        lower limit of `variable` to be plotted; inclusive !
        if None then `lower == min(variable)`
    upper: Optional[float] = None,
        upper limit of `variable` to be plotted; inclusive !
        if None then `upper == max(variable)`
    exclude: Optional[Sequence[float] | float] = None,
        values to be excluded from `variable` before plotting;
    transform: Optional[bool | Transformation] = None,
        if None or False no transformation is used;
        if True then Yeo-Johnson transformation is used with automatic parameter;
        if function is passed then this function is used;
    lower_t: Optional[float] = None,
        lower limit of transformed `variable` to be plotted; inclusive !
        if None then `lower_t == min(T(variable))`
    upper_t: Optional[float] = None,
        upper limit of transformed `variable` to be plotted; inclusive !
        if None then `upper_t == max(T(variable))`
    exclude_t: Optional[Sequence[float] | float] = None,
        values to be excluded from transformed `variable` before plotting;

    # histogram

    bins: int | List[float] = 7,
        how many or what bins (groups)
        if integer then how many bins for for "hist" (histogram) and "agg" subplots;
        if list of floats then these are boarders of bins;
        ii is passed to `ax.hist(...)` or `numpy.histogram(...)` and has exactly the same meaning;
    agg: Callable[[Numeric], float] = sum,
        type of aggregate for "agg" plot where for each group from "hist"
        we plot point (having the same color as respective bar of "hist")
        with coordinates `(count, agg)` where `count` is nr of elements in a group
        and `agg` is aggregate of values for this group.

    # sampling

    n_obs: int = int(1e4),
        if not None then maximum nr of observations to be sampled from variable before plotting
        'cloud', 'density', 'distr';
        if None whole data will be plotted (what is usually not sensible for very large data).
    shuffle: bool = False,
        shuffle data before plotting – useful only for "cloud" plot in case
        when data are provided in clumps with different statistical properties;
        shuffling helps to spot distribution features common to the whole data.
    random_state: int = 2222,
        passed to numpy random generator for reproducibility in case of
        `n_obs` is not None or `shuffle` is True;
    extremes: Optional[int | float] = .02,
        in not 0 or None then this is number of extreme values to be sampled;
        when float then it means portion of `n_obs`;

    Graphical parameters
    --------------------

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

    ## for separate axes (subplots) but for all of them

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
    scale: Scale = "linear",
        scale of the x axe for all the subplots;
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

    lines: bool = True;                            # ! TODO
        lines for 'cloud', 'boxplot', 'density' and 'distr' which are put in the same places
        as limits of bins of the histogram ("hist" subplot);
    cmap: str | ColorMap = "ak01",
        matplotlib's ListedColormap, LinearSegmentedColormap or colormap name;
        for coloring histogram bars "hist";
        "hsv" is a popular choice however it has uneaven luminosity;
        see https://matplotlib.org/stable/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py
        or dir(matplotlib.pyplot.cm) for list of all available color maps;
        see https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html#creating-colormaps-in-matplotlib
        on how to create and register ListedColormaps.
    color: Optional[str | pd.Series] = None,
        color of lines and points for 'cloud', 'boxplot', 'density' and 'distr';
        if None then set to "yellow" for style "black_background", else to "black";
    s: int | str | pd.Series = 9,
        size of a data point in a "cloud"
        if str and `data` is not None then it is interpreted as a name of a column in `data`
        where sizes of data point are stored;
        if `pd.Series` then must be of the same length as `variable`, `covariate` or `data` and stores
        size value for each data point;
    alpha: Optional[float | str | pd.Series] = None,
        float between 0 and 1; for points of "cloud" only;
        if None then set automatically according to `n_obs`;
        if str and `data` is not None then it is interpreted as a name of a column in `data`
        where alphas for data points are stored;
        if `pd.Series` then must be of the same length as `variable`, `covariate` or `data` and stores
        alpha value for each data point;
    brightness: Optional[float] = None,              # ! TODO
    ignore_index: bool = False,
        `variable`, `color`, `s`, `alpha` may be passed as `pd.Series` and if `ingnore_index` is True
        then index of these series is ignored and they are aligned to series of `variable`
        only positionally (thus must be of the same length);

    Output
    ------

    print_info: bool = True,
        print df.info(variable) (after all transformations)
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
            "cloud": {
                "ax": <Axes objects>,
                "result": <data plotted>
                }
            <
              other subplot objects under respective keys as called for by `stats` / `what`
              with keys like "axes", "result", "agg" ... (depending on the plot type);
            >
            ...
            "axs": array([[<Axes: >, <Axes: >], [<Axes: >, <Axes: >]], dtype=object)     # example
                # in general: axs.shape == stats.shape;
                # ! "axs" is porobably spurious as all the axes are already available under "ax" key
                # of respecitve subplot entries like "cloud", "hist", ...
            "fig": <Figure of a plot>
            }
    }

    """

    # -------------------------------------------------------------------------
    #  loading data

    variable, varname = h.get_var_and_name(variable, data, varname, "X")

    # !!! index is ABSOLUTELY CRITICAL here !!!
    if ignore_index:
        variable, color, s, alpha = udf.align_indices(variable, color, s, alpha)

    # -----------------------------------------------------
    #  info on raw variable
    info_raw = udf.info(pd.DataFrame(variable), stats=["dtype", "oks", "oks_ratio", "nans_ratio", "nans", "uniques"])

    if print_info:
        print(" 1. info on raw variable")
        print(info_raw)

    # -------------------------------------------------------------------------
    #  preparing data

    variable = variable.dropna()

    # -----------------------------------------------------
    #  transformation and clipping

    variable, transname = h.clip_transform(
        variable, lower, upper, exclude,
        transform, lower_t, upper_t, exclude_t, "T"
    )

    # -----------------------------------------------------
    #  statistics for processed variable

    info_proc = udf.summary(
        pd.DataFrame(variable),
        stats=["oks", "uniques", "most_common", "most_common_ratio", "most_common_value", "dispersion"])

    summary_proc = udf.summary(
        pd.DataFrame(variable),
        stats=["range", "iqr", "mean", "median", "min", "max", "negatives", "zeros", "positives"])

    if print_info:
        print()
        print(" 2. statistics for processed variable (on the plot)")
        print(info_proc)
        print()
        print(summary_proc)

    # -----------------------------------------------------
    #  title

    if not title:
        title = h.make_title(varname, lower, upper, transname, lower_t, upper_t)

    if title_suffix:
        title = title + title_suffix

    # -----------------------------------------------------

    counts = None
    aggs = None

    # ----------------------------------------------------
    # !!! result !!!

    result = {
        "title": title,                 # title of the plot (suptitle)
        "variable": variable,           # processed – after all prunings and transformations
        "info": info_raw,               # info on raw data
        "variation": info_proc,         # statistics for processed variable
        "distribution": summary_proc,   # more statistics for processed data
        "plot": dict()
    }

    # -------------------------------------------------------------------------
    #  style affairs

    N = len(variable) if not n_obs else min(len(variable), int(n_obs))

    # !!! get  color, s, alpha  from data if they are proper column names !!!

    if isinstance(alpha, str):
        alpha = data[alpha]

    if isinstance(s, str):
        s = data[s]

    # take color from data only if it's not a color name
    if isinstance(color, str) and not h.is_mpl_color(color) and color in data.columns:
        color = data[color]

    color_data = color
    if not isinstance(color, str) and isinstance(color, Iterable):
        color = None

    style, color, grid, axescolor, suptitlecolor, titlecolor, brightness, alpha = \
        h.style_affairs(style, color, grid, axescolor, suptitlecolor, titlecolor, brightness, alpha, N)

    if color_data is None:
        color_data = color

    # ---------------------------------------------------------------------------------------------
    #  plotting

    if isinstance(cmap, str):
        cmap = plt.colormaps[cmap]

    len_bins = len(bins) - 1 if isinstance(bins, list) else bins
    colors = cmap(np.linspace(0.1, 0.9, len_bins))

    # -------------------------------------------------------------------------
    #  plot types

    def hist(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        nonlocal bins
        nonlocal counts

        # counts, bins, patches = ax.hist(variable, bins=bins)
        # for p, c in zip(patches.patches, colors):
        #     p.set_color(c)

        counts, bins = np.histogram(variable, bins=bins)
        labels = [str(b) for b in range(1, len(bins))]
        bars = ax.bar(labels, counts, color=colors)  # edgecolor='y',
        for p in bars.patches:
            p.set_width(.97)

        #  ---------
        # ax.set_xscale(scale)                  # ???
        h.set_grid(ax, off="x", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        result = dict(counts=counts, bins=bins, bars=bars)  # patches=patches)
        return dict(ax=ax, result=result)

    def agg_vs_count(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        nonlocal bins
        nonlocal counts
        nonlocal aggs
        if counts is None:
            counts, bins = np.histogram(variable, bins=bins)
        aggs, bins = h.agg_for_bins(variable, bins, agg)
        scatter = ax.scatter(
            counts, aggs,
            s=50, color=colors, marker="D")
        #  ---------
        h.set_xscale(ax, scale)
        h.set_yscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        result = dict(aggs=aggs, bins=bins, scatter=scatter)
        return dict(ax=ax, result=result)

    def boxplot(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        # ---------
        result = ax.boxplot(
            variable,
            vert=False,
            notch=True,
            #
            patch_artist=True,                              # !!!
            boxprops=dict(color=color, facecolor=color),
            whiskerprops=dict(color=color),
            capprops=dict(color=color),
            flierprops=dict(color=color, markeredgecolor=color, marker="|"),
            medianprops=dict(color='gray' if color in ['k', 'black'] else 'k'),
            #
            showmeans=True,
            # meanline=False,
            meanprops=dict(  # color='white' if color in ['k', 'black'] else 'k',
                             marker="d",
                             markeredgecolor=color,
                             markerfacecolor='white' if color in ['k', 'black'] else 'k', markersize=17))
        # ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="y", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        return dict(ax=ax, result=result)

    def density(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        # ---------
        try:
            density = gaussian_kde(variable.astype(float))
        except Exception:
            density = gaussian_kde(variable)
        xx = np.linspace(min(variable), max(variable), 200)
        lines = ax.plot(xx, density(xx), color=color)  # list of `.Line2D`
        # ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        result = dict(xx=xx, lines=lines)
        return dict(ax=ax, result=result)

    def cloud(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        # ---------
        result = ax.scatter(variable, range(len(variable)), s=s, color=color_data, alpha=alpha)
        # ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        return dict(ax=ax, result=result)

    def distr(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        # # line version
        # result = ax.plot(*h.distribution(variable), color=color, linewidth=1)
        # dots version
        result = ax.scatter(*h.distribution(variable), s=.5, color=color_data)
        # `~matplotlib.collections.PathCollection`
        #  ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        # set_axescolor(ax, axescolor)
        #
        return dict(ax=ax, result=result)

    def blank(ax, title="", text="", *args, **kwargs):
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        ax.plot()
        ax.axis('off')
        ax.text(
            0.5, 0.5, text,
            verticalalignment='center', horizontalalignment='center',
            transform=ax.transAxes,
            color='gray', fontsize=10)
        return dict(ax=ax, result=False)

    def error(ax, title=None):
        """"""
        h.set_title(ax, title, titlecolor)
        #  --------
        ax.plot()
        ax.axis('off')
        ax.text(
            0.5, 0.5, 'unavailable',
            verticalalignment='center', horizontalalignment='center',
            transform=ax.transAxes,
            color='gray', fontsize=10)
        return dict(ax=ax, result=False)

    PLOTS = {
        "hist": {"plot": hist, "name": "histogram"},
        "boxplot": {"plot": boxplot, "name": "box-plot"},
        "agg": {"plot": agg_vs_count, "name": f"{agg.__name__} vs count"},
        "cloud": {"plot": cloud, "name": "cloud"},
        "density": {"plot": density, "name": "density"},
        "distr": {"plot": distr, "name": "distribution"},
        "blank": {"plot": blank, "name": ""},
        "error": {"plot": error, "name": "error"},
    }

    # ------------------------------------------------------------------------
    #  plotting procedure

    # -----------------------------------------------------
    #  figure and plots sizes
    stats = what or stats
    stats = np.array(stats, ndmin=2)
    nrows = stats.shape[0]
    ncols = stats.shape[1]

    if figsize is None:

        if figheight is None:
            height = height or size
            figheight = height * nrows + 1     # ? +1 ?

        if figwidth is None:
            width = width or size * width_adjust
            figwidth = width * ncols

        figsize = figwidth, figheight

    # ----------------------------------------------------
    #  core

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axs = np.reshape(axs, (nrows, ncols))    # unfortunately it's necessary because ...

    for t in ["hist", "boxplot", "agg", "blank"]:
        if t in stats:
            ax = axs[np.nonzero(stats == t)][0]
            try:
                result['plot'][t] = PLOTS[t]["plot"](ax, PLOTS[t]["name"])
            except Exception as e:
                print(e)
                result['plot'][t] = PLOTS["error"]["plot"](ax, PLOTS[t]["name"])

    variable = udf.sample(variable, n_obs, shuffle, random_state, extremes)
    variable, color, s, alpha, color_data = \
        udf.align_nonas(variable, color=color, s=s, alpha=alpha, color_data=color_data)

    for t in ["cloud", "density", "distr"]:
        if t in stats:
            ax = axs[np.nonzero(stats == t)][0]
            try:
                result['plot'][t] = PLOTS[t]["plot"](ax, PLOTS[t]["name"])
                if lines and not isinstance(bins, int):
                    for l, c in zip(bins, np.vstack([colors, colors[-1]])):
                        ax.axvline(l, color=c, alpha=.3)
            except Exception as e:
                print(e)
                result['plot'][t] = PLOTS["error"]["plot"](ax, PLOTS[t]["name"])

    result['plot']['axs'] = axs

    # -------------------------------------------------------------------------
    #  final

    if print_info:
        print()
        if isinstance(bins, Iterable):
            print("  For histogram groups:")
            #
            print("bins: [", end="")
            print(", ".join(f"{b:.2g}" for b in bins), end="")
            print("]")
        #
        if aggs:
            print(f"counts: {counts}")
            aggs_rounded = [round(a) for a in aggs]
            print(f"{agg.__name__}: {aggs_rounded}")

    h.set_figtitle(fig, title, suptitlecolor, suptitlesize)

    fig.tight_layout()
    # plt.show()

    result['plot']["fig"] = fig

    return None if not res else result


# %% alias
plot_num = plot_numeric
