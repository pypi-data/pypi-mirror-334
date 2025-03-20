#! python3
# -*- coding: utf-8 -*-
"""
---
title: Variable (y) vs covariate (x)
version: 1.0
type: module
keywords: [plot, covariates, variable, categorical, numeric, ...]
description: |
remarks:
todo:
    - categorical ~ numeric  may be shown via multinomial logistic model,
      i.e. probability of each category wrt to value of x;
    - violinplots  for  numeric ~ factor (~432);
    - factor ~ factor (~695)  is in very crude version;
    - barchart (~475): legend (bbox_to_anchor, loc, ...);
      figure size for large amount of levels and long level names;
    -
sources:
"""

# %%
import logging

import numpy as np
import pandas as pd

import statsmodels.api as sm   # type: ignore
from scipy.stats import gaussian_kde   # type: ignore

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes, Figure
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from .. import df as udf
from . import helpers as h

from typing import cast, Any, Union, Iterable, Sequence, List, Tuple, Literal, Callable, Optional, \
    MutableMapping, TypedDict
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]
Transformation = Callable[[Numeric], Numeric]
Aggregate = Callable[[Numeric], float]
PlotType = Literal["cloud", "grouped_cloud", "densities", "boxplots", "distr", "barchart", "blank"]
ListPlotType = List[PlotType] | List[List[PlotType]] | NDArray[PlotType]  # type: ignore  # cannot be PlotType but it MUST be PlotType (and works!)  # noqa
Scale = Literal["linear", "log"]

