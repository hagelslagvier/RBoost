#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


def chance(probability):
    if not 0 <= probability <= 1:
        raise ValueError("incorrect probability value: {}".format(probability))

    return random.random() < probability


def mask_text(text, degree):
    result = ""
    for char in text:
        result += char if chance(degree) else "_"

    return result

if "__main__" == __name__:
    for idx in range(10):
        print(chance(0.5))