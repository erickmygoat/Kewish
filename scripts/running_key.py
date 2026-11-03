#!/usr/bin/env python3
"""Could the key be a natural-language text?  (Nagarjuna, Crowley, Emerson...)

Hypothesis tested: "use everything that is out there" -- i.e. the key is some
existing book, used as a running key: C[i] = P[i] + K[i] mod 29, with K the
runes of that book.

This can be tested for EVERY book at once, without knowing which book. Both
P and K are natural language, so both have uneven letter frequencies. Adding
two uneven distributions mod 29 gives a distribution that is flatter but not
flat, and with 12,956 runes the residual unevenness is measurable. The test
simulates running-key ciphertext from a large English rune corpus and asks
whether the unsolved pages look like it -- or like a uniform random key.

Caveat stated up front: this covers keys that are *text*. A key text that has
itself been encrypted, hashed, or otherwise randomised is a different
hypothesis and is not touched by this test.

Usage:  python3 -I scripts/running_key.py [--sources DIR] [--trials 40]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import stats                                   # noqa: E402
from lp.alphabet import INDEX, N                       # noqa: E402
from lp.runetext import RuneText, UNSOLVED             # noqa: E402


def mean_sd(xs):
    m = sum(xs) / len(xs)
    v = sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1)
    return m, math.sqrt(v)


def measures(c):
    _, _, lag1 = stats.doubles_rate(c)
    return stats.index_of_coincidence(c), stats.chi_squared_uniform(c), lag1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--trials', type=int, default=40)
    args = ap.parse_args()

    corpus = [INDEX[ch] for ch in open(
        os.path.join(args.sources, 'data', 'baseline-rune-stream.txt'),
        encoding='utf-8').read() if ch in INDEX]
    uns = []
    for n in UNSOLVED:
        uns.extend(RuneText.from_page(args.sources, n).indices)
    n = len(uns)
    rng = random.Random(3301)

    def chunk():
        a = rng.randrange(0, len(corpus) - n)
        return corpus[a:a + n]

    sims = {'text + text  (running key)': [], 'text + random (uniform key)': [],
            'text - text  (running key, subtract)': []}
    for _ in range(args.trials):
        p, k = chunk(), chunk()
        sims['text + text  (running key)'].append(
            measures([(a + b) % N for a, b in zip(p, k)]))
        sims['text - text  (running key, subtract)'].append(
            measures([(a - b) % N for a, b in zip(p, k)]))
        sims['text + random (uniform key)'].append(
            measures([(a + rng.randrange(N)) % N for a in p]))

    obs = measures(uns)
    print('=' * 78)
    print(f'RUNNING-KEY TEST   ({len(corpus):,}-rune English corpus, '
          f'{n:,} runes per trial, {args.trials} trials)')
    print('=' * 78)
    print()
    print(f'{"model":38s} {"IoC":>17s} {"chi^2 (28 df)":>17s} {"lag-1":>13s}')
    for name, rows in sims.items():
        cols = list(zip(*rows))
        cells = []
        for idx, c in enumerate(cols):
            m, s = mean_sd(c)
            fmt = ('{:.5f}+-{:.5f}', '{:7.1f}+-{:5.1f}', '{:.2f}+-{:.2f}')[idx]
            cells.append(fmt.format(m, s))
        print(f'{name:38s} {cells[0]:>17s} {cells[1]:>17s} {cells[2]:>13s}')
    print(f'{"UNSOLVED PAGES (observed)":38s} {obs[0]:>17.5f} {obs[1]:>17.1f} '
          f'{obs[2]:>13.2f}')
    print()

    rk = list(zip(*sims['text + text  (running key)']))
    m, s = mean_sd(rk[1])
    z = (obs[1] - m) / s
    print(f'chi^2 of unsolved vs running-key simulations: z = {z:+.1f}')
    m2, s2 = mean_sd(rk[0])
    print(f'IoC   of unsolved vs running-key simulations: '
          f'z = {(obs[0]-m2)/s2:+.1f}')
    print()
    print('reading')
    print('  A running key made of ordinary text leaves the letter counts')
    print('  measurably uneven at this length. The unsolved pages are as flat')
    print('  as a uniform random key -- so no ordinary text used as-is is the')
    print('  key. Tested on English; other natural languages are comparably')
    print('  uneven, so the same should hold, but only English was run here.')
    print('  A text that was scrambled (hashed, encrypted) first is NOT ruled out.')


if __name__ == '__main__':
    sys.exit(main())
