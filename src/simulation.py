'''
Created on May 14, 2016

@author: eguo
'''

from __future__ import division

import itertools
import random

import enchant
from tqdm import tqdm

import pandas as pd


class ScrabbleSet:

    '''
    A set of letters matching Scrabble's distribution
    English edition contains 100 letter tiles
    Ignores 2 blank tiles, so this sim has 98 total
    '''

    def __init__(self):
        self.set = self.get_distribution()

    def reset(self):
        self.set = self.get_distribution()

    def get_distribution(self):
        a = ['a'] * 9
        b = ['b'] * 2
        c = ['c'] * 2
        d = ['d'] * 4
        e = ['e'] * 12
        f = ['f'] * 2
        g = ['g'] * 3
        h = ['h'] * 2
        i = ['i'] * 9
        j = ['j'] * 1
        k = ['k'] * 1
        l = ['l'] * 4
        m = ['m'] * 2
        n = ['n'] * 6
        o = ['o'] * 8
        p = ['p'] * 2
        q = ['q'] * 1
        r = ['r'] * 6
        s = ['s'] * 4
        t = ['t'] * 6
        u = ['u'] * 4
        v = ['v'] * 2
        w = ['w'] * 2
        x = ['x'] * 1
        y = ['y'] * 2
        z = ['z'] * 1

        letters = a + b + c + d + e + f + g + h + i + j + k + \
            l + m + n + o + p + q + r + s + t + u + v + w + x + y + z

        assert(len(letters) == 98), "Incorrect Scrabble Set"

        return letters

    def draw(self, num):
        draw = []
        for _ in xrange(num):
            l = random.choice(self.set)
            self.set.remove(l)
            draw.append(l)
        return draw

if __name__ == '__main__':
    sims = 5000
    word_length = 7
    word_tally = {}
    s = ScrabbleSet()
    d = enchant.Dict("en_US")

    for _ in tqdm(xrange(sims)):
        draw = s.draw(word_length)
        permutations = set(list(map("".join, itertools.permutations(draw))))
        for perm in permutations:
            if d.check(perm):
                if perm in word_tally:
                    word_tally[perm] += 1
                else:
                    word_tally[perm] = 1
        s.reset()
    table = pd.DataFrame.from_dict(word_tally, orient='index')
    table.rename(columns={0: 'tally'}, inplace=True)
    table = table.sort('tally', ascending=False).reset_index()
    table = table.rename(columns={'index': 'word'})
    print table
    table.to_clipboard()
