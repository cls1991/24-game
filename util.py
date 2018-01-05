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
               '%d %s (%d %s (%d %s %d))')

OPERATIONS = '+-*/'


def make24(seq):
    """Make up 24 points with a sep consisted of 4 elements."""

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
                    return exp

    return ''


class Stack:
    def __init__(self):
        self.items = []

    def empty(self):
        return not self.items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.empty():
            return self.items.pop()
        return ''

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


def infix2postfix(infix_expr):
    """convert infix notation to postfix notation."""
    priorities = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    op_stack = Stack()
    postfix_list = []

    def greater(tk):
        try:
            priority_a = priorities[op_stack.peek()]
            property_b = priorities[tk]
            return True if priority_a > property_b else False
        except KeyError:
            return False

    for token in infix_expr:
        if token.isdigit():
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token and top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while not op_stack.empty() and greater(token):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.empty():
        postfix_list.append(op_stack.pop())

    return ' '.join(postfix_list)
