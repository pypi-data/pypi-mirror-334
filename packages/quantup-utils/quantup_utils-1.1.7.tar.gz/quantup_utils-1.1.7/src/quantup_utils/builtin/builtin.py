#! python3
# -*- coding: utf-8 -*-
"""
---
title: Conveniences And Utilities – lacking builtins
subtitle: Based only on built-ins and basic libraries.
version: 1.0
type: module
keywords: [flatten, coalesce, ... ]
description: |
    Convenience functions and utilities used in everyday work
    which might be regarded as lacking builtins and are not implemented in any basic library.
    Only basic packages from standard library should be used,
    like functools, itertools, typing, time, math, etc.
    i.e. additional installations (via pip or conda) shouldn't be needed.
todo:
sources:
"""
from typing import Any, Union, Iterable
import numpy as np
import math as m


def coalesce(*args: Any, empty: tuple[Any] = (None,)) -> Any | None:
    """
    As in PostgreSQL: returns first not None argument;
    if all arguments are None then returns None.

    However it is possible to provide own empties via `empty` keyword-argument:
    each element of `empty` tuple is considered as being "empty" value
    and is ommited when searching for first non-empty.
    If all arguments are empty then first element of `empty` (None by default) is returned.

    This is safe (thus default to use) version
    where we use `is` operator for checking if element is in `empty`.
    Notice that `1 == True` and `0 == False` evaluates to `True` what is a reason behind
        coalesce0(None, False, 0, 1, 0, empty=(None, False))     # 1, as `0 == False` is True
    (what is WRONG! `coalesce0` used `==` instead of `is`)
    but
        coalesce(None, False, 0, 1, 0, empty=(None, False))      # 0, as `0 is False` is False
    what is demanded behaviour.

    However this version is slower (checking `is` is slower then `==` ?)
    than coalesce0().

    Examples
    --------
    coalesce(1, None, None)     # 1
    coalesce(None, None, None)  # None
    coalesce(None, None, False) # False
    coalesce(None, None, False, empty=(None, False))    # None
    coalesce(None, None, False, empty=(False, None))    # False
    coalesce(None, None, False, 1, empty=(None, False)) # 1
    coalesce(None, False, 0, 1, 0, empty=(None, False)) # 0       # because `0 is False` is False
    coalesce0(None, False, 0, 1, 0, empty=(None, False))  # 1     # because `0 == False` is True
    """
    for res in args:
        is_empty = False
        for e in empty:
            if e is res:
                is_empty = True
                break
        if not is_empty:
            return res
    return empty[0]


def flatten(lst: list) -> list:
    """
    Examples
    --------
    flatten([1, 2, [[3, 4, [5]], 6, 7], 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    flatten([1, 2, [["3, 4", [5]], 6, 7], "8"]) == [1, 2, "3, 4", 5, 6, 7, "8"]
    flatten([1, 2, [[(3, 4), [5]], {6, 7}], "8"]) == [1, 2, (3, 4), 5, {6, 7}, "8"]
    """
    result = []
    for l in lst:
        if isinstance(l, list):
            result.extend(flatten(l))
        else:
            result.append(l)
    return result


def adaptive_round(value: Union[float, Iterable[float], str], r: int = 4):
    """
    Rounding numbers to only r significant digits;
    if not number returns value unchanged;
    iterates over elements of Iterables (recursively) except strings which are ignored.
    Notice the difference:
    adaptive_round(123456, 3)     # 123456
    "{:.3g}".format(123456)       # '1.23e+05'
    adaptive_round(.123456, 3)     # .1235
    "{:.3g}".format(.123456)       # '.123'
    adaptive_round(.000123456, 3)     # .0001235
    "{:.3g}".format(.000123456)       # '.000123'
    adaptive_round(.000000123456, 3)     # 1.235e-07
    "{:.3g}".format(.000000123456)       # '1.23e-07'
    """
    if value is None:
        pass
    elif isinstance(value, (str, int)):
        pass
    elif isinstance(value, Iterable):
        value = [adaptive_round(v, r) for v in value]
    elif isinstance(value, float):
        r = round(m.log10(abs(value))) - r
        r = max(0, -r)
        value = round(value, r)
    else:
        pass
    return value


def reorder(seq: list | tuple, step: int, flat: bool = True) -> list:
    """
    Examples
    --------
    reorder(list('123456789'), 3)   # ['1', '4', '7', '2', '5', '8', '3', '6', '9']
    reorder(list('123456789'), 3, False)   # [['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9']]
    reorder(list('123456789'), 4)   # ['1', '5', '9', '2', '6', '3', '7', '4', '8']
    reorder(list('123456789'), 4, False)   # [['1', '5', '9'], ['2', '6'], ['3', '7'], ['4', '8']]
    """
    res = [seq[i::step] for i in range(step)]
    if flat:
        res = sum(res, [])
    return res


def get_optimal_division(aa: list[str], thresh: int = 300, penalty: int = 3) -> tuple[int, int, int]:
    """
    For given sequence of numbers, divide it into groups in such a way that:
    1. (sum of elements in each group) + penalty * g <= thresh (where `g` is length of a group);
    2. we search for longest groups yet the most even divisions,
       e.g. for sequence of length 11 we take division into groups of length (4, 4, 3) instead of (5, 5, 1)
       even if condition 1 is satisfied for the latter.
    Obtained by brute force search (yet very efficient).
    """
    l = len(aa)
    split = []
    for r in range(1, l + 1):
        c = int(np.ceil(l / r))
        rows = np.split(aa, np.arange(1, r) * c)
        len_last = len(rows[-1])
        if len_last > 0:
            row_max_length = max(map(sum, rows))
            split.append((r, c, row_max_length + penalty * c))     # nrows,  ncols,  max_col_width
    # [print(s, "\n") for s in split]
    k = 0
    while split[k][2] > thresh:
        k += 1
    else:
        res = split[k]
    return res          # nrows,  ncols,  max_col_width
