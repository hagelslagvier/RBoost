import re
from helpers.random import chance
from fuzzywuzzy import fuzz


def mask_text(text, degree):
    result = ""
    for char in text:
        result += char if chance(degree) else "_"

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

    return fuzz.ratio(left, right)


if "__main__" == __name__:
    l = "We looked at a lot of computers before buying this one, in order to compare prices."
    r = "We looked at a lot of computers before buying this one, in order to compare prices."

    print(compare(l, r))

    print(re.sub(r"[.?!:;,-]", "", l))
