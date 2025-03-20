#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from typing import Optional

import matplotlib.pyplot as plt
plt.style.use('ggplot')
# other commonly used versions of style are:
# plt.style.use('grayscale')
# plt.style.use('dark_background')
# see `plt.style.available` for list of available styles


def pandas_options(kwargs: Optional[dict[str, str | float | None]] = None) -> None:
    """
    Setting pandas parameters, especially those concerning displaying data frames and series.
    However arbitrary set of parameters may be passed within one dictionary.

    kwargs: dict = {}
        each `key: value` pair is passed to `pd.set_option(key, value)`.

    https://stackoverflow.com/questions/11707586/how-do-i-expand-the-output-display-to-see-more-columns-of-a-pandas-dataframe
    """
    pd.set_option('display.width', 1000)
    # pd.options.display.width = 0  # autodetects the size of your terminal window - does it work???
    pd.set_option("display.max_rows", None)
    # pd.options.display.max_rows = None         # the same
    pd.set_option('max_colwidth', None)

    pd.set_option("display.max_columns", None)
    pd.set_option('display.max_seq_items', None)

    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.precision', 3)

    if kwargs:
        for k, v in kwargs.items():
            pd.set_option(k, v)
