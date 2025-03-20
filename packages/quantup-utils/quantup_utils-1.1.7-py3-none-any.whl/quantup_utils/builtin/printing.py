#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any


def section(title: str, out: Any = True, vsep: int = 1, level: int = 1) -> None:
    """
    Prints out `title` of the section (of the code).
    Decoration of this title depends on `level` and follows pattern of headers decorations in Markdown.

    title: str
        title to be printed out giving also a meaningful code separator;
    out: Any = True
        if `out` evaluates to True in flow control statements then `title` is printed out;
        if `out` evalueates to False then `title` is not printed, thus serves only as code separator;
        it's better to use `""` instead of `False` as it makes less "`title` obfuscation";
        after all any predicate may used what allows for some automation.
    vsep: int = 1
        number of empty lines above the title (when it's printed out);
    level: int = 1
        results in title decoration proper for given level (like in Markdown):
        0: underscore with '='
        1: underscore with '-' (default)
        2, 3, ... : '## ', '### ', ... before `title`
    """
    if out:  # i.e. print it out
        if vsep > 0:
            print("\n" * vsep, end="")
        if level > 1:
            print("#" * level, end=" ")
        print(title)
        if level == 1:
            print("-" * len(title))
        if level == 0:
            print("=" * len(title))
    else:
        # we want to have nice sections in the code
        # even if we not always want to print them out
        pass