ColorMap = Union[LinearSegmentedColormap, ListedColormap]

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# %% plot_()
def plot_covariates(
        variable: str | Variable,
        covariate: str | Variable,
        data: Optional[pd.DataFrame] = None,
        stats: ListPlotType = cast(ListPlotType, ["grouped_cloud", "densities", "boxplots"]),
        what: ListPlotType = cast(ListPlotType, []),
        varname: Optional[str] = None, covarname: Optional[str] = None,
        title: Optional[str] = None, title_suffix: Optional[str] = None,
        ignore_index: bool = False,
        as_factor_y: Optional[bool] = None, as_factor_x: Optional[bool] = None,
        factor_threshold: int = 13,
        # Variables modifications (before plotting)
        # # transformations
        lower_y: Optional[float] = None, upper_y: Optional[float] = None,
        exclude_y: Optional[Sequence[float] | float] = None,
        lower_x: Optional[float] = None, upper_x: Optional[float] = None,
        exclude_x: Optional[Sequence[float] | float] = None,
        transform_y: Optional[bool | Transformation] = None,
        transform_x: Optional[bool | Transformation] = None,
        lower_t_y: Optional[float] = None, upper_t_y: Optional[float] = None,
        exclude_t_y: Optional[Sequence[float] | float] = None,
        lower_t_x: Optional[float] = None, upper_t_x: Optional[float] = None,
        exclude_t_x: Optional[Sequence[float] | float] = None,
        fillna: Optional[str] = '<NA>',   # filling NA values (None, np.nan, ...) for categorical (only!)
        sort_levels: Optional[Literal['frequency', 'alphabetical']] = 'frequency',
        ascending: Optional[bool] = None,
        # # sampling
        n_obs: int = int(1e4),
        shuffle: bool = False, random_state: int = 2222,
        extremes: Optional[int | float] = .02,
        most_common: int = 13,  # for categorical
        # Graphical parameters
        # # Figure and axes parameters
        # ## for the whole figure
        figsize: Optional[Tuple[float, float]] = None,
        figwidth: Optional[float] = None, figheight: Optional[float] = None,
        suptitlecolor: Optional[str] = None, suptitlesize: float = 1.,  # multiplier of 15
        # ## for separate axes (subplots) but for all of them
        width: Optional[float] = None, height: Optional[float] = None,
        size: float = 5, width_adjust: float = 1.2,
        scale: Scale = "linear", xscale: Optional[Scale] = None, yscale: Optional[Scale] = None,
        style: str | bool = True, grid: bool | dict = True,
        axescolor: Optional[str] = None,
        titlecolor: Optional[str] = None,
        # # elements and attributes of plots (artists)
        lines: bool = True,  # ! TODO
        cmap: str | ColorMap = "ak01",  # 'hsv'; for coloring wrt to categories of the categorical (levels of factor);
        # ## data point
        color: Optional[str | pd.Series] = None,
        s: int | str | pd.Series = 9,
        alpha: Optional[float | str | pd.Series] = None,
        brightness: Optional[float] = None,  # ! TODO  # alpha, size and brightness of a data point in a "cloud"
        # ## other parameters for various types of plots
        bins: int | List[float] = 21, smooth: float = .5,
        qq_plot: bool = False,       # add qq-plot for  num ~ num  plot
        legend: bool = True, axes_labels: bool = True,
        # ## only fac~fac
        bar_height: float = .9, align: bool = True, horizontal: bool = True, print_counts: bool = True,
        # Output & text
        tex: bool = False,  # varname & covarname passed in TeX format e.g. "\\hat{Y}" (double`\` needed)
        print_info: bool = True, print_levels: bool = False,  # prints all levels regardless of `most_common`
        precision: int = 3,
        use_logger: bool = False,
        res: bool = False,
        *args: Any, **kwargs: Any
) -> Optional[MutableMapping]:
    """
    What is the dependence of a variable (y) on the covariate (x)?
    Symbolically `y ~ x` or `y vs x`.
    There are 4 cases:
        (y is numeric | categorical) ~ (x is numeric | categorial)  or in short
        (y is num | cat) ~ (x is num | cat)
    but cat ~ num is always turned to num ~ cat (i.e. variable and covariate are swapped in such case)
    as it's more straightforward to show dependency this way (however, see todo).
    In this case (num ~ cat) there are 3 main types of plots:
    - grouped cloud,
    - densities (separate density of y for each level of x),
    - boxplots (or each level of x);
    num ~ num is just an ordinary scatter-plot (with some add-ons),
    while cat ~ cat is a bar-chart (yet it's difficult case for large number of levels).

    As for the plot_variable() the idea was to make it fully automated but also very flexible –
    lots of intelligent preprocessing, fully parameterised but with sensible defaults, e.g.
    - `variable` and `covariate` may be passed as pd.Series or np.array or just names of the columns in `data`;
    - their names are taken from respective attribute or passsed separately or set automatically to `Y` and `X`
      if the previous are None; these names are used for proper automatic naming of plots and axes;
    - data do not need to be properly aligned wrt to no-NaNs
      – this is quite cumbersome procedure and it's completely tackled here;
    - we may align data wrt. index (default) or just by order of elements (`ignore_index` param);
    - we may simply `prune -> transform -> prune again` numeric data just passing limits and transformation
      in need (as scikit transformer or ordinary function);
      by default, when `transform=True` Yeo-Johnson transformation is used with automatic parameter
      (this is generalised Box-Cox transformation and it's usually all you need);
      again, this spares a lot of code-lines and dramatically speeds up search for good data transformation;
    - for categorical data the common problem is large number of levels: `most_common` parameter allows
      to limit number of them to only given number of most common levels (default is 13);
    - levels of categorical data may be sorted alphabetically;
    - num ~ num plot is given side histograms and may be additionally given qq-plot ('qq_plot=True')
      and lowess regression with given smoothing value (`smooth` param, default is 0.5 while 0 means no lowess line);
    - data set is by default limited to 10k random data-points to quicken plotting
      (usually with very little loss of statistical information);
      this is parameterised via `n_obs` and if `n_obs <= 1` then all points are plotted (be carefull though!);
    - number of bins for histogram is obviously settable (via `bins`, default is 21);
    - most important graphical parameters – `color`, point size `s`, transparency `alpha` – are set in various ways
      as str or float or pd.Series (separate values for each data point)
      – they are interpreted according to types of variable and covariate (i.e. according to plot type);
    - titles are set automatically and they are informative (with transformations and clipping values);
    - matplotlib plot style is taken into account:
        may be set externally via `plt.style.use(<style_name>)`
        or internally passing style name to `style`
        (`plt.style.availabe` is a list of all styles available);
    - we may choose `cmap` i.e. colormap;
      default is custom 'ak01' which is carefully constructed to have uniform luminosity (v. important!);
    - we may choose scale of axes (linear or log);
    - flexible and conveninet fig size and subplots arrangement.

    Basic params
    ------------
    variable: str | Variable (any Sequence of data);
        if str then it indicates column of `data`;
        else any Sequence of data (like pd.Series or just list) to be plotted;
        referenced for brevity as `y`;
        we plot `y ~ x` i.e. variable on y axis as dependent on covariate – x axis;
    covariate: str | Variable (any Sequence of data);
        as for `variable`
        referenced for brevity as `x`.
    data: pd.DataFrame = None
        if None then `variable` must be Sequence of data (e.g. pd.Series) with data of interest;
    stats: List[PlotType] | List[List[PlotType]] = [["grouped_cloud", "densities", "boxplots"]];
        This parameter is only considered for num ~ cat case (and cat ~ num which is turned to num ~ cat).
        list of lists (or just list which is internally changed to `list(what)`).
        It reflects the design of the whole final figure where
        each sublist represents one row of plots (axes) within a figure
        and each element of a sublist is the name of the respective plot type
        which will be rendered in a respective subplot (axis) of the figure.
        Thus each sublist should be of the same length (if not there will be blank subplots);
        possible values of the elements of the sublist (types of the plots) are:
            "cloud", "grouped_cloud", "densities", "boxplots", "distr", "barchart", "blank" (for empty subplot);
    what : []; list (of lists);
        alias for `stats` for backward compatibility;
    varname: Optional[str] = None;
        variable name to be used in title, etc.;
        if None then taken from .name attr of `variable` if exists, and if not then set to 'Y';
    covarname: Optional[str] = None;
        variable name to be used in title, etc.;
        if None then taken from .name attr of `variable` if exists, and if not then set to 'Y';
    title: Optional[str] = None,
        title of a plot; if None then generated automaticaly;
    title_suffix: Optional[str] = None,
        makes possible to distinguish plots for which automatic title would be the same;
    ignore_index: bool = False,
        if True then `y` and `x` will not be aligned wrt their index (if exists) but only positionally,
        i.e. as they are passed;
        otherwise (default) index is taken into account (if exists);

    as_factor_y: Optional[bool] = None,
        if True variable will be treated as categorical (factor);
        if False then numeric variable is never turned to factor
        (even if it has less distinct values than `factor_threshold`);
        if left None then it is turned into factor iff it has less unique values than `factor_threshold`;
    as_factor_x: Optional[bool] = None,
        the same as `as_factor_y` but for `x` (covariate);
    factor_threshold: int = 13,
        if mumeric variable (or covariate) has less distinct values than `factor_threshold`
        it will be treaded as categorical variable (factor);
        this will happen only if `as_factor_y` or `as_factor_x` are left None;

    Variable modifications (before plotting)
    ----------------------------------------

    # transformations

    lower_y: Optional[float] = None;
        lower limit of `variable` (y) to be plotted; inclusive !
        if None then `lower_y == min(variable)`
    upper_y: Optional[float] = None;
        upper limit of `variable` (y) to be plotted; inclusive !
        if None then `upper_y == max(variable)`
    exclude_y: Optional[Sequence[float] | float] = None;
        values to be excluded from `variable` (y) before plotting;
    transform_y: Optional[bool | Transformation] = None;
        what transformation of `variable` (y) to use (if any) before plotting;
        if None or False no transformation is used;
        if True then Yeo-Johnson transformation is used with automatic parameter;
        if function (Callable) is passed then this function is used;

    lower_x: Optional[float] = None;
        as `lower_y` but for `covariate` (x);
    upper_x: Optional[float] = None;
        as `upper_y` but for `covariate` (x);
    exclude_x: Optional[Sequence[float] | float] = None;
        as `exclude_y` but for `covariate` (x);
    transform_x: Optional[bool | Transformation] = None;
        as `transform_y` but for `covariate` (x);

    upper_t_y: Optional[float] = None;
        upper limit of transformed `variable` (y) to be plotted; inclusive !
        if None then `upper_t_y == max(transform_y(variable))`;
    lower_t_y: Optional[float] = None;
        lower limit of transformed `variable` (y) to be plotted; inclusive !
        if None then `lower == min(transformed_y(variable))`;
    exclude_t_y: Optional[Sequence[float] | float] = None;
        values to be excluded from transformed `variable` (y) before plotting;

    lower_t_x: Optional[float] = None;
        as `lower_t_y` but for `covariate` (x);
    upper_t_x: Optional[float] = None;
        as `upper_t_y` but for `covariate` (x);
    exclude_t_x: Optional[Sequence[float] | float] = None;
        as `exclude_t_y` but for `covariate` (x);

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

    # sampling

    n_obs: int = int(1e4),
        if at least 2 then maximum nr of observations to be sampled from variable before plotting
        "grouped_cloud", "densities", "distr";
        if `n_obs <= 1` the whole data will be plotted (what is usually not sensible for very large data).
    shuffle: bool = False;
        shuffle data before plotting -- useful only for "grouped_cloud" plot in case
        when data are provided in clumps with different statistical properties;
        shuffling helps to spot distribution features of the whole data.
    random_state: int = 2222,
        passed to numpy random generator for reproducibility in case of
        `n_obs <= 1` or shuffle is True;
    extremes: Optional[int | float] = .02
        in not 0 or None then this is number of extreme values for each numeric variable to be sampled;
        when float then it means portion of `n_obs`;
    most_common: int = 13,
        if <= 1 then all bars for all factor levels will be plotted;
        this is dangerous if not sure how many levels there are;
        it's better to set big integer but no bigger then 100;
        otherwise plot may not be rendered at all if there are thousands of levels;
        `most_common` is applied before `sort_levels`.

    Graphical parameters
    --------------------

    # Figure and axes parameters

    # ## for the whole figure
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
        color of the whole title plot (fig.suptitle)
        if None then set automatically according to style;
    suptitlesize: float = 1.,
        multiplier of 15 for the whole title plot (fig.suptitle)

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
        scale of axes of the subplots of type "cloud", "grouped_cloud", "densities", "distributions", "box_plots";
        possible values are "linear" and "log";
    xscale: Optional[Scale] = None,
        scale type of x-axis for "cloud" plot (num ~ num); overwrites `scale`;
    yscale: Optional[Scale] = None,
        scale type of y-axis for "cloud" plot (num ~ num); overwrites `scale`;
    #
    style: str | bool = True,
        if True takes all the graphic parameters set externally (uses style from environment);
        if False then is set to "dark_background";
        str must be a name of one of available styles: see `plt.style.available`.
        set style via `plt.style.use("style_name")` e.g. `plt.style.use("ggplot")`.
    grid: bool | dict = True,
        if False then no grid is plotted (regardless of style);
        if True then grid is plotted as ascribed to given style;
        in case of "black_background" it is dict(color='gray', alpha=.3)
        if dict then values from this dict will be applied as described in
        https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.grid.html
        Most general form (example values):
        { 'alpha': 1.0,  'color': '#b0b0b0',  'linestyle': '-',  'linewidth': 0.8 }
    axescolor: Optional[str] = None,
        color of the main axes (or rather the frame) of the subplot;
        if None then set automatically according to style;
    titlecolor: Optional[str] = None,
        color of axes titles;
        if None then set automatically according to style;

    # elements and attributes of plots (artists)

    lines: bool = True;                            # ! TODO
        lines for "grouped_cloud", "densities", "boxplots", "distr" which are put in the same places
        as limits of bins of the histogram of the numeric `variable` ("hist" subplot of `plot_numeric(variable)`);
    cmap: str | ColorMap = "ak01",
        matplotlib's ListedColormap, LinearSegmentedColormap or colormap name;
        for coloring wrt to categories of the categorical (levels of factor);
        "hsv" is a popular choice however it has uneaven luminosity;
        see https://matplotlib.org/stable/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py
        or dir(matplotlib.pyplot.cm) for list of all available color maps;
        see https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html#creating-colormaps-in-matplotlib
        on how to create and register ListedColormaps.

    ## data point

    color: Optional[str | pd.Series] = None,
        color of lines and points for 'cloud', 'boxplot', 'density' and 'distr';
        if None then set automatically according to `style`: "yellow" for style "black_background", else to "black";
        if it is str but not a valid color name and `data` is not None
        then it is interpreted as a name of a column in `data`
        where color values are stored (may be different for each data point);
        if pd.Series then must be of the same length as `variable`, `covariate` or `data` and stores
        color value for each data point;
    s: int | str | pd.Series = 9,
        size of a data point in a "cloud"
        if str and `data` is not None then it is interpreted as a name of a column in `data`
        where sizes of data point are stored;
        if pd.Series then must be of the same length as `variable`, `covariate` or `data` and stores
        size value for each data point;
    alpha: Optional[float | str | pd.Series] = None,
        float between 0 and 1; for points of "cloud" only;
        if None then set automatically according to `n_obs`;
        if str and `data` is not None then it is interpreted as a name of a column in `data`
        where alphas for data points are stored;
        if `pd.Series` then must be of the same length as `variable`, `covariate` or `data` and stores
        alpha value for each data point;
    brightness: Optional[float] = None,
        not used yet

    ## other parameters for various types of plots

    bins: int | List[float] = 21,
        if integer then how many bins for side histograms for num ~ num plot;
        if list of floats then these are boarders of bins;
        in both cases this arg is passed to `ax.hist(...)`;
    smooth: float = .5,
        For num ~ num plot (cloud of points) there is always plotted a lowess trend (of variable vs covariate);
        this param tells how smooth it should be: the higher the value the smoother is the trend estimation.
        Between 0 and 1: the fraction of the data used when estimating each y-value.
        0 means 'turn it off' – no lowess line.
    qq_plot: bool = False,
        do add qq-plot for  num_vs_num  plot?
    legend: bool = True,
        do draw legend on a plot?
    axes_labels: bool = True,
        do give labels to axes?

    ## only fac~fac

    bar_height: float = .5,
        only for barchart (factor ~ factor);
        this is relative to the space available for one bar (one category of variable in horizontal mode)
        not absolute (in any unit). 1 means use the whole space available.
    align: bool = True,
        only for barchart (factor ~ factor);
    horizontal: bool = True,
        only for boxplots (numeric ~ factor) (not working yet) and barchart (factor ~ factor);
    print_counts: bool = True,
        do print counts (number of cases with the respective combination of factor levels)
        on each bar of the (fac ~ fac) plot?

    Output & text
    -------------

    tex: bool = False,
        informs if the varname & covarname were passed in TeX format e.g. "\\hat{Y}" (double '\' needed)
        or how '_' should be interpreted (as part of name or TeX subscript);
    print_info: bool = True,
        print df.info(variable) (after all transformations)
    print_levels: bool = False,
        in case of one factor i.e. categorical variable (num ~ fac) prints table of counts and means of numeric
        for all factor levels (categories);
        in case of fac ~ fac prints table of counts for all combinations of levels of both variables;
        in both cases it prints information for all levels regardless of `most_common`
        what is somewhat dangerous as there may be huge number of levels;
        thus default is False (after all these informations are visualised on the plot);
        basically, it's only helper not an objective of this function so difficult cases should be treated separately;
    precision: int = 3,
        precision of floats as variable levels; more or less significant digits (however only for fractions);
        when turning numeric float variable into factor (makes sense when there are only few distinct values)
        then it's better to round the values to get nice factor level lables;
    use_logger: bool = False,
        use logger for ptinting (sensible only within scripts writing to file, otherwise clutters the screen);
    res: bool = False,
        do return result of all the calculations?
        default is False and then None is returned;
        otherwise (if True) dictionary is returned with the following structure:

    Returns
    -------
    If required (`res=True`) it is dictionary "of everything":

        result = {
            "title": title,     # title of the plot (suptitle)
            "df0": df0,         # unprocessed pd.DataFrame([variable, covariate])
            "df": df,           # processed   "  (after all clippings and transformations)
            "info": df0_info,                   # info on raw data
            "variation": df_variation,          # statistics for processed data
            "distribution": df_distribution,    # more statistics for processed data
            "plot": {           # plot objects
                "cloud": {
                    "axes": <Axes objects>,
                    "result": <data plotted>
                    }
                <
                  other subplot objects under respective keys as called for by `stats` / `what`
                  with keys like "ax" / "axes", "result", "agg" ... (depending on the plot type);
                >
                ...
                "fig": <Figure of a plot>
                }
        }

    Remarks
    -------
    1. When used in CL-scripts with `res=True` then plot is not automatically displayed on the screen
    (one might not want it but only to save figures to files via `result['plot']['fig'].savefig(...)`).
    Thus in such case remember about `plt.show()` just after this function call to get figure onto screen.
    When `res=False` (default) then `plt.show()` is run automatically
    (otherwise there would be no point of calling this function).
    In interactive mode plot is always displayed
    (exactly how, i.e. by what backend, depends on the IPython or Jupyter Notebook setup).

    2. Plots are drawn as `variable ~ covariate` i.e.
    `variable` serves as `y` (_dependent_ or _explained_ variable)
    and `covariate` serves as `x` (_independent_ or _explanatory_ variable).
    All parameter names where 'x' or 'y' is used are based on this convention.
    It was preferred to use 'x' or 'y' for its brevity;
    However, `variable` and `covariate` are used for the first two parameters
    (instead of 'y' and 'x') to convey their meaning and objective of the whole function:
    explain (via plots) `variable` (`y`) with `covariate` (`x`).

    3.
    - `style=True` by default what means using style set up externally
      and it is assumed to be set to `plt.style.use('dark_background')`;
    - All default graphic parameters are set for best fit with 'dark_background' style.
    - Unfortunately changing styles is not fully reversible, i.e.
      some parameters (`plt.rcParams`) stays changed after reverting style;
      (eg. grid stays white after 'ggplot',
      the same for title colors after 'black_background', etc);
      Just because of this there are some parameters like `color`, `grid`, `titlecolor`
      to set up their values by hand in case of unwanted "defaults".

    4. It is assumed that `variable` may be passed as `pd.Series`
    while `covariate` as a string indicating column of `data` (and vice versa).
    `variable` and `covariate` may have different indices while they may be irrelevant
    (to be ignored).
    Thus `ignore_index` is provided but it has different meaning from the same parameter of `pd.concat()`:
    here it means that if `ignore_index=True` then we ignore indices of `variable` and `covariate`
    and make one index common to both of them based solely on the elements order
    (thus number of elements must be the same in both series).
    It is critical for proper aligning of both data series.
    Default value for `ignore_index` is False what means that we pay attention to
    both indices and align two series according to indices values (like in pd.concat()).

    4. `most_common` applied before `sort_levels`.

    5. `fillna` option works only for categorical data, with default value '<NA>'.
    For numeric data filling NA values is left outside the scope of this function, because:
    - it is simple operation with no strange side effects on the plot
    - unlike for categorical data where in some situations unexpected things happen
      (especially for categoricals obtained from numerics) thus it's tackled inside to spare headache during analyses;
    - one may ommit NAs for categoricals (like by default for numerics) passing `fillna=None`,
      however it's usually more informative for the plots to treat NAs as separate category;
      yet user should be able to decide the name if it – '<NA>' is taken from R,
      however sometime may not be the best choice or even conflict with other category name.

    """
    # ---------------------------------------------------------------------------------------------
    #  preparations
    # -------------------------------------------------------------------------
    #  loading data

    variable, varname = h.get_var_and_name(variable, data, varname, "Y")
    covariate, covarname = h.get_var_and_name(covariate, data, covarname, "X")
    if varname == covarname:
        covarname += "_0"
        covariate.name = covarname

    # !!! index is ABSOLUTELY CRITICAL here !!!
    if ignore_index:
        variable, covariate, color, s, alpha = udf.align_indices(variable, covariate, color, s, alpha)  # type: ignore [assignment]  # it's too complicated for mypy # noqa

    # -----------------------------------------------------
    #  info on raw data

    df0 = pd.concat([variable, covariate], axis=1)
    # #df0.columns = pd.Index([varname, covarname])

    df0_info = udf.info(df0, stats=["dtype", "oks", "oks_ratio", "nans_ratio", "nans", "uniques"])

    if print_info:
        info = "\n" + \
            " 1. info on raw data" + "\n" + \
            df0_info.to_string()
        if use_logger:
            logger.info(info)
        else:
            print(info)

    variable_: pd.Series = cast(pd.Series, df0[varname])
    covariate_: pd.Series = cast(pd.Series, df0[covarname])

    del df0

    # -------------------------------------------------------------------------
    #  preparing data

    # this makes sense also for factors although not always
    variable_, _ = h.clip_transform(variable_, lower_y, upper_y, exclude_y)
    covariate_, _ = h.clip_transform(covariate_, lower_x, upper_x, exclude_x)

    # it's here because we may turn numeric to factor after clipping
    is_factor_y, variable_, variable_vc = h.to_factor(
        variable_, as_factor_y, factor_threshold=factor_threshold, most_common=most_common,
        fillna=fillna, sort_levels=sort_levels, ascending=ascending, precision=precision)
    is_factor_x, covariate_, covariate_vc = h.to_factor(
        covariate_, as_factor_x, factor_threshold=factor_threshold, most_common=most_common,
        fillna=fillna, sort_levels=sort_levels, ascending=ascending, precision=precision)

    # aligning data
    df0 = pd.merge(variable_, covariate_, left_index=True, right_index=True, how='outer')
    # #df0.columns = pd.Index([varname, covarname])
    df0.dropna(inplace=True)     # (*) this is essential for numeric data (but not for categorical with `fillna`)

    variable_ = df0[varname]
    covariate_ = df0[covarname]

    df = df0
    # df0 -- data not transformed (however clipped and .dropna())
    # df  -- data potentially transformed (or just copy of df0 if no tranformations)

    # -----------------------------------------------------
    #  transforms

    transname_y = None
    if not is_factor_y:
        variable_, transname_y = h.clip_transform(
            variable_, None, None, None,
            transform_y, lower_t_y, upper_t_y, exclude_t_y, "T_y")

    transname_x = None
    if not is_factor_x:
        covariate_, transname_x = h.clip_transform(
            covariate_, None, None, None,
            transform_x, lower_t_x, upper_t_x, exclude_t_x, "T_x")

    # aligning data
    transforms = [transform_y, lower_t_y, upper_t_y, exclude_t_y, transform_x, lower_t_x, upper_t_x, exclude_t_x]
    if any(transforms):
        df = pd.concat([variable_, covariate_], axis=1)
        df.columns = pd.Index([varname, covarname])
        df.dropna(inplace=True)     # (*)

        variable_ = df[varname]
        covariate_ = df[covarname]

        data_were_processed = True
    else:
        data_were_processed = False

    # must be repeated beacause of (*) (but now only for already-factors)
    is_factor_y, variable_, variable_vc = h.to_factor(
        variable_, is_factor_y, most_common=most_common, sort_levels=sort_levels, ascending=ascending)
    is_factor_x, covariate_, covariate_vc = h.to_factor(
        covariate_, is_factor_x, most_common=most_common, sort_levels=sort_levels, ascending=ascending)

    # -----------------------------------------------------
    #  statistics for processed data

    df_variation = udf.summary(
        df, stats=["oks", "uniques", "most_common", "most_common_ratio", "most_common_value", "dispersion"])

    df_distribution = udf.summary(
        df, stats=["range", "iqr", "mean", "median", "min", "max", "negatives", "zeros", "positives"])

    # -------------------------------------------------------------------------
    #  title

    if title is None:

        title = h.make_title(varname, lower_y, upper_y, transname_y, lower_t_y, upper_t_y, tex) + \
            " ~ " + \
            h.make_title(covarname, lower_x, upper_x, transname_x, lower_t_x, upper_t_x, tex)
        # the same for  numeric ~ factor  and  factor ~ numeric

    if title_suffix:
        title = title + title_suffix

    # -------------------------------------------------------------------------
    #  result

    result: MutableMapping = {
        "title": title,
        "df0": df0,  # unprocessed
        "df": df,    # processed
        "info": df0_info,
        "variation": df_variation,
        "distribution": df_distribution,  # data after all prunings and transformations
        "plot": dict()
    }

    # ---------------------------------------------------------------------------------------------
    #  plotting

    # -------------------------------------------------------------------------
    #  style affairs

    n_obs = len(variable_) if n_obs <= 1 else min(len(variable_), int(n_obs))

    # get  color, s, alhpa  from  data  if they are proper column names

    if isinstance(alpha, str):
        alpha = udf.get_column_or_except(alpha, data, "(for `alpha` parameter)")

    if isinstance(s, str):
        s = udf.get_column_or_except(s, data, "(for `s` parameter)")

    # take color from data only if it's not a color name
    if isinstance(color, str) and not h.is_mpl_color(color):
        color = udf.get_column_or_except(color, data, "(for `color` parameter)")

    color_data: pd.Series | str | None = color
    if not isinstance(color, str) and isinstance(color, Iterable):
        color = None         # from this moment `color` may be only str | None

    style, color, grid, axescolor, suptitlecolor, titlecolor, brightness, alpha = \
        h.style_affairs(style, color, grid, axescolor, suptitlecolor, titlecolor, brightness, alpha, n_obs)
    # now `color` is always str

    if color_data is None:
        color_data = color   # `color_data` is now valid color name (str) or Series of colors from `data`

    if isinstance(cmap, str):
        cmap = plt.colormaps[cmap]

    # -----------------------------------------------------
    # sampling and aligning color, size, alpha (if they are series)

    def sample_and_align(
            variable: pd.Series, covariate: pd.Series,
            n_obs: int, shuffle: bool, random_state: int, extremes: Optional[int | float],
            color: str | pd.Series, s: int | pd.Series, alpha: float | pd.Series,
            color_data: str | pd.Series,
    ) -> tuple[pd.Series, pd.Series,
               str | pd.Series, int | pd.Series,
               float | pd.Series, str | pd.Series]:
        df = pd.concat([variable, covariate], axis=1)
        df, color, s, alpha, color_data = udf.align_sample(     # type: ignore
            df, n_obs, shuffle, random_state, extremes,
            color=color, s=s, alpha=alpha, color_data=color_data
        )
        df, color, s, alpha, color_data = udf.align_nonas(      # type: ignore
            df,
            color=color, s=s, alpha=alpha, color_data=color_data
        )
        variable = df.iloc[:, 0]
        covariate = df.iloc[:, 1]
        return variable, covariate, color, s, alpha, color_data

    # -------------------------------------------------------------------------
    #  plot types

    # -----------------------------------------------------
    #  numeric ~ numeric

    def qq(variable: pd.Series, covariate: pd.Series) -> tuple[list[float], list[float]]:
        qqx = [covariate.quantile(q / 10) for q in range(11)]
        qqy = [variable.quantile(q / 10) for q in range(11)]
        return qqx, qqy

    def scatter_hist(ax: Axes, ax_histx: Axes, ax_histy: Axes, variable: pd.Series, covariate: pd.Series) -> dict:
        """helper for cloud()
        scatter plot of variable vs covariate and
        side histograms for each var (marginal distributions)
        """
        # no labels
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        # the scatter plot:
        scatter = ax.scatter(covariate, variable, s=s, color=color_data, alpha=alpha)  # type: ignore  # mypy is wrong – alpha MAY BE Sequence  # noqa
        if qq_plot:
            qqx, qqy = qq(variable, covariate)
            ax.plot(qqx, qqy, color=mpl.colors.to_rgba(cast(str, color), .5), marker="*")
        else:
            qqx, qqy = None, None

        histx = ax_histx.hist(covariate, bins=bins, color=mpl.colors.to_rgba(cast(str, color), .6))
        histy = ax_histy.hist(variable, bins=bins, color=mpl.colors.to_rgba(cast(str, color), .6), orientation='horizontal')    # noqa

        result = dict(scatter=scatter, histx=histx, histy=histy, qqx=qqx, qqy=qqy)
        return dict(ax=ax, result=result)

    def smoother(ax: Axes, variable: pd.Series, covariate: pd.Series) -> dict:
        """helper for cloud()
        lowess trend of variable vs covariate
        """
        xx = np.linspace(min(covariate), max(covariate), 100)
        smoothed = sm.nonparametric.lowess(
            exog=covariate, endog=variable,
            xvals=xx,
            frac=smooth)

        ax.plot(xx, smoothed, c="r" if color != 'r' else 'k')

        result = dict(xx=xx, smoothed=smoothed)
        return dict(ax=ax, result=result)

    def cloud(fig: Figure, variable: pd.Series, covariate: pd.Series, title: str = "scatter") -> dict:
        """
        On how to get side histograms
        https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py
        """
        # set_title(ax, title, titlecolor)
        # # ---------

        # definitions for the axes
        left, width = 0.1, 0.7
        bottom, height = 0.1, 0.7
        spacing = 0.005

        rect_scatter = (left, bottom, width, height)
        rect_histx = (left, bottom + height + spacing, width, 0.145)
        rect_histy = (left + width + spacing, bottom, 0.149, height)

        ax = fig.add_axes(rect_scatter)
        ax_histx = fig.add_axes(rect_histx, sharex=ax)
        ax_histy = fig.add_axes(rect_histy, sharey=ax)

        # use the previously defined function
        sh = scatter_hist(ax, ax_histx, ax_histy, variable, covariate)
        sm = smoother(sh['ax'], variable, covariate)
        ax = sm['ax']

        # plt.show()
        if axes_labels:
            ax.set_ylabel(varname)
            ax.set_xlabel(covarname)

        # ---------
        if grid:
            if isinstance(grid, dict):
                ax.grid(**grid)
                ax_histx.grid(**grid)
                ax_histy.grid(**grid)
        else:
            ax.grid(visible=False, axis="both")
            ax_histx.grid(visible=False, axis="both")
            ax_histy.grid(visible=False, axis="both")

        axes = dict(ax=ax, ax_histx=ax_histx, ax_histy=ax_histy)
        result = dict(scatter_hist=sh['result'], smoother=sm['result'])

        return dict(fig=fig, axes=axes, result=result)

    # -----------------------------------------------------
    #  numeric ~ factor

    def grouped_cloud(
            ax: Axes, variable: pd.Series, factor: pd.Series,
            cats: list[str], cat_colors: np.ndarray,
            title: str = "grouped cloud",
    ) -> dict:
        """
        """
        h.set_title(ax, title, titlecolor)
        # ---------

        dff = pd.concat([variable, factor], axis=1)
        dff.columns = pd.Index([variable.name, factor.name])
        dff = dff[dff[factor.name].isin(cats)]     # sorting is retained !
        dff = dff.sort_values(by=factor.name, ascending=False, ignore_index=True)

        scatters: dict = dict()
        # idx_cat_means: list() = []
        for cat, col in reversed(list(zip(cats, cat_colors))):
            vv = dff[variable.name][dff[factor.name] == cat]
            scatters[cat] = ax.scatter(vv, vv.index, color=col, s=s, alpha=alpha)  # type: ignore  # mypy is wrong – alpha MAY BE Sequence  # noqa
            # idx_cat_means.append(np.mean(vv.index))    # (1)  strange and bad coupling with the look of ax for densities !  # noqa

        if axes_labels:
            ax.set_xlabel(varname)
            # ax.set_ylabel('id')
        # ax.set_yticks(idx_cat_means[::-1], cats)    # (1)
        ax.set_yticks([])    # as long as (1) not fixed
        #  ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        #
        result = dict(scatter=scatters, cat_colors=cat_colors, dff=dff)
        return dict(ax=ax, result=result)

    def densities(
            ax: Axes, variable: pd.Series, factor: pd.Series,
            cats: list[str], cat_colors: np.ndarray,
            title: str = "densities by levels", legend: bool = legend
    ) -> dict:
        """
        """
        h.set_title(ax, title, titlecolor)
        # ---------
        result: dict = dict()
        for cat, col in list(zip(cats, cat_colors)):
            result[cat] = dict()
            vv = variable[factor == cat]
            if len(vv) > 1:
                try:
                    result[cat]['kde'] = gaussian_kde(vv.astype(float))
                except Exception:
                    result[cat]['kde'] = gaussian_kde(vv)
                xx = np.linspace(min(vv), max(vv), 200)
                lines = ax.plot(xx, result[cat]['kde'](xx), color=col, label=cat)
                result[cat]['xx'] = xx
                result[cat]['lines'] = lines
        if legend:
            ax.legend(title=covarname)
        if axes_labels:
            ax.set_xlabel(varname)
        ax.set_yticks([])
        # ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        #
        return dict(ax=ax, result=result)

    def distr(
            ax: Axes, variable: pd.Series, factor: pd.Series,
            cats: list[str], cat_colors: np.ndarray,
            title: str = "distributions by levels", legend: bool = legend
    ) -> dict:
        """
        """
        h.set_title(ax, title, titlecolor)
        # ---------
        result: dict = dict()
        for cat, col in list(zip(cats, cat_colors)):
            result[cat] = dict()
            vv = variable[factor == cat]
            if len(vv) > 1:
                # # line version
                # result = ax.plot(*h.distribution(vv), color=col, label=cat, linewidth=1)
                # dots version
                result[cat]['scatter'] = ax.scatter(*h.distribution(vv), s=1, color=col, label=cat)
                # `~matplotlib.collections.PathCollection`
        if legend:
            ax.legend(title=covarname)
        if axes_labels:
            ax.set_xlabel(varname)
        #  ---------
        h.set_xscale(ax, scale)
        h.set_grid(ax, off="both", grid=grid)
        #
        return dict(ax=ax, result=result)

    def boxplots(
            ax: Axes, variable: pd.Series, factor: pd.Series,
            cats: list[str], cat_colors: np.ndarray,
            title: str = "box-plots", horizontal: bool = True, color: str = cast(str, color)
    ) -> dict:
        """
        future:
            - violinplots
        """
        h.set_title(ax, title, titlecolor)
        # ---------

        vvg = variable.groupby(factor, observed=False)
        data = [vvg.get_group(g) for g in cats if g in vvg.groups.keys()]
        if horizontal:
            data = data[::-1]
            cat_colors = cat_colors[::-1]
            cats = cats[::-1]

        bplot = ax.boxplot(
            data,
            tick_labels=cats,  # `labels` deprecated since 3.9, renamed to `tick_labels`; will be removed in 3.11
            vert=(not horizontal),
            notch=False,
            #
            patch_artist=True,                              # !!!
            boxprops=dict(color=color, facecolor=color),
            whiskerprops=dict(color=color),
            capprops=dict(color=color),
            flierprops=dict(color=color, markeredgecolor=color, marker="|"),
            medianprops=dict(color=color, lw=3),   # (color='white' if color in ['k', 'black'] else 'k', lw=2),
            #
            showmeans=True,
            # meanline=False,
            meanprops=dict(  # color='white' if color in ['k', 'black'] else 'k',
                             marker="d",
                             markeredgecolor=color,
                             markerfacecolor='white' if color in ['k', 'black'] else 'k', markersize=11))

        for patch, color in zip(bplot['boxes'], cat_colors):
            patch.set_facecolor(color)

        if axes_labels:
            if horizontal:
                ax.set_xlabel(varname)
                ax.set_ylabel(covarname)
                h.set_xscale(ax, scale)
            else:
                ax.set_ylabel(varname)
                ax.set_xlabel(covarname)
                h.set_yscale(ax, scale)
        #  ---------
        h.set_grid(ax, off="both", grid=grid)
        #
        result = dict(bplot=bplot)
        return dict(ax=ax, result=result)

    # -----------------------------------------------------
    #  factor ~ factor

    def barchart(
            ax: Axes, crosstab: pd.DataFrame,
            title: Optional[str] = "bar-chart", horizontal: bool = True, align: bool = True,
            bar_height: float = bar_height
    ) -> dict:
        """
        for both factors
        future:
            - figure size for large amount of levels and long level names
        """
        # h.set_title(ax, title, titlecolor)
        # ---------

        # crosstab = pd.crosstab(covariate, variable)
        # like for horizontal view (default) – compare with num~fac – covariate on y-axis, variable along x-axis
        crosstab_cum = crosstab.cumsum(axis=1)

        labels_c = crosstab.index.to_list()
        labels_v = crosstab.columns.to_list()

        if align:
            data_widths = crosstab.apply(lambda x: x / sum(x), axis=1)
            data_widths_cum = crosstab_cum.apply(lambda x: x / max(x), axis=1)
        else:
            data_widths = crosstab
            data_widths_cum = crosstab_cum

        colors = cmap(np.linspace(0.1, 0.9, len(labels_v)))

        if horizontal:
            ax.invert_yaxis()
            ax.set_xlim(0, data_widths_cum.max().max())
            ax.xaxis.set_visible(False)
            ax.spines[['top', 'bottom', 'right']].set_visible(False)
        else:       # all the  _widths_  should be understood as  _heights_
            ax.set_ylim(0, data_widths_cum.max().max())
            ax.yaxis.set_visible(False)
            ax.spines[['top', 'left', 'right']].set_visible(False)
        ax.grid(visible=False, axis='both')

        for i, (cat, color) in enumerate(zip(labels_v, colors)):
            widths = data_widths.iloc[:, i]
            starts = data_widths_cum.iloc[:, i] - widths
            if horizontal:
                rects = ax.barh(labels_c, width=widths, left=starts, height=bar_height, label=cat, color=color)
            else:
                rects = ax.bar(labels_c, height=widths, bottom=starts, width=bar_height, label=cat, color=color)
            if print_counts:
                r, g, b, _ = color
                text_color = 'white' if r + g + b < 0.5 else 'black'
                ax.bar_label(rects, labels=crosstab.iloc[:, i], label_type='center', color=text_color)

        if horizontal:
            if axes_labels:
                ax.set_xlabel(varname)
                ax.set_ylabel(covarname)
            if legend:
                ax = h.horizontal_legend(
                    ax, title=varname, thresh=(width * 10), extra=5
                )
        else:
            if axes_labels:
                ax.set_ylabel(varname)
                ax.set_xlabel(covarname)
            if legend:
                ax.legend(
                    ncol=1, bbox_to_anchor=(0, .5), loc='center right', fontsize='small', title=varname, reverse=True)

        # ---------
        result = dict(rects=rects)
        return dict(ax=ax, result=result)

    # -----------------------------------------------------
    #  special

    def blank(
            ax: Axes,
            variable: Any, factor: Any, cats: Any, cat_colors: Any, cmap: Any, title: str = "",
            *args: Any, **kwargs: Any
    ) -> dict:
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        ax.plot()
        ax.axis('off')
        ax.text(
            0.5, 0.5, '',
            verticalalignment='center', horizontalalignment='center',
            transform=ax.transAxes,
            color='gray', fontsize=10)
        return dict(ax=ax, result=False)

    def error(ax: Axes, title: str = "error") -> dict:
        """"""
        h.set_title(ax, title, titlecolor)
        #  ---------
        ax.plot()
        ax.axis('off')
        ax.text(
            0.5, 0.5, 'unavailable',
            verticalalignment='center', horizontalalignment='center',
            transform=ax.transAxes,
            color='gray', fontsize=10)
        return dict(ax=ax, result=False)

    # -----------------------------------------------------
    #
    class PlotItem(TypedDict):
        plot: Callable
        name: str

    PLOTS: dict[str, PlotItem] = {
        "boxplots": {"plot": boxplots, "name": "box-plots"},
        "cloud": {"plot": cloud, "name": "scatter"},
        "grouped_cloud": {"plot": grouped_cloud, "name": "grouped cloud"},
        "densities": {"plot": densities, "name": "densities"},
        "distr": {"plot": distr, "name": "distributions"},
        "barchart": {"plot": barchart, "name": "bar chart"},
        "blank": {"plot": blank, "name": ""},
        "error": {"plot": error, "name": "error"},
    }

    # -------------------------------------------------------------------------
    #  plotting procedure

    # -----------------------------------------------------
    #  sizes
    def set_fig(
            nrows: int = 1, ncols: int = 1
    ) -> tuple[Figure, NDArray[Axes]]:  # type: ignore  # cannot be Axes but it MUST be Axes (and works!)
        """"""
        nonlocal size
        nonlocal height
        nonlocal width
        nonlocal figsize
        nonlocal figheight
        nonlocal figwidth

        if nrows == 0 or ncols == 0:
            """
            for uneven (custom) figure split into axes
            see  numeric_vs_numeric()  ->  cloud()
            """
            if figsize is None:
                figheight = figheight or (height or (size * 2.2))
                figwidth = figwidth or (width or (size * 2.2))
                figsize = figwidth, figheight

            fig = plt.figure(figsize=figsize)
            axs = None

        else:
            if figsize is None:
                figwidth = figwidth or (ncols * (width or (size * width_adjust)))
                figheight = figheight or (nrows * (height or size) + 1)     # ? +1 for title
                figsize = figwidth, figheight

            fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

        return fig, np.array(axs)

    # -----------------------------------------------------
    #  variable ~ covariate scenarios

    def numeric_vs_numeric(variable: pd.Series, covariate: pd.Series) -> Figure:
        """"""
        nonlocal result
        nonlocal df
        nonlocal color
        nonlocal s
        nonlocal alpha
        nonlocal color_data

        fig, _ = set_fig(0)

        # statistics:
        if print_info:  # of course!
            info = "\n" + \
                " 2. statistics for processed data (on the plot)" + "\n" + \
                df_variation.to_string() + "\n" + \
                df_distribution.to_string()
            if use_logger:
                logger.info(info)
            else:
                print(info)

        variable, covariate, color, s, alpha, color_data = \
            sample_and_align(
                variable, covariate, n_obs=n_obs, shuffle=shuffle, random_state=random_state, extremes=extremes,
                color=color, s=s, alpha=alpha, color_data=color_data    # type: ignore  # none of these args is None at this stage  # noqa
            )

        resc = cloud(fig, variable, covariate, title=title)   # fig, axes, result

        h.set_xscale(resc['axes']['ax'], xscale or scale)
        h.set_xscale(resc['axes']['ax_histx'], xscale or scale)

        h.set_yscale(resc['axes']['ax'], yscale or scale)
        h.set_yscale(resc['axes']['ax_histy'], yscale or scale)

        result['plot']["cloud"] = {'axes': resc['axes'], 'result': resc['result']}
        fig = resc['fig']

        return fig

    def numeric_vs_factor(num: pd.Series, fac: pd.Series, most_common: pd.Series) -> Figure:
        """"""
        nonlocal result
        nonlocal df0
        nonlocal df
        nonlocal stats
        nonlocal what
        nonlocal cmap
        nonlocal color
        nonlocal s
        nonlocal alpha
        nonlocal color_data

        # ---------------------------------------
        # for potentially processed data    -- but NOT sampled yet (i.e. always all data!)
        df1 = pd.concat([num, fac], axis=1)
        df1agg = df1.groupby([fac.name], observed=False).agg([len, "mean"])
        df1agg = df1agg.droplevel(level=0, axis=1).sort_values(by=["len"], ascending=False)

        if data_were_processed:
            df0 = df0.loc[df.index, :]
            df0agg = df0.groupby([fac.name]).agg("mean")
            df0agg.columns = pd.Index(["mean oryg."])

            df1agg = pd.merge(df1agg, df0agg, left_index=True, right_index=True, how='left')

        # statistics:
        if print_info:  # of course!
            info = "\n" + \
                " 2. statistics for processed data (on the plot)" + "\n" + \
                df_variation.to_string()
            if print_levels:
                info += "\n\n" + df1agg.to_string()
            if use_logger:
                logger.info(info)
            else:
                print(info)

        # ---------------------------------------
        #  figure and plots sizes
        stats = what or stats
        stats = np.array(stats, ndmin=2)
        nrows = stats.shape[0]
        ncols = stats.shape[1]

        fig, axs = set_fig(nrows, ncols)
        axs = np.reshape(axs, (nrows, ncols))    # unfortunately it's necessary because ...

        cats, cat_colors, cmap_ = h.cats_and_colors(most_common, cmap)

        for t in ["boxplots", "blank"]:
            if t in stats:
                ax = axs[np.nonzero(stats == t)][0]
                try:
                    result['plot'][t] = PLOTS[t]["plot"](
                        ax, num, fac, cats, cat_colors, PLOTS[t]["name"], horizontal, color
                    )
                except Exception as e:
                    print(e)
                    result['plot'][t] = PLOTS["error"]["plot"](ax, PLOTS[t]["name"])

        num, fac, color, s, alpha, color_data = \
            sample_and_align(
                num, fac, n_obs=n_obs, shuffle=shuffle, random_state=random_state, extremes=extremes,
                color=color, s=s, alpha=alpha, color_data=color_data    # type: ignore  # none of these args is None at this stage  # noqa
            )

        for t in ["grouped_cloud", "densities", "distr"]:
            if t in stats:
                ax = axs[np.nonzero(stats == t)][0]
                try:
                    result['plot'][t] = PLOTS[t]["plot"](
                        ax, num, fac, cats, cat_colors, PLOTS[t]["name"]
                    )
                except Exception as e:
                    print(e)
                    result['plot'][t] = PLOTS["error"]["plot"](ax, PLOTS[t]["name"])

        result['plot']["agg"] = df1agg

        return fig

    def factor_vs_factor(
            variable: pd.Series, covariate: pd.Series,
            most_common_v: pd.Series, most_common_c: pd.Series
    ) -> Figure:
        """"""
        nonlocal result
        nonlocal height
        nonlocal width

        crosstab = pd.crosstab(covariate, variable).loc[most_common_c.index, most_common_v.index]
        # like for horizontal view (default) – compare with num~fac – covariate on y-axis, variable along x-axis

        n_cats_v = len(most_common_v)
        n_cats_c = len(most_common_c)
        longest_cat_v = max(map(lambda s: len(str(s)), most_common_v.index))

        if horizontal:
            height = height or max(n_cats_c * .5 + 1, size)
            width = width or max(n_cats_v * .5 + longest_cat_v * .1, size * width_adjust)
        else:
            height = height or max(n_cats_v * .3, size)
            width = width or max(n_cats_c * .7 + longest_cat_v * .1, size * width_adjust)

        fig, axs = set_fig(nrows=1, ncols=1)

        result['plot']["barchart"] = barchart(
            cast(Axes, axs.tolist()), crosstab, title, horizontal, align, bar_height
        )

        result['plot']["agg"] = pd.crosstab(covariate, variable, margins=True)

        # statistics:
        if print_info:  # of course!
            info = "\n" + \
                " 2. statistics for processed data (on the plot)" + "\n" + \
                df_variation.to_string()
            if print_levels:
                info += "\n\n" + result['plot']["agg"].to_string()
            if use_logger:
                logger.info(info)
            else:
                print(info)

        return fig

    # -----------------------------------------------------
    #  core

    if is_factor_y:
        if is_factor_x:
            fig = factor_vs_factor(variable_, covariate_, variable_vc, covariate_vc)
        else:
            fig = numeric_vs_factor(covariate_, variable_, variable_vc)
    else:
        if is_factor_x:
            fig = numeric_vs_factor(variable_, covariate_, covariate_vc)
        else:
            fig = numeric_vs_numeric(variable_, covariate_)

    # -------------------------------------------------------------------------
    #  final

    h.set_figtitle(fig, title, suptitlecolor, suptitlesize)

    fig.tight_layout()
    # !! UserWarning: This figure includes Axes that are not compatible with tight_layout,
    # so results might be incorrect.
    # (for numeric vs numeric with side histograms)

    # plt.show()  # in scripts we might not want it – only to write result (figure) to file;

    result['plot']["fig"] = fig

    if not res:
        plt.show()      # not necessary in interactive mode but necessary in CL-scripts
        return None
    else:
        return result   # in CL-scripts remember about  plt.show()  to get figure onto screen

# %%
