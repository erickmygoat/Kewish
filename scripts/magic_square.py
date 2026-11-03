#!/usr/bin/env python3
"""Verify the three Liber Primus magic squares and the 'An End' hash.

Cicada asked 2014 solvers to submit "the three magic squares". Accounts
quote both 3301 and 1033 as the constant; they are describing different
squares. This computes all three directly. The SOME WISDOM square mixes
words and numbers: each word is replaced by its Gematria Primus value.

Usage:  python3 -I scripts/magic_square.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import gematria as g                           # noqa: E402

# The 5x5 grid on the "AN INSTRUCTION ... KNOW THIS" page (229.jpg),
# transcribed in relikd/LiberPrayground `_solved.txt`.
SQUARE_5 = [
    [434, 1311, 312, 278, 966],
    [204,  812, 934, 280, 1071],
    [626,  620, 809, 620, 626],
    [1071, 280, 934, 812, 204],
    [966,  278, 312, 1311, 434],
]

# "SOME WISDOM ... KNOW THIS": words stand for their gematria values.
SQUARE_WORDS = [
    ['272', '138', 'SHADOWS', '131', '151'],
    ['AETHEREAL', 'BUFFERS', 'VOID', 'CARNAL', '18'],
    ['226', 'OBSCURA', 'FORM', '245', 'MOBIUS'],
    ['18', 'ANALOG', 'VOID', 'MOURNFUL', 'AETHEREAL'],
    ['151', '131', 'CABAL', '138', '272'],
]

# 7x7 hidden in onion5.mp3 (OpenPuff), as posted in #cicadasolvers.
SQUARE_7 = [
    [7, 375, 236, 190, 27, 17, 181],
    [351, 223, 14, 47, 293, 98, 7],
    [456, 232, 121, 114, 72, 23, 15],
    [16, 65, 270, 331, 270, 65, 16],
    [15, 23, 72, 114, 121, 232, 456],
    [7, 98, 293, 47, 14, 223, 351],
    [181, 17, 27, 190, 236, 375, 7],
]


def words_to_numbers(grid):
    from lp.translit import to_runes
    return [[int(c) if c.isdigit() else g.value(to_runes(c)) for c in row]
            for row in grid]


# The SHA-512 hash quoted on the "An End" page. The page that hashes to this
# has never been found -- it is the puzzle's outstanding open bounty.
AN_END_HASH = ('36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618'
               'dee09a8425893dc7500b464fdaf1672d7bef5e891c6e227456892'
               '6a49fb4f45132c2a8b4')


def check(square, name):
    n = len(square)
    rows = [sum(r) for r in square]
    cols = [sum(square[i][j] for i in range(n)) for j in range(n)]
    d1 = sum(square[i][i] for i in range(n))
    d2 = sum(square[i][n - 1 - i] for i in range(n))
    all_sums = rows + cols + [d1, d2]
    target = rows[0]

    print(f'{name} ({n}x{n})')
    for r in square:
        print('  ' + ' '.join(f'{v:5d}' for v in r) + f'   = {sum(r)}')
    print('  ' + ' '.join(f'{v:5d}' for v in cols) + '   <- column sums')
    print(f'  diagonals: {d1}, {d2}')
    magic = len(set(all_sums)) == 1
    print(f'  magic: {magic}   constant: {target}')
    print(f'  constant is prime: {g.is_prime(target)}'
          f'   emirp: {g.is_emirp(target)}'
          f'   reverse: {g.reverse(target)}')
    print(f'  centre cell: {square[n//2][n//2]}')
    print(f'  grid is symmetric under 180 deg rotation: '
          f'{square == [row[::-1] for row in square[::-1]]}')
    print()
    return magic, target


def main():
    print('=' * 70)
    print('MAGIC SQUARE / HASH VERIFICATION')
    print('=' * 70)
    print()
    magic, target = check(SQUARE_5, 'Liber Primus 5x5, "AN INSTRUCTION" page')
    check(words_to_numbers(SQUARE_WORDS), 'Liber Primus 5x5, "SOME WISDOM" '
          '(words -> gematria)')
    check(SQUARE_7, '7x7 from onion5.mp3')

    print('distinct values and 3301-complements')
    vals = sorted({v for r in SQUARE_5 for v in r})
    print(f'  {len(vals)} distinct values in a 25-cell grid: {vals}')
    print('  3301 - v, and whether that complement is prime:')
    for v in vals:
        c = 3301 - v
        print(f'    3301 - {v:4d} = {c:4d}   prime: {g.is_prime(c)}')
    print()

    print('"An End" hash')
    print(f'  hex length {len(AN_END_HASH)} chars = {len(AN_END_HASH)*4} bits '
          f'-> {"SHA-512" if len(AN_END_HASH)==128 else "unknown"}')
    print(f'  value: {AN_END_HASH[:32]}...')
    print('  The page hashing to this has never been located.')


if __name__ == '__main__':
    sys.exit(main())
