#!/usr/bin/env python3
"""Test autokey-family hypotheses suggested by the lag-1 repeat deficit.

The unsolved pages are uniform at every lag except lag 1, where adjacent
identical runes are suppressed by a factor of ~5 (z ~= -17). One cipher
family predicts exactly a lag-1-only constraint: ciphertext autokey.

Under C[i] = P[i] + C[i-1] (mod 29), two adjacent ciphertext runes are
equal precisely when P[i] == 0, i.e. the plaintext rune is F. So a low
doubles rate is forced, and recovery is trivial: P[i] = C[i] - C[i-1],
the first difference of the ciphertext.

This script runs that and its near relatives against every unsolved page,
scoring each with a null-calibrated English scorer. The same scorer is
first run on known plaintext and on known ciphertext so the numbers have
a scale.

Usage:  python3 -I scripts/autokey.py [--sources DIR] [--ngram 3]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402
from lp.score import Scorer                            # noqa: E402

N = 29


def ct_autokey(c, seed=0):
    """P[i] = C[i] - C[i-1]  (ciphertext autokey; first difference)."""
    out, prev = [], seed
    for v in c:
        out.append((v - prev) % N)
        prev = v
    return out


def ct_autokey_rev(c, seed=0):
    """P[i] = C[i-1] - C[i]  (opposite sign convention)."""
    out, prev = [], seed
    for v in c:
        out.append((prev - v) % N)
        prev = v
    return out


def pt_autokey(c, seed=0):
    """P[i] = C[i] - P[i-1]  (plaintext autokey)."""
    out, prev = [], seed
    for v in c:
        p = (v - prev) % N
        out.append(p)
        prev = p
    return out


def cumulative(c, seed=0):
    """P[i] = sum(C[0..i])  (inverse of first-differencing)."""
    out, acc = [], seed
    for v in c:
        acc = (acc + v) % N
        out.append(acc)
    return out


VARIANTS = {
    'ciphertext-autokey (1st diff)': ct_autokey,
    'ciphertext-autokey (reversed)': ct_autokey_rev,
    'plaintext-autokey': pt_autokey,
    'cumulative sum': cumulative,
    'identity (control)': lambda c, seed=0: list(c),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--ngram', type=int, default=3)
    args = ap.parse_args()

    sc = Scorer(os.path.join(args.sources, 'data'), n=args.ngram)

    print('=' * 78)
    print(f'AUTOKEY-FAMILY TEST   (English scorer: rune {args.ngram}-grams, '
          f'z vs uniform random)')
    print('=' * 78)
    print()
    print('calibration -- what the scorer says about text we already understand')
    known_plain = []
    for n in SOLVED:
        known_plain.extend(RuneText.from_page(args.sources, 'solved_' + n).indices)
    known_ct = []
    for n in ['0_welcome', 'jpg107-167', 'p56_an_end']:
        known_ct.extend(RuneText.from_page(args.sources, n).indices)
    print(f'  known English plaintext        z = {sc.z(known_plain):+7.2f}')
    print(f'  known ciphertext (3 enciphered)z = {sc.z(known_ct):+7.2f}')
    print()
    print('  A real break should land near the plaintext number, not the')
    print('  ciphertext one. Anything within a couple of sd of 0 is noise.')
    print()

    print('unsolved pages')
    names = list(VARIANTS)
    print(f'  {"page":10s} ' + ' '.join(f'{k.split()[0][:11]:>12s}' for k in names))
    best = (None, None, -1e9)
    for page in UNSOLVED:
        c = RuneText.from_page(args.sources, page).indices
        row = []
        for label, fn in VARIANTS.items():
            z = sc.z(fn(c))
            row.append(z)
            if z > best[2]:
                best = (page, label, z)
        print(f'  {page:10s} ' + ' '.join(f'{v:+12.2f}' for v in row))
    print()
    print(f'best cell: {best[1]} on {best[0]}  z = {best[2]:+.2f}')
    print()
    print('legend: columns are ' + '; '.join(names))


if __name__ == '__main__':
    sys.exit(main())
