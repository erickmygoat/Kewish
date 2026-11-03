#!/usr/bin/env python3
"""Three checks that come straight from the book's own habits.

1. HEADINGS. The solved chapter reuses a small set of headings: A KOAN,
   AN INSTRUCTION, SOME WISDOM, KNOW THIS, WISDOM. Word boundaries survive
   encryption, so an unsolved heading can only be one of these if its word
   lengths match. No decryption needed.

2. PRIME SENTENCES. "Do not edit or change this book ... either the words or
   their numbers. For all is sacred." The Parable's three lines each sum to a
   prime. Is that design or coincidence? Compare the share of solved
   sentences with prime gematria sums against ordinary English sentences of
   the same length.

3. UNENCRYPTED RUNES. Three of the five enciphered solved pages leave plaintext
   F unencrypted. If the unsolved pages did the same with ANY rune r, r would be
   over-represented by roughly r's English frequency. Scan all 29.

Usage:  python3 -I scripts/theme_checks.py [--sources DIR] [--iddqd DIR]
"""
import argparse
import math
import os
import random
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import gematria as g                           # noqa: E402
from lp.alphabet import INDEX, RUNES, LETTERS, N, is_rune   # noqa: E402
from lp.runetext import RuneText, SOLVED, UNSOLVED     # noqa: E402
from lp.translit import to_runes                       # noqa: E402

LP1_HEADINGS = ['A KOAN', 'AN INSTRUCTION', 'SOME WISDOM', 'KNOW THIS', 'WISDOM',
                'A WARNING', 'WELCOME', 'THE LOSS OF DIVINITY', 'AN END',
                'PARABLE', 'A PARABLE']


def pattern(words):
    return tuple(len(w) for w in words)


def sentences(path):
    txt = open(path, encoding='utf-8').read().replace('\n', '')
    out, cur = [], []
    for ch in txt:
        if is_rune(ch):
            cur.append(ch)
        elif ch in '⁘⁜' and cur:
            out.append(''.join(cur))
            cur = []
    if cur:
        out.append(''.join(cur))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--iddqd', default='/home/user/rtkd/iddqd')
    args = ap.parse_args()
    rng = random.Random(3301)

    print('=' * 78)
    print('1. UNSOLVED HEADINGS vs THE SOLVED CHAPTER\'S HEADINGS (word lengths in runes)')
    print('=' * 78)
    known = {pattern(to_runes(w) for w in h.split()): h for h in LP1_HEADINGS}
    for k, h in sorted(known.items(), key=lambda kv: kv[1]):
        print(f'  solved   {str(k):16s} {h}')
    idx = open(os.path.join(args.iddqd, 'liber-primus__index',
                            'liber-primus__index.txt'), encoding='utf-8').read()
    hits = 0
    for line in idx.splitlines():
        m = re.match(r'\s*(0\.\d+\.\d+)\s+([ᚠ-ᛸ ]+)\s+\(', line)
        if not m:
            continue
        words = m.group(2).split()
        pat = pattern(words)
        match = known.get(pat)
        hits += bool(match)
        print(f'  UNSOLVED {str(pat):16s} {m.group(1):7s} {" ".join(words):34s} '
              f'{"<-- could be " + match if match else "no solved heading fits"}')
    print(f'  -> {hits} unsolved heading(s) share a word-length pattern with a solved one.')
    print()

    print('=' * 78)
    print('2. ARE SENTENCE SUMS PRIME BY DESIGN?')
    print('=' * 78)
    corpus_words = []
    with open(os.path.join(args.sources, 'data', 'baseline-rune-words.txt'),
              encoding='utf-8') as f:
        for line in f:
            w = ''.join(ch for ch in line if is_rune(ch))
            if w:
                corpus_words.append(w)
    corpus_words = corpus_words[:400000]

    def null_rate(length, trials=300):
        """Share of ordinary English word-runs of ~`length` runes with a prime sum."""
        hits = 0
        for _ in range(trials):
            i = rng.randrange(len(corpus_words) - 60)
            s, k = '', i
            while len(s) < length:
                s += corpus_words[k]
                k += 1
            hits += g.is_prime(g.value(s))
        return hits / trials

    tot_obs = tot_exp = tot_n = 0
    print(f'  {"page":20s} {"sentences":>9s} {"prime":>6s} {"expected":>9s}')
    for n in SOLVED:
        sents = sentences(os.path.join(args.sources, 'pages', f'solved_{n}.txt'))
        sents = [s for s in sents if len(s) >= 3]
        obs = sum(g.is_prime(g.value(s)) for s in sents)
        exp = sum(null_rate(len(s), 120) for s in sents)
        tot_obs += obs
        tot_exp += exp
        tot_n += len(sents)
        print(f'  {n:20s} {len(sents):9d} {obs:6d} {exp:9.1f}')
    p0 = tot_exp / tot_n
    sd = math.sqrt(tot_n * p0 * (1 - p0))
    print(f'  {"ALL SOLVED":20s} {tot_n:9d} {tot_obs:6d} {tot_exp:9.1f}   '
          f'z = {(tot_obs - tot_exp) / sd:+.1f}')
    # the unsolved CIPHERTEXT, against random runes of the same lengths
    u_obs = u_exp = u_n = 0
    for n in UNSOLVED:
        for s in sentences(os.path.join(args.sources, 'pages', f'{n}.txt')):
            if len(s) < 3:
                continue
            u_n += 1
            u_obs += g.is_prime(g.value(s))
            u_exp += sum(g.is_prime(sum(g.PRIMES[rng.randrange(N)] for _ in s))
                         for _ in range(40)) / 40
    sd_u = math.sqrt(u_n * (u_exp / u_n) * (1 - u_exp / u_n))
    print(f'  {"unsolved ciphertext":20s} {u_n:9d} {u_obs:6d} {u_exp:9.1f}   '
          f'z = {(u_obs - u_exp) / sd_u:+.1f}  (vs random runes)')
    print()

    print('=' * 78)
    print('3. IS ANY RUNE LEFT UNENCRYPTED IN THE UNSOLVED PAGES?')
    print('=' * 78)
    plain = []
    for n in SOLVED:
        plain.extend(RuneText.from_page(args.sources, 'solved_' + n).indices)
    fE = Counter(plain)
    uns = []
    for n in UNSOLVED:
        uns.extend(RuneText.from_page(args.sources, n).indices)
    cU = Counter(uns)
    T = len(uns)
    rows = []
    for r in range(N):
        f = fE[r] / len(plain)
        obs = cU[r] / T
        base = 1 / N
        exp_if = base * (1 - f) + f
        sd = math.sqrt(base * (1 - base) / T)
        rows.append(((obs - base) / sd, (obs - exp_if) / sd, r, obs, exp_if))
    rows.sort(reverse=True)
    print(f'  {"rune":6s} {"seen":>7s} {"if left plain":>14s} {"z vs chance":>12s} {"z vs plain-rule":>16s}')
    for z0, z1, r, obs, e in rows[:5]:
        print(f'  {RUNES[r]} {LETTERS[RUNES[r]]:4s} {100*obs:6.2f}% {100*e:13.2f}% '
              f'{z0:+12.1f} {z1:+16.1f}')
    print(f'  ... chance is {100/N:.2f}% for every rune; max of 29 random z-scores is ~+2')
    print('  A rune left unencrypted would sit near its "if left plain" share, i.e.')
    print('  well above chance. Frequent English runes would stick out by 10+ sd.')


if __name__ == '__main__':
    sys.exit(main())
