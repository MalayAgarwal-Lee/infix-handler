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


def parse(string):
    s = Stack()
    s.push(0)

    string = string + '$'

    action, goto = get_parse_tables('parse_table.html')
    i = 0

    while True:
        tos = s.tos()
        char = string[i]
        increment = 1

        if char.isspace():
            i += increment
            continue

        if char == 'U':
            end = string.find(' ', i)
            char = string[i:end]
            increment = end - i + 1

        try:
            entry = action.iloc[tos][char]
        except IndexError:
            raise SyntaxError("Invalid character in expression")

        if not entry:
            raise SyntaxError("Invalid expression.")

        if entry == 'acc':
            break

        if entry.startswith('s'):
            state = int(entry[1:])
            i += increment
        else:
            prod_num = int(entry[1:])
            head, expansion = PRODUCTIONS[prod_num - 1]
            for _ in range(len(expansion)):
                s.pop()
            tos = s.tos()
            state = int(goto.iloc[tos][head])

        s.push(state)
