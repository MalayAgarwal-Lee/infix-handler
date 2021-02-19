'''
(SLR Parser)
Grammar:

E' -> E
E -> E + T | E - T | T
T -> T * F | T / F | T % F | F
F -> ( E ) | ( UMINUS F ) | N
N -> N D | D
D -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

The HTML is obtained from http://jsmachines.sourceforge.net/machines/slr.html
'''
import re
from os import stat

import pandas as pd

from stack import Stack
from operators import OPERATORS


PRODUCTIONS = [
    ('E', 'E+T'), ('E', 'E-T'), ('E', 'T'),
    ('T', 'T*F'), ('T', 'T/F'), ('T', 'T%F'), ('T', 'F'),
    ('F', '(E)'), ('F', '(-F)'), ('F', 'N'),
    ('N', 'ND'), ('N', 'D'),
    ('D', '0'), ('D', '1'), ('D', '2'), ('D', '3'),
    ('D', '4'), ('D', '5'), ('D', '6'), ('D', '7'), ('D', '8'), ('D', '9')
]


def get_parse_tables(filename):
    with open(filename, 'r') as f:
        df = pd.read_html(f.read())[0]
        df = df.droplevel([0, 1], axis=1)
        df = df.drop(labels='State', axis=1)
        df = df.fillna('')
        return df.loc[:, '+':'$'], df.loc[:, 'E':]


class SLRParser:
    def __init__(self, string):
        self.action, self.goto = get_parse_tables('parse_table.html')
        self.string = string + '$'
        self.tokens = []
        self.token_indices = set()

    def get_numeric_token(self, index):
        length = len(self.string)
        end = index + 1
        while end < length and self.string[end] not in OPERATORS.keys():
            end += 1
        end = end - 1
        return self.string[index:end].replace(" ", ''), end

    def get_unary_op_token(self, char, index):
        end = self.string.find(' ', index)
        return self.string[index:end], end

    def update_tokens(self, char, index):
        if char == 'U':
            token, end = self.get_unary_op_token(char, index)
        elif char.isdigit():
            token, end = self.get_numeric_token(index)
        else:
            token, end =  char, index + 1

        self.tokens.append(token)
        self.token_indices.update({index for index in range(index, end)})

        increment = None

        if char == 'U':
            char = token
            increment = end - index + 1

        return char, increment

    def get_entry(self, tos, char):
        try:
            entry = self.action.iloc[tos][char]
        except IndexError:
            raise SyntaxError("Invalid character in expression")

        if not entry:
            raise SyntaxError("Invalid expression.")

        return entry

    def shift(self, entry, index, increment):
        return int(entry[1:]), index + increment

    def reduce(self, entry, s):
        prod_num = int(entry[1:])
        head, expansion = PRODUCTIONS[prod_num - 1]
        for _ in range(len(expansion)):
            s.pop()
        tos = s.tos()
        return int(self.goto.iloc[tos][head])

    def parse(self):
        s, string = Stack(), self.string
        s.push(0)

        i = 0

        while True:
            tos = s.tos()
            char = string[i]
            increment = 1

            if char.isspace():
                i += increment
                continue

            if i not in self.token_indices and char != '$':
                char, temp_inc = self.update_tokens(char, i)

                if temp_inc:
                    increment = temp_inc

            entry = self.get_entry(tos, char)
            if entry == 'acc':
                break

            if entry.startswith('s'):
                state, i = self.shift(entry, i, increment)
            else:
                state = self.reduce(entry, s)

            s.push(state)

        return self.tokens
