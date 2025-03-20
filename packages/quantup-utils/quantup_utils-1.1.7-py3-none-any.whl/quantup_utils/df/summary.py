#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
title: Info and summary on pd.DataFrame
version: 1.0
type: module
keywords: [data frame, info/summary table]
description: |
content:
    -
remarks:
todo:
    - use try/except to serve more types; how to serve exceptions? stop! (~109)
    - round safely (i.e. only to significant digits !!!) (~331)
sources:
"""

# %%
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from scipy.stats import entropy  # type: ignore

from typing import Literal, Optional, Any, Callable, Sequence, Union, TypedDict, get_args
from numpy.typing import NDArray

Data = Union[pd.DataFrame, pd.Series]
Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']
Factor = Union[Sequence[str], NDArray[np.str_], 'pd.Series[str]']
Variable = Union[Numeric, Factor]
Transformation = Callable[[Numeric], Numeric]
Aggregate = Callable[[Numeric], float | None]

Stat = Literal[
    "dtype", "position", "oks", "oks_ratio", "nans_ratio", "nans", "uniques",
    "most_common", "most_common_ratio", "most_common_value", "negatives", "zeros", "positives",
    "mean", "median", "min", "max", "range", "dispersion", "iqr"
]
TakeAll = Literal["all", "everything"]
StatAll = Stat | TakeAll
StatOrAgg = StatAll | Aggregate
InfoArg = list[StatOrAgg] | tuple[StatOrAgg, ...] | StatOrAgg

SeqOfStr = list[str] | tuple[str, ...] | str

NUMS = {"float", "float64", "int", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8"}

PD_DATES = {"datetime64[ns]", "datetime64[s]", "datetime64"}


class StatInfo(TypedDict):
    name: str
    abbr: str
    stat: Callable


def to_list(x: InfoArg) -> list[StatOrAgg]:
    if not isinstance(x, (list, tuple)):
        x = [x]
    return list(x)


def manage_types_list(types_list: Optional[SeqOfStr]) -> list[str] | None:
    if types_list is not None:
        if not isinstance(types_list, (list, tuple)):
            types_list = [types_list]
        types_list = list(types_list)
        if "numeric" in types_list:
            types_list.extend(NUMS)
        if len({"date", "time", "datetime"}.union(PD_DATES).intersection(types_list)) > 0:
            types_list.extend(PD_DATES)
    return types_list


# %%
def info(
        df: Data,
        stats: InfoArg = (
            "dtype", "oks", "oks_ratio", "nans_ratio", "nans", "uniques", "most_common", "most_common_ratio"
        ),
        what: Optional[InfoArg] = None,      # alias for `stats` for backward compatibility
        add: Optional[InfoArg] = None,
        #            # "position", "most_common_value", "negatives", "zeros", "positives"
        #            # "mean", "median", "min", "max", "range", "dispersion", "iqr"
        sub: Optional[InfoArg] = None,  # stats we do not want
        #            # (even if otherwise we want "all"/"everything")
        #
        omit: Optional[SeqOfStr] = None,     # columns/variables to omit
        dtypes: Optional[SeqOfStr] = None,   # only these dtypes; if None then all dtypes
        exclude: Optional[SeqOfStr] = None,  # but not these types
        round: Optional[int] = None,
        name_as_index: bool = True,
        short_names: bool = False,
        exceptions: bool = False,
) -> pd.DataFrame:
    """
    Basic information on columns of data frame `df`.
    Remarks:
    - 'most_common_ratio' is the ratio of the most common value to all no-NaN values
    - 'position' is the position of the column/variable in a `df`
    All possible stats (statistics/infos) are:
        dtype
        position
        oks
        oks_ratio
        nans_ratio
        nans
        uniques
        most_common
        most_common_ratio
        most_common_value
        negatives
        zeros
        positives
        mean
        median
        min
        max
        range
        dispersion
        iqr
        all / everything  = take all the above
    """

    # ---------------------------------------------------------------------
    #  basic preparations: args preproc

    # !!! use try/except to serve more types; how to serve exceptions? stop!
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    stats = to_list(what) if what else to_list(stats)

    if add:
        stats.extend(to_list(add))

    sub = to_list(sub) if sub else list()

    if "all" in stats or "everything" in stats:
        stats.extend([w for w in get_args(Stat) if w not in stats])
        # add everything from Stat but avoid repetition and preserve as much order as possible
        sub.extend(["all", "everything"])

    if len(sub) > 0:
        stats = [w for w in stats if w not in sub]

    if omit and isinstance(omit, str):
        omit = [omit]

    dtypes = manage_types_list(dtypes)
    exclude = manage_types_list(exclude)

    # ---------------------------------------------------------------------
    # stats

    N = df.shape[0]
    info = pd.DataFrame()
    ss = pd.Series()

    # -------------------------------------------------
    #  core parameters (unique for each column)

    OKs: int | None = None
    NANs: int | None = None

    ss_position: int = 0
    ss_vc: pd.Series | None = None      # = ss.value_counts()
    ss_min: float | None = None
    ss_max: float | None = None

    # -------------------------------------------------
    #  core stats subroutines

    def dtype() -> str | None:
        return ss.dtype.__str__()   # !

    def oks() -> int | None:
        return OKs

    def nans() -> int | None:
        return NANs

    def oks_ratio() -> float | None:
        res = float(OKs / N) if OKs else None
        return res

    def nans_ratio() -> float | None:
        return float(NANs / N)

    def col_position() -> float | None:
        return ss_position

    # -------------------------------------------------
    #  other stats  subroutines

    def negatives() -> int | None:
        return sum(ss < 0)

    def zeros() -> int | None:
        return sum(ss == 0)

    def positives() -> int | None:
        return sum(ss > 0)

    def uniques() -> int | None:
        res = len(ss_vc) if ss_vc is not None else None
        return res

    def most_common() -> int | None:
        res = int(ss_vc.max()) if ss_vc is not None else None
        return res

    def most_common_ratio() -> float | None:
        res = float(ss_vc.max()) / OKs if (ss_vc is not None and OKs) else None
        return res

    def most_common_value() -> Any | None:
        res = ss_vc.index[0] if ss_vc is not None else None
        return res

    def mean() -> float | None:
        return ss.mean()

    def median() -> float | None:
        return ss.median()

    def min_() -> float | None:
        return ss_min

    def max_() -> float | None:
        return ss_max

    def range_() -> float | None:
        res = (ss_max - ss_min) if (ss_max is not None and ss_min is not None) else None
        return res

    def dispersion() -> float | None:
        if is_numeric_dtype(ss):
            var = np.sqrt(ss.var())  # type: ignore  # Argument 1 to "__call__" of "_UFunc_Nin1_Nout1" has incompatible type "str | ... # nonsense!  # noqa
        else:
            # "relative" entropy (wrt. maximum entropy – NOT a KL-distance)
            # the smaller value the less variability i.e. ~ "near-zero-variance"
            if ss_vc is not None and OKs:
                var = 0. if len(ss_vc) == 1 else entropy(ss_vc / OKs) / entropy(np.ones(len(ss_vc)) / len(ss_vc))
            else:
                var = None  # will never happen (but mypy can't get it)
        return float(var)

    def iqr() -> float:
        return ss.quantile(.75) - ss.quantile(.25)

    STATS: dict[str, StatInfo] = {
        "dtype": {"name": "dtype", "abbr": "dtype", "stat": dtype},
        "position": {"name": "position", "abbr": "pos", "stat": col_position},
        "oks": {"name": "OKs", "abbr": "OKs", "stat": oks},
        "nans": {"name": "NaNs", "abbr": "NaNs", "stat": nans},
        "oks_ratio": {"name": "OKs_ratio", "abbr": "OKs/all", "stat": oks_ratio},
        "nans_ratio": {"name": "NaNs_ratio", "abbr": "NaNs/all", "stat": nans_ratio},
        "uniques": {"name": "uniques_nr", "abbr": "uniq", "stat": uniques},
        "most_common": {"name": "most_common", "abbr": "mc", "stat": most_common},
        "most_common_ratio": {"name": "most_common_ratio", "abbr": "mc/all", "stat": most_common_ratio},
        "most_common_value": {"name": "most_common_value", "abbr": "mcv", "stat": most_common_value},
        "negatives": {"name": "<0", "abbr": "<0", "stat": negatives},
        "zeros": {"name": "=0", "abbr": "=0", "stat": zeros},
        "positives": {"name": ">0", "abbr": ">0", "stat": positives},
        "mean": {"name": "mean", "abbr": "mean", "stat": mean},
        "median": {"name": "median", "abbr": "med", "stat": median},
        "min": {"name": "min", "abbr": "min", "stat": min_},
        "max": {"name": "max", "abbr": "max", "stat": max_},
        "range": {"name": "range", "abbr": "rng", "stat": range_},
        "iqr": {"name": "IQR", "abbr": "IQR", "stat": iqr},
        "dispersion": {"name": "dispersion", "abbr": "disp", "stat": dispersion},
    }

    name: Literal["abbr", "name"] = "abbr" if short_names else "name"

    # ---------------------------------------------------------------------
    # MAIN LOOP : fill `info` data frame with values

    for colname, ss in df.items():  # iteritems() for pandas <2.0
        ss_position += 1

        if (dtypes and not dtype() in dtypes) or \
           (exclude and dtype() in exclude) or \
           (omit and colname in omit):
            continue

        item = {"name": [colname]}

        ss = ss.dropna()        # !

        if len({"oks", "nans", "oks_ratio", "nans_ratio", "dispersion", "most_common_ratio"}
               .intersection(stats)) > 0:
            OKs = len(ss)       # !
            NANs = N - OKs

        if len({"uniques", "most_common", "most_common_ratio", "most_common_value", "dispersion"}
               .intersection(stats)) > 0:
            ss_vc = ss.value_counts()

        if len(set(["min", "max", "range"]).intersection(stats)) > 0:
            try:
                ss_min, ss_max = ss.min(), ss.max()
            except Exception as e:
                if exceptions:
                    print(e)
                ss_min, ss_max = None, None

        for w in stats:
            if w in STATS.keys():
                w_ = str(w)  # mypy nonsense
                try:
                    if (v := STATS[w_]['stat']()) is not None:
                        item[str(STATS[w_][name])] = [v]
                except Exception as e:
                    if exceptions:
                        print(e)
            else:
                w_name = w.__name__ if hasattr(w, "__name__") else str(w)  # type: ignore  # mypy doesn't recognise duck-typing https://github.com/python/mypy/issues/2420 # noqa
                try:
                    if callable(w) and (v := w(ss)) is not None:
                        item[w_name] = [v]
                except Exception as e:
                    if exceptions:
                        print(e)

        info = pd.concat([info, pd.DataFrame(item)])

        OKs = None
        NANs = None
        ss_vc = None
        ss_min = None
        ss_max = None

        #  END OF LOOP

    info.reset_index(inplace=True, drop=True)

    if name_as_index:
        info.index = pd.Index(info['name'])
        info.drop(columns=['name'], inplace=True)

    # !!! round safely (i.e. only to significant digits !!!)
    if round:
        info = info.round(round)

    return info


# %%
def summary(
        df: Data,
        stats: InfoArg = (
            "dtype", "negatives", "zeros", "positives", "mean", "median", "min", "max", "range", "iqr", "dispersion"
        ),
        what: Optional[InfoArg] = None,      # alias for `stats` for backward compatibility
        add: Optional[InfoArg] = None,
        #            # "position", "most_common_value", "negatives", "zeros", "positives"
        #            # "mean", "median", "min", "max", "range", "dispersion", "iqr"
        sub: Optional[InfoArg] = None,  # statistics we do not want
        #            # (even if otherwise we want "all"/"everything")
        #
        omit: Optional[SeqOfStr] = None,     # columns/variables to omit
        dtypes: Optional[SeqOfStr] = None,   # only these dtypes; if None then all dtypes
        exclude: Optional[SeqOfStr] = None,  # but not these types
        round: Optional[int] = None,
        name_as_index: bool = True,
        short_names: bool = False,
        exceptions: bool = False,
) -> pd.DataFrame:
    """
    version of info() focused by default on statistical properties (mean, median, etc.)
    rather than technical (like NaNs number and proportions);
    i.e. info() with different (kind of reversed) defaults
    """
    summary = info(
        df, stats=stats, what=what, add=add, sub=sub,
        omit=omit, dtypes=dtypes, exclude=exclude,
        round=round,
        name_as_index=name_as_index,
        short_names=short_names,
        exceptions=exceptions,
    )

    return summary

# %%
