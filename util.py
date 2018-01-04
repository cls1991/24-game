# coding: utf8

"""
    Algorithms and some other tools for `24 Game`.
"""

from itertools import (
    permutations, product
)

EXPRESSIONS = ('((%d %s %d) %s %d) %s %d',
               '(%d %s %d) %s (%d %s %d)',
               '(%d %s (%d %s %d)) %s %d',
               '%d %s ((%d %s %d) %s %d)',
               '%d %s (%d %s (%d %s %d))'
               )

OPERATIONS = '+-*/'


def make24(seq):
    """Make up 24 points with a sep consisted of 4 elements."""
    result = []

    def check(ep):
        try:
            if abs(eval(ep) - 24.0) < 1e-10:
                return True
        except ZeroDivisionError:
            return False

        return False

    for dt in permutations(seq):
        for op in product(OPERATIONS, repeat=3):
            for p in EXPRESSIONS:
                exp = p % (dt[0], op[0], dt[1], op[1], dt[2], op[2], dt[3])
                if check(exp):
                    result.append(exp)

    return list(set(result))
