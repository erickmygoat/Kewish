#!/usr/bin/env python3
"""Is there a repeating keyword of ANY length up to 500?

A keyword key (DIVINITY, FIRFUMFERENFE -- or SUNYATA, NAGARJUNA, ...) repeats
with period L. Runes L apart are then enciphered with the same shift, so they
coincide at the plaintext rate (~0.06) instead of 1/29 (~0.0345). This scans
every lag 1..500 inside each page (never across pages, in case the key resets
per page) and reports the strongest positive excess.

Calibrated first: solved English enciphered with random keywords of several
lengths, to show what a real period looks like at these text sizes.

Also re-run with every F removed, since interrupts (unencrypted F that do not
consume key) would smear a period.

Usage:  python3 -I scripts/periodicity.py [--sources DIR] [--maxlag 500]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import cipher                                  # noqa: E402
from lp.alphabet import N                              # noqa: E402
from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402


def lag_z(pages, lag):
    hits = pairs = 0
    for idx in pages:
        for a, b in zip(idx, idx[lag:]):
            pairs += 1
            hits += a == b
    if pairs == 0:
        return 0.0, 0
    p = 1 / N
    return (hits - pairs * p) / math.sqrt(pairs * p * (1 - p)), pairs


def scan(pages, maxlag):
    rows = [(lag, *lag_z(pages, lag)) for lag in range(1, maxlag + 1)]
    return sorted(rows, key=lambda r: -r[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--maxlag', type=int, default=500)
    args = ap.parse_args()
    rng = random.Random(3301)

    plain = []
    for n in SOLVED:
        plain.extend(RuneText.from_page(args.sources, 'solved_' + n).indices)

    print('=' * 70)
    print(f'PERIODICITY SCAN  (lags 1..{args.maxlag}, coincidences within pages)')
    print('=' * 70)
    print()
    print('calibration: solved English under a random keyword of length L')
    for L in (8, 13, 50, 150, 300):
        key = [rng.randrange(N) for _ in range(L)]
        ct = cipher.vigenere_encrypt(plain, key)
        z, _ = lag_z([ct], L)
        top = scan([ct], args.maxlag)[0]
        print(f'  L={L:3d}  z at true period = {z:+6.1f}   '
              f'strongest lag found = {top[0]} (z {top[1]:+.1f})')
    print()

    uns = [RuneText.from_page(args.sources, n).indices for n in UNSOLVED]
    no_f = [[v for v in p if v != 0] for p in uns]
    expect = math.sqrt(2 * math.log(args.maxlag))
    for label, pages in (('unsolved pages', uns), ('unsolved, all F removed', no_f)):
        res = scan(pages, args.maxlag)
        print(f'{label}: top 5 lags by positive excess')
        for lag, z, pairs in res[:5]:
            print(f'  lag {lag:4d}   z = {z:+5.2f}   ({pairs:,} pairs)')
        print(f'  (max z expected from noise alone over {args.maxlag} lags: '
              f'~{expect:.1f})')
        print()
    print('reading')
    print('  A real keyword shows a large z at its length (see calibration).')
    print('  If nothing on the unsolved pages beats what noise gives, no')
    print('  repeating keyword up to this length is in use -- whatever the word.')


if __name__ == '__main__':
    sys.exit(main())
