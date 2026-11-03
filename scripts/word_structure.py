#!/usr/bin/env python3
"""Does a rune stand for a letter, or for a whole word?

Hypothesis tested: "maybe a rune means a whole word" (a codebook / logogram
reading). The unsolved pages keep word separators (•). If those separators
are real plaintext word boundaries and each rune is roughly one letter, the
distribution of word LENGTHS in runes should match English. Under a
rune-per-word reading, each separated group would be a phrase, and matching
English word lengths would be a coincidence.

Second check: one-rune words. In English rune text these are almost all A
or I, so under any FIXED rune meaning they would pile onto two or three
runes. Under a key that changes every position they spread across all 29.

Usage:  python3 -I scripts/word_structure.py [--sources DIR]
"""
import argparse
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp.alphabet import RUNES, is_rune, to_letters     # noqa: E402
from lp.runetext import SOLVED, UNSOLVED               # noqa: E402

MAXLEN = 12


def words_from_page(path):
    """Join lines (lines split words), then split on any non-rune glyph.
    Tokens containing digits/latin (the numeric pages) fall away naturally
    because they contain no runes."""
    txt = open(path, encoding='utf-8').read().replace('\n', '').replace('\r', '')
    out, cur = [], []
    for ch in txt:
        if is_rune(ch):
            cur.append(ch)
        else:
            if cur:
                out.append(''.join(cur))
            cur = []
    if cur:
        out.append(''.join(cur))
    return out


def length_dist(words):
    c = Counter(min(len(w), MAXLEN) for w in words)
    n = sum(c.values()) or 1
    return [c.get(k, 0) / n for k in range(1, MAXLEN + 1)]


def tvd(a, b):
    return 0.5 * sum(abs(x - y) for x, y in zip(a, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()
    pages = os.path.join(args.sources, 'pages')

    eng = []
    with open(os.path.join(args.sources, 'data', 'baseline-rune-words.txt'),
              encoding='utf-8') as f:
        for line in f:
            w = ''.join(ch for ch in line if is_rune(ch))
            if w:
                eng.append(w)
    solved = []
    for n in SOLVED:
        solved += words_from_page(os.path.join(pages, f'solved_{n}.txt'))
    uns = []
    for n in UNSOLVED:
        uns += words_from_page(os.path.join(pages, f'{n}.txt'))

    # Null: same total rune count, boundaries placed at random with the
    # same mean word length (geometric lengths).
    rng = random.Random(3301)
    mean_len = sum(len(w) for w in uns) / len(uns)
    p_break = 1 / mean_len
    null = []
    cur = 0
    for _ in range(sum(len(w) for w in uns)):
        cur += 1
        if rng.random() < p_break:
            null.append('x' * cur)
            cur = 0

    E, S, U, R = (length_dist(x) for x in (eng, solved, uns, null))

    print('=' * 74)
    print('WORD STRUCTURE: letter-per-rune vs word-per-rune')
    print('=' * 74)
    print()
    print(f'words:  English corpus {len(eng):,}   solved {len(solved):,}   '
          f'unsolved {len(uns):,}')
    print(f'mean length (runes): English {sum(map(len,eng))/len(eng):.2f}   '
          f'solved {sum(map(len,solved))/len(solved):.2f}   unsolved {mean_len:.2f}')
    print()
    print(f'{"len":>4s} {"English":>9s} {"solved":>9s} {"unsolved":>9s} '
          f'{"random-break null":>18s}')
    for k in range(MAXLEN):
        lab = f'{k+1}' if k + 1 < MAXLEN else f'{MAXLEN}+'
        print(f'{lab:>4s} {100*E[k]:8.1f}% {100*S[k]:8.1f}% {100*U[k]:8.1f}% '
              f'{100*R[k]:17.1f}%')
    print()
    print('total variation distance from English (0 = identical, 1 = disjoint)')
    print(f'  solved plaintext   {tvd(S, E):.3f}')
    print(f'  unsolved pages     {tvd(U, E):.3f}')
    print(f'  random-break null  {tvd(R, E):.3f}')
    print()

    def one_rune(words):
        return Counter(w for w in words if len(w) == 1)

    for label, ws in (('solved plaintext', solved), ('unsolved', uns)):
        c = one_rune(ws)
        tot = sum(c.values())
        top = ', '.join(f'{r}={to_letters(r)}:{n}' for r, n in c.most_common(5))
        print(f'one-rune words, {label}: {tot} tokens over {len(c)} distinct '
              f'runes   top: {top}')
    print()
    print('reading')
    print('  If unsolved word lengths track English far closer than the random')
    print('  null, the separators are real word boundaries and a rune is a')
    print('  letter-sized unit, not a word. Spread-out one-rune words mean the')
    print('  meaning of a rune changes with position, i.e. there is a key.')


if __name__ == '__main__':
    sys.exit(main())
