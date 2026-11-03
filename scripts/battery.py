#!/usr/bin/env python3
"""Run candidate keys against every unsolved page, with calibrated scoring.

Two kinds of candidate:

  1. Built-in KEYWORDS -- terms from the traditions Liber Primus draws on
     (Nagarjuna / Madhyamaka, Zen, Cicada's own vocabulary, Emerson,
     Crowley). Each is tried in two spellings, with and without atbash,
     at every rotation. scripts/periodicity.py already rules out every
     keyword up to length 500 in bulk; this makes that concrete.

  2. YOUR keystream -- lp.hypotheses.my_keystream(n), if you've written it.
     Tried at start offsets 0..299 on every page, decoded both plainly and
     with the KEY_BUMP no-repeat rule undone.

Scores are z against random streams of the same length. Calibration line
first, so you know what a hit looks like.

IMPORTANT -- the multiple-testing trap. Try 16,000 keys and the best one
will score well above zero by luck alone, and its name will often feel
meaningful. So by default the SAME procedure is also run with random keys of
identical lengths (`--null`). A candidate only means something if it beats
that random-key maximum, not merely if it is "high". (When this was built,
THEMIDDLEWAY topped the keyword list at +4.78; three random-key runs of the
identical procedure topped out at +5.29, +4.82 and +5.01. Noise.)

Usage:  python3 -I scripts/battery.py [--sources DIR] [--offsets 300]
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import cipher, hypotheses                      # noqa: E402
from lp.runetext import RuneText, UNSOLVED             # noqa: E402
from lp.score import Scorer                            # noqa: E402
from lp.translit import to_indices                     # noqa: E402

KEYWORDS = {
    'nagarjuna': ['NAGARJUNA', 'SUNYATA', 'SHUNYATA', 'EMPTINESS', 'MADHYAMAKA',
                  'MIDDLEWAY', 'THEMIDDLEWAY', 'PRATITYASAMUTPADA',
                  'DEPENDENTORIGINATION', 'CATUSKOTI', 'TETRALEMMA',
                  'TWOTRUTHS', 'SVABHAVA', 'NIRVANA', 'SAMSARA', 'PRAJNA',
                  'PRAJNAPARAMITA', 'MULAMADHYAMAKAKARIKA', 'NOSELF',
                  'NEITHERBEINGNORNONBEING'],
    'zen': ['KOAN', 'ZEN', 'SATORI', 'MU', 'BODHIDHARMA', 'BUDDHA', 'DHARMA',
            'ENLIGHTENMENT', 'WHOAREYOU'],
    'cicada': ['CICADA', 'INSTAR', 'EMERGENCE', 'CIRCUMFERENCE', 'DIVINITY',
               'PILGRIM', 'PARABLE', 'LIBERPRIMUS', 'PRIMUS', 'WISDOM',
               'SACRED', 'TOTIENT', 'PRIMES', 'ANEND', 'SELF', 'TRUTH'],
    'emerson/crowley': ['SELFRELIANCE', 'CIRCLES', 'EMERSON', 'THELEMA',
                        'LIBERAL', 'LAWUNTOYOURSELF', 'DOWHATTHOUWILT'],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--offsets', type=int, default=300)
    ap.add_argument('--null', type=int, default=1,
                    help='random-key replicas of the whole procedure (0 = off)')
    args = ap.parse_args()
    import random
    rng = random.Random(1033)
    sc = Scorer(os.path.join(args.sources, 'data'), n=3)
    pages = {n: RuneText.from_page(args.sources, n).indices for n in UNSOLVED}

    print('=' * 74)
    print('KEY BATTERY')
    print('=' * 74)
    plain = RuneText.from_page(args.sources, 'solved_0_koan_1').indices
    fake = cipher.vigenere_encrypt(plain, to_indices('SUNYATA', False))
    hit = sc.z(cipher.vigenere_decrypt(fake, to_indices('SUNYATA', False)))
    miss = sc.z(cipher.vigenere_decrypt(fake, to_indices('NIRVANA', False)))
    print(f'calibration: a koan page enciphered with SUNYATA')
    print(f'  right key  z = {hit:+6.1f}      wrong key  z = {miss:+6.1f}')
    print()

    def run_keys(keys):
        """keys: list of (label, family, index-list). Returns per-family best."""
        out, cells = {}, 0
        for label, family, key in keys:
            for inv in (False, True):
                for page, c in pages.items():
                    src = cipher.invert(c) if inv else c
                    for rot in range(len(key)):
                        z = sc.z(cipher.vigenere_decrypt(src, key, key_offset=rot))
                        cells += 1
                        if z > out.get(family, (-1e9,))[0]:
                            out[family] = (z, f'{label}{" +atbash" if inv else ""}'
                                              f' on {page} rot {rot}')
        return out, cells

    keys = []
    for family, words in KEYWORDS.items():
        for w in words:
            for dg in (False, True):
                keys.append((w + (' (digraph)' if dg else ''), family,
                             to_indices(w, dg)))
    best, cells = run_keys(keys)
    print(f'keywords: {cells:,} page x key x spelling x atbash x rotation cells')
    overall = max(z for z, _ in best.values())
    for family, (z, where) in best.items():
        print(f'  best {family:16s} z = {z:+5.2f}   {where}')
    for t in range(args.null):
        rkeys = [(f'random#{i}', 'random', [rng.randrange(29) for _ in k])
                 for i, (_, _, k) in enumerate(keys)]
        rb, _ = run_keys(rkeys)
        rz = rb['random'][0]
        verdict = 'BEATS noise -- look closer' if overall > rz else 'within noise'
        print(f'  random keys, same procedure (replica {t+1}): max z = {rz:+5.2f}'
              f'   -> keyword best {overall:+.2f} is {verdict}')
    print()

    try:
        ks = hypotheses.my_keystream(5000)
    except NotImplementedError:
        print('my_keystream(): not written yet -- see lp/hypotheses.py')
        return 0
    ks = [int(v) % 29 for v in ks]
    top = (-1e9, None)
    tried = 0
    for page, c in pages.items():
        for off in range(args.offsets):
            stream = ks[off:off + len(c)]
            if len(stream) < len(c):
                break
            for mode in ('plain', 'key_bump'):
                p = (cipher.vigenere_decrypt(c, stream) if mode == 'plain'
                     else hypotheses.undo_key_bump(c, stream))
                z = sc.z(p)
                tried += 1
                if z > top[0]:
                    top = (z, f'{page} offset {off} {mode}')
    print(f'my_keystream(): {tried:,} cells, best z = {top[0]:+.2f} at {top[1]}')
    for t in range(args.null):
        rs = [rng.randrange(29) for _ in range(len(ks))]
        rbest = -1e9
        for page, c in pages.items():
            for off in range(args.offsets):
                stream = rs[off:off + len(c)]
                if len(stream) < len(c):
                    break
                rbest = max(rbest, sc.z(cipher.vigenere_decrypt(c, stream)),
                            sc.z(hypotheses.undo_key_bump(c, stream)))
        verdict = 'BEATS noise -- look closer' if top[0] > rbest else 'within noise'
        print(f'  random stream, same procedure (replica {t+1}): max z = '
              f'{rbest:+.2f}   -> {verdict}')
    print('  (a real break scores far above both -- the calibration hit was +47)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
