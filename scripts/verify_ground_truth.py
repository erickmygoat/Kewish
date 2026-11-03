#!/usr/bin/env python3
"""Decrypt every solved Liber Primus page and diff against the known answer.

This is the toolkit's calibration harness. Nothing measured on the unsolved
pages means anything unless the same code reproduces the pages whose answers
are already public -- so this runs first and exits non-zero on any mismatch.

Usage:  python3 -I scripts/verify_ground_truth.py [--sources DIR]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import cipher, keystream                      # noqa: E402
from lp.runetext import RuneText, SOLVED              # noqa: E402

DIVINITY = [23, 10, 1, 10, 9, 10, 16, 26]
FIRFUMFERENFE = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

# Published solutions. `kind` records how the page is protected, which is
# worth separating: four of the nine solved pages are not enciphered at all,
# they are plain rune-for-letter text.
SOLUTIONS = {
    '0_warning':          dict(kind='atbash',  invert=True),
    '0_welcome':          dict(kind='vigenere', key=DIVINITY,
                               interrupts={4, 5, 6, 7, 10, 11, 14, 18, 20, 21, 25}),
    '0_wisdom':           dict(kind='plain'),
    '0_koan_1':           dict(kind='atbash+vigenere', invert=True, key=[26]),
    '0_loss_of_divinity': dict(kind='plain'),
    'jpg107-167':         dict(kind='vigenere', key=FIRFUMFERENFE,
                               interrupts={2, 3}),
    'jpg229':             dict(kind='plain'),
    'p56_an_end':         dict(kind='sequence', seq='totient_of_primes',
                               interrupts={4}),
    'p57_parable':        dict(kind='plain'),
}


def decrypt(page, spec):
    idx = page.indices
    if spec.get('invert'):
        idx = cipher.invert(idx)
    if spec['kind'] == 'sequence':
        stream = keystream.totient_of_primes()
        idx = cipher.sequence_decrypt(idx, stream, spec.get('interrupts'))
    elif spec.get('key'):
        idx = cipher.vigenere_decrypt(idx, spec['key'], spec.get('interrupts'))
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground',
                    help='clone of relikd/LiberPrayground')
    args = ap.parse_args()

    ok = True
    print(f'{"page":22s} {"protection":16s} {"runes":>6s}  result')
    print('-' * 72)
    for name in SOLVED:
        spec = SOLUTIONS[name]
        page = RuneText.from_page(args.sources, name)
        expect = RuneText.from_page(args.sources, 'solved_' + name)
        got = decrypt(page, spec)

        if len(got) != len(expect.indices):
            print(f'{name:22s} {spec["kind"]:16s} {len(got):6d}  '
                  f'LENGTH MISMATCH (expected {len(expect.indices)})')
            ok = False
            continue
        bad = [i for i, (a, b) in enumerate(zip(got, expect.indices)) if a != b]
        if bad:
            print(f'{name:22s} {spec["kind"]:16s} {len(got):6d}  '
                  f'MISMATCH at {len(bad)} runes (first @{bad[0]})')
            ok = False
        else:
            head = page.with_indices(got).render().replace('\n', ' ')[:38]
            print(f'{name:22s} {spec["kind"]:16s} {len(got):6d}  OK  "{head.strip()}"')

    print('-' * 72)
    print('ALL SOLVED PAGES REPRODUCED' if ok else 'FAILURES PRESENT')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
