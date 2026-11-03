#!/usr/bin/env python3
"""Quantify the adjacent-repeat deficit in the unsolved pages.

Every first-order statistic on the unsolved material is flat: the rune
histogram is uniform and the index of coincidence sits exactly on 1/29.
One second-order statistic is not. Adjacent identical runes are far rarer
than chance. This script measures that deficit and its significance, and
checks whether it also shows up across word boundaries and at a lag of 2+
(which separates "the generator avoided doubles" from "the text has
structure at distance 1 only").

Usage:  python3 -I scripts/doubles.py [--sources DIR]
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp.alphabet import N                              # noqa: E402
from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402


def lag_repeats(idx, lag):
    pairs = len(idx) - lag
    if pairs <= 0:
        return 0, 0
    hits = sum(1 for a, b in zip(idx, idx[lag:]) if a == b)
    return hits, pairs


def binom_z(hits, pairs, p=1.0 / N):
    if pairs == 0:
        return 0.0
    mu = pairs * p
    sd = math.sqrt(pairs * p * (1 - p))
    return (hits - mu) / sd if sd else 0.0


def analyse(label, idx, max_lag=6):
    print(f'{label}  ({len(idx):,} runes)')
    print(f'  {"lag":>4s} {"observed":>9s} {"expected":>9s} {"ratio":>7s} {"z":>9s}')
    for lag in range(1, max_lag + 1):
        hits, pairs = lag_repeats(idx, lag)
        mu = pairs / N
        z = binom_z(hits, pairs)
        print(f'  {lag:4d} {hits:9d} {mu:9.1f} {hits/mu if mu else 0:7.2f} {z:9.2f}')
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()

    def load(names, prefix=''):
        out = []
        for n in names:
            out.extend(RuneText.from_page(args.sources, prefix + n).indices)
        return out

    print('=' * 64)
    print('ADJACENT-REPEAT ANALYSIS')
    print('=' * 64)
    print()
    analyse('[A] solved pages, decrypted English plaintext', load(SOLVED, 'solved_'))
    analyse('[C] unsolved pages', load(UNSOLVED))

    print('interpretation key')
    print('  ratio ~ 1.00, |z| < 3   consistent with a uniform independent stream')
    print('  ratio < 1 at lag 1 only generator avoided ADJACENT equal output')
    print('  ratio < 1 at many lags  wider structure, not a doubles rule')


if __name__ == '__main__':
    sys.exit(main())
