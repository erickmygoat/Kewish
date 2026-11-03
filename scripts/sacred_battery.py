#!/usr/bin/env python3
"""Decrypt-test the theme-derived keys that survive the fingerprint tests.

Every keystream family here passed BOTH structural tests in
scripts/diff_spectrum.py (its values and its step-to-step differences look
random mod 29), so it cannot be ruled out without actually decrypting.

All decoding is SKIP-AWARE (lp.decode.undo_key_skip). That matters: on a
test page enciphered with the no-repeat rule, the right key decoded the
ordinary way scores z = -1.4 -- indistinguishable from noise.

Families (from the book's own vocabulary):
  phi(n)          "THE TOTIENT FUNCTION IS SACRED"; An End used phi(primes)
  phi(phi(n)), n*phi(n), sigma(n), running sum of primes, p(p(n))
  base-29 digits of pi, e, sqrt2 and the golden ratio ("the divinity within"
                  = the divine ratio, as a 2013 solver put it)

Each family is tried at every section start with offsets 0..199, at a few
meaningful offsets (3301, 1033, 761, 464, 29, 109, 1480), and -- for the
"one stream for the whole book" reading -- in a window around where the
stream would have reached if it ran continuously from the first section.
Both directions (C=P+K, C=P-K), with and without atbash.

Screening uses the first 150 runes of each section; the best cells are then
re-decoded in full. The identical procedure is run with random keystreams to
show what the best cell looks like by luck alone.

Usage:  python3 -I scripts/sacred_battery.py [--sources DIR] [--screen 150]
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

from lp import cipher, keystream as ks                 # noqa: E402
from lp.decode import undo_key_skip                     # noqa: E402
from lp.runetext import RuneText, UNSOLVED              # noqa: E402
from lp.score import Scorer                             # noqa: E402

N = 29
SPECIAL = [3301, 1033, 761, 464, 29, 109, 1480]
SKIP_RATE = 1 + 0.8 / 29


def phi_table(L):
    ph = list(range(L + 1))
    for p in range(2, L + 1):
        if ph[p] == p:
            for q in range(p, L + 1, p):
                ph[q] -= ph[q] // p
    return ph


def frac_digits(x_scaled, scale, count):
    """x_scaled / scale in [0,1): emit `count` base-29 digits."""
    out, r = [], x_scaled % scale
    for _ in range(count):
        r *= N
        out.append(r // scale)
        r %= scale
    return out


def constants(count):
    digs = int(count * math.log10(N)) + 40
    scale = 10 ** digs

    def arctan_inv(x):
        total = term = scale // x
        k, sign, x2 = 3, -1, x * x
        while term:
            term //= x2
            total += sign * (term // k)
            sign, k = -sign, k + 2
        return total
    pi = 16 * arctan_inv(5) - 4 * arctan_inv(239)
    e, term, k = 0, scale, 0
    while term:
        e += term
        k += 1
        term //= k
    sqrt2 = math.isqrt(2 * scale * scale)
    sqrt5 = math.isqrt(5 * scale * scale)
    golden = (scale + sqrt5) // 2
    return {
        'pi (base 29)': frac_digits(pi, scale, count),
        'e (base 29)': frac_digits(e, scale, count),
        'golden ratio (base 29)': frac_digits(golden, scale, count),
        'sqrt 2 (base 29)': frac_digits(sqrt2, scale, count),
    }


def families(L):
    ph = phi_table(L + 2)
    pr = list(ks.primes(L))
    fam = {
        'phi(n)': [ph[n] for n in range(1, L + 1)],
        'phi(phi(n))': [ph[ph[n]] for n in range(1, L + 1)],
        'n*phi(n)': [n * ph[n] for n in range(1, L + 1)],
        'running sum of primes': [],
        'super-primes p(p(n))': [],
    }
    acc = 0
    for p in pr:
        acc += p
        fam['running sum of primes'].append(acc)
    P2 = list(ks.primes(pr[-1] + 10)) if L < 6000 else list(ks.primes(L * 12))
    fam['super-primes p(p(n))'] = [P2[p - 1] for p in pr if p - 1 < len(P2)][:L]
    sig = [0] * (L + 1)
    for d in range(1, L + 1):
        for m in range(d, L + 1, d):
            sig[m] += d
    fam['sigma(n)'] = sig[1:]
    fam.update(constants(L))
    return {k: [v % N for v in s] for k, s in fam.items()}


def run(sections, streams, sc, screen, rng=None):
    """Return list of (z, family, section, offset, mode) for every cell."""
    cells = []
    starts_cache = {}
    for name, seq in streams.items():
        for si, (sec, c) in enumerate(sections):
            before = sum(len(x) for _, x in sections[:si])
            cont = int(before * SKIP_RATE)
            offs = set(range(0, 200)) | set(SPECIAL) | \
                set(range(max(0, cont - 60), cont + 61))
            for off in sorted(offs):
                stream = seq[off: off + int(screen * 1.3) + 5]
                if len(stream) < screen * 1.1:
                    continue
                for sign in (1, -1):
                    st = stream if sign == 1 else [(-v) % N for v in stream]
                    for inv in (False, True):
                        src = cipher.invert(c[:screen]) if inv else c[:screen]
                        p = undo_key_skip(src, st, sc, beam=4)
                        cells.append((sc.z(p), name, sec, off,
                                      f'{"C=P+K" if sign == 1 else "C=P-K"}'
                                      f'{" +atbash" if inv else ""}'))
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    ap.add_argument('--screen', type=int, default=150)
    args = ap.parse_args()
    sc = Scorer(os.path.join(args.sources, 'data'), n=3)
    sections = [(n, RuneText.from_page(args.sources, n).indices) for n in UNSOLVED]
    L = int(sum(len(c) for _, c in sections) * SKIP_RATE) + 4000
    fams = families(L)

    print('=' * 80)
    print('SACRED-SEQUENCE BATTERY (skip-aware decoding)')
    print('=' * 80)
    cells = run(sections, fams, sc, args.screen)
    cells.sort(reverse=True)
    print(f'{len(cells):,} cells screened on the first {args.screen} runes of each section')
    print('best cells:')
    for z, name, sec, off, mode in cells[:8]:
        print(f'  z = {z:+5.2f}   {name:24s} {sec:8s} offset {off:5d}  {mode}')

    rng = random.Random(1033)
    rand = {f'random#{i}': [rng.randrange(N) for _ in range(L)] for i in range(len(fams))}
    null = run(sections, rand, sc, args.screen)
    nmax = max(z for z, *_ in null)
    print(f'random keystreams, identical procedure ({len(null):,} cells): best z = {nmax:+.2f}')
    verdict = 'BEATS noise -- inspect' if cells[0][0] > nmax else 'within noise'
    print(f'  -> best sacred cell {cells[0][0]:+.2f} is {verdict}')
    print()
    print('full-section re-decode of the top 3 cells (a real break scores > +20):')
    for z, name, sec, off, mode in cells[:3]:
        c = dict(sections)[sec]
        seq = fams[name][off:off + int(len(c) * 1.3) + 5]
        if 'P-K' in mode:
            seq = [(-v) % N for v in seq]
        src = cipher.invert(c) if 'atbash' in mode else c
        p = undo_key_skip(src, seq, sc, beam=8)
        txt = RuneText.from_page(args.sources, sec).with_indices(p).render()
        print(f'  {name} / {sec} / {off} / {mode}: full z = {sc.z(p):+.2f}')
        print(f'     "{" ".join(txt.split())[:90]}"')


if __name__ == '__main__':
    sys.exit(main())
