#!/usr/bin/env python3
"""Validate the gematria implementation against Cicada's own published sums.

relikd/LiberPrayground's `_solved.txt` annotates each decrypted sentence with
its gematria value, e.g.  "A__ WARNNG# = 332". Those values come from the
solver community, independent of this code, so reproducing them is a real
check on the prime table and the summing rule -- not a tautology.

Also reports the number-theoretic properties the puzzle keeps invoking.

Usage:  python3 -I scripts/gematria_check.py [--sources DIR]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import gematria as g                           # noqa: E402
from lp.alphabet import PRIMES, RUNES                  # noqa: E402

RUNE_RE = re.compile(r'[ᚠ-ᛸ]')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()

    print('=' * 70)
    print('GEMATRIA PRIMUS')
    print('=' * 70)
    print()
    print('rune : prime  (the first 29 primes, in alphabet order)')
    for i in range(0, 29, 6):
        row = [f'{RUNES[j]}={PRIMES[j]:3d}' for j in range(i, min(i + 6, 29))]
        print('  ' + '  '.join(row))
    print(f'\n  sum of all 29 primes = {sum(PRIMES)}')
    print()

    # Validate against published per-sentence sums.
    path = os.path.join(args.sources, '_solved.txt')
    checked = ok = 0
    failures = []
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    # Format is: a rune line, then its transliteration annotated "= <sum>".
    # Pair each rune line with the NEXT annotation line, not a preceding one.
    for i, line in enumerate(lines):
        runes = ''.join(RUNE_RE.findall(line))
        if not runes:
            continue
        claimed = None
        for k in range(i + 1, min(i + 3, len(lines))):
            if RUNE_RE.search(lines[k]):
                break
            m = re.search(r'=\s*(\d+)', lines[k])
            if m:
                claimed = int(m.group(1))
                break
        if claimed is None:
            continue
        got = g.value(runes)
        checked += 1
        if got == claimed:
            ok += 1
        else:
            failures.append((line[:28], claimed, got))

    print(f'published-sum validation: {ok}/{checked} sentences match')
    if failures[:5]:
        print('  first mismatches:')
        for r, c, gt in failures[:5]:
            print(f'    {r}  claimed {c}  computed {gt}')
    print()

    print('number-theoretic properties the puzzle invokes')
    for n in (3301, 1033, 761, 1595, 29, 109):
        props = []
        if g.is_prime(n):
            props.append('prime')
        if g.is_emirp(n):
            props.append(f'emirp (reverse {g.reverse(n)} also prime)')
        props.append(f'phi={g.totient(n)}')
        print(f'  {n:5d}  ' + ', '.join(props))
    print()
    print('  3301 is the 464th prime; 1033 is its digit rotation and also prime.')
    print(f'  totient stream phi(p) mod 29 for first 12 primes: '
          f'{g.rune_totient_stream([2,3,5,7,11,13,17,19,23,29,31,37])}')


if __name__ == '__main__':
    sys.exit(main())
