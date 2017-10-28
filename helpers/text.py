#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from helpers import chance
from fuzzywuzzy import fuzz


def mask_text(text, degree):
    result = ""
    for char in text:
        result += char if chance.chance(degree) else "_"

    return result


def compare(left, right):
    strings = []
    for string in [left, right]:
        string = string.lower()
        string = string.split()
        string = " ".join(string)
        string = re.sub(r"[.?!:;,-]", "", string)
        strings.append(string)

    left, right = strings

    return fuzz.token_set_ratio(left, right)


if "__main__" == __name__:
    l = "Because I'm Batman"
    r = "because I am   Batman"

    print(compare(l, r))

    print(re.sub(r"[.?!:;,-]", "", l))
