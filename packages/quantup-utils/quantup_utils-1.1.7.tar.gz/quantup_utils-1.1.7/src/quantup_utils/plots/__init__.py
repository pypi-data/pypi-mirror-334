from .helpers import is_mpl_color, get_var_and_name, distribution, agg_for_bins, sample, \
    clip_transform, prepare_factor, to_factor, cats_and_colors, \
    make_title, style_affairs, set_xscale, set_yscale, set_grid, set_title, set_figtitle, \
    horizontal_legend
from .plot_covariates import plot_covariates
from .plot_numeric import plot_numeric, plot_num
from .plot_factor import plot_factor, plot_cat
from .plot_variable import plot_variable
from .rocs import plot_roc

__all__ = [
    'is_mpl_color', 'get_var_and_name', 'distribution', 'agg_for_bins', 'sample',
    'clip_transform', 'prepare_factor', 'to_factor', 'cats_and_colors',
    'make_title', 'style_affairs', 'set_xscale', 'set_yscale', 'set_grid', 'set_title', 'set_figtitle',
    'horizontal_legend',
    'plot_covariates',
    'plot_numeric', 'plot_num', 'plot_factor', 'plot_cat', 'plot_variable',
    'plot_roc',
]
