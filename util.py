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


class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


def infixToPostfix(infixexpr):
    prec = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in token in '0123456789':
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

