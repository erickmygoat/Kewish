#!/usr/bin/env python3
"""Measure solved plaintext against unsolved ciphertext.

Prints the statistics that decide what kind of cipher is in play, with the
uniform-random baseline alongside so each number can be read without
having to remember what 1/29 is.

Usage:  python3 -I scripts/report.py [--sources DIR]
"""
import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import stats                                   # noqa: E402
from lp.alphabet import RUNES, N                       # noqa: E402
from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402


def load_all(root, names, prefix=''):
    idx = []
    per = {}
    for n in names:
        p = RuneText.from_page(root, prefix + n)
        per[n] = p.indices
        idx.extend(p.indices)
    return idx, per


def block(title, idx):
    ioc = stats.index_of_coincidence(idx)
    chi = stats.chi_squared_uniform(idx)
    obs, exp, ratio = stats.doubles_rate(idx)
    print(f'{title}')
    print(f'  runes                {len(idx):,}')
    print(f'  index of coincidence {ioc:.5f}   (uniform = {1/N:.5f})')
    print(f'  chi^2 vs uniform     {chi:8.1f}   (df = {N-1}, random ~= {N-1})')
    print(f'  doubles rate         {obs:.5f}   expected {exp:.5f}  ratio {ratio:.2f}x')
    c = Counter(idx)
    tot = len(idx) or 1
    top = sorted(c.items(), key=lambda kv: -kv[1])[:3]
    bot = sorted(c.items(), key=lambda kv: kv[1])[:3]
    fmt = lambda kv: f'{RUNES[kv[0]]} {100*kv[1]/tot:.2f}%'
    print(f'  most common          {", ".join(fmt(k) for k in top)}')
    print(f'  least common         {", ".join(fmt(k) for k in bot)}')
    f_pct = 100 * c.get(0, 0) / tot
    print(f'  interrupt rune F     {f_pct:.2f}%   (uniform = {100/N:.2f}%)')
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()

    plain, _ = load_all(args.sources, SOLVED, prefix='solved_')
    cipher_solved, _ = load_all(args.sources, SOLVED)
    unsolved, per_page = load_all(args.sources, UNSOLVED)

    print('=' * 72)
    print('LIBER PRIMUS -- SOLVED PLAINTEXT vs UNSOLVED CIPHERTEXT')
    print('=' * 72)
    print()
    block('[A] solved pages, DECRYPTED (known English plaintext)', plain)
    block('[B] solved pages, as-printed (mixed: 4 of 9 are plaintext)', cipher_solved)
    block('[C] unsolved pages (56 pages)', unsolved)

    print('per-page breakdown of the unsolved material')
    print(f'  {"page":10s} {"runes":>6s} {"IoC":>8s} {"chi2":>8s} {"dbl ratio":>10s}')
    for name in UNSOLVED:
        idx = per_page[name]
        _, _, ratio = stats.doubles_rate(idx)
        print(f'  {name:10s} {len(idx):6d} {stats.index_of_coincidence(idx):8.5f} '
              f'{stats.chi_squared_uniform(idx):8.1f} {ratio:10.2f}')
    print()
    print(f'total unsolved runes: {len(unsolved):,}')
    print(f'total solved runes:   {len(plain):,}')


if __name__ == '__main__':
    sys.exit(main())
