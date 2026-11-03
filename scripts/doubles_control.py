#!/usr/bin/env python3
"""Control test: is the lag-1 repeat deficit special to the unsolved pages?

The unsolved pages suppress adjacent identical runes by ~5x. Before reading
anything into that, check the enciphered pages whose answers are known. If
their CIPHERTEXT also suppresses doubles, the effect belongs to how Liber
Primus was written or transcribed, and says nothing about the unsolved
cipher. If their ciphertext sits at chance, the deficit is a real property
of the unsolved material.

Usage:  python3 -I scripts/doubles_control.py [--sources DIR]
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402

N = 29

# Which solved pages are actually enciphered (vs printed as plain runes).
ENCIPHERED = {'0_warning', '0_welcome', '0_koan_1', 'jpg107-167', 'p56_an_end'}


def doubles(idx):
    pairs = len(idx) - 1
    if pairs <= 0:
        return 0, 0, 0.0, 0.0
    hits = sum(1 for a, b in zip(idx, idx[1:]) if a == b)
    mu = pairs / N
    sd = math.sqrt(pairs * (1 / N) * (1 - 1 / N))
    return hits, pairs, (hits / mu if mu else 0), ((hits - mu) / sd if sd else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()

    print('=' * 76)
    print('CONTROL: adjacent-repeat rate, page by page')
    print('=' * 76)
    print()
    print(f'{"page":22s} {"kind":11s} {"runes":>6s} {"obs":>5s} {"exp":>7s} '
          f'{"ratio":>6s} {"z":>7s}')
    print('-' * 76)

    print('SOLVED, as printed (ciphertext where enciphered):')
    for n in SOLVED:
        idx = RuneText.from_page(args.sources, n).indices
        h, p, r, z = doubles(idx)
        kind = 'enciphered' if n in ENCIPHERED else 'plain'
        print(f'  {n:20s} {kind:11s} {len(idx):6d} {h:5d} {p/N:7.1f} '
              f'{r:6.2f} {z:7.2f}')

    print()
    print('SOLVED, decrypted (English plaintext):')
    agg_h = agg_p = 0
    for n in SOLVED:
        idx = RuneText.from_page(args.sources, 'solved_' + n).indices
        h, p, r, z = doubles(idx)
        agg_h += h
        agg_p += p
        print(f'  {n:20s} {"plaintext":11s} {len(idx):6d} {h:5d} {p/N:7.1f} '
              f'{r:6.2f} {z:7.2f}')

    print()
    print('UNSOLVED:')
    for n in UNSOLVED:
        idx = RuneText.from_page(args.sources, n).indices
        h, p, r, z = doubles(idx)
        print(f'  {n:20s} {"unknown":11s} {len(idx):6d} {h:5d} {p/N:7.1f} '
              f'{r:6.2f} {z:7.2f}')

    print()
    print('-' * 76)
    enc = []
    for n in SOLVED:
        if n in ENCIPHERED:
            enc.extend(RuneText.from_page(args.sources, n).indices)
    uns = []
    for n in UNSOLVED:
        uns.extend(RuneText.from_page(args.sources, n).indices)
    for label, idx in [('enciphered solved ciphertext (pooled)', enc),
                       ('unsolved (pooled)', uns)]:
        h, p, r, z = doubles(idx)
        print(f'{label:40s} runes={len(idx):6d} ratio={r:5.2f} z={z:+7.2f}')


if __name__ == '__main__':
    sys.exit(main())
