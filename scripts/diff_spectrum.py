#!/usr/bin/env python3
"""What kind of key could have produced these pages -- tested at ANY offset.

Two fingerprints of a keystream survive encryption and can be measured
without decrypting anything:

  1. the distribution of key VALUES      -> shapes the rune histogram
         C = P + K, so hist(C) = hist(P) convolved with hist(K)
  2. the distribution of key DIFFERENCES -> shapes C[i+1]-C[i]
         C[i+1]-C[i] = (P[i+1]-P[i]) + (K[i+1]-K[i])

English plaintext is lopsided in both. If the key's values or consecutive
differences are lopsided too, the ciphertext stays measurably lopsided, at
every starting offset, because these are properties of the whole sequence,
not of where you start in it. So a key family can be ruled out in one shot.

The unsolved pages are flat in both (apart from the doubles, d=0, which is
the no-repeat rule and is excluded here). For each candidate family this
prints the chi^2 the pages WOULD show if that family were the key, next to
what they actually show.

It also prints the lag-1 difference histogram itself, which settles how the
no-repeat rule works: a deterministic "bump" piles the missing doubles into
one bin; a skip/redraw spreads them evenly.

Usage:  python3 -I scripts/diff_spectrum.py [--sources DIR]
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lp import keystream as ks                         # noqa: E402
from lp.alphabet import INDEX, N                       # noqa: E402
from lp.runetext import RuneText, UNSOLVED             # noqa: E402

LEN = 20000   # key values per family
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)   # pi digits need long int -> str


def hist(vals, k=N):
    h = [0] * k
    for v in vals:
        h[v % k] += 1
    t = sum(h) or 1
    return [x / t for x in h]


def conv(a, b, sign=1):
    out = [0.0] * N
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[(i + sign * j) % N] += x * y
    return out


def exp_chi2(dist, n, skip_zero=False):
    """Expected chi^2 vs uniform for n samples drawn from `dist`."""
    bins = list(range(1, N)) if skip_zero else list(range(N))
    tot = sum(dist[b] for b in bins)
    k = len(bins)
    return (k - 1) + n * k * sum((dist[b] / tot - 1 / k) ** 2 for b in bins)


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    return r - r // m if m > 1 else r


def mobius_seq(L):
    mu = [1] * (L + 1)
    is_p = [True] * (L + 1)
    for p in range(2, L + 1):
        if is_p[p]:
            for q in range(p, L + 1, p):
                if q > p:
                    is_p[q] = False
                mu[q] *= -1
            for q in range(p * p, L + 1, p * p):
                mu[q] = 0
    return mu[1:]


def families():
    pr = list(ks.primes(LEN))
    fam = {}
    fam['primes p(n)'] = pr
    fam['totient of primes p(n)-1  [An End key]'] = [p - 1 for p in pr]
    fam['primes, large (p > 10^6)'] = [p for p in ks.primes(90000)][70000:70000 + LEN]
    fam['totient phi(n), n=1..'] = [phi(n) for n in range(1, LEN + 1)]
    mu = mobius_seq(LEN)
    mert, acc = [], 0
    for v in mu:
        acc += v
        mert.append(acc)
    fam['Moebius mu(n)  [MOBIUS in the 1033 square]'] = mu
    fam['Mertens M(n) (running Moebius)'] = mert
    pi_n, c, pset = [], 0, set(pr)
    for n in range(1, LEN + 1):
        c += n in pset
        pi_n.append(c)
    fam['prime-counting pi(n)'] = pi_n
    fam['natural numbers n'] = list(range(LEN))
    fam['squares n^2'] = [n * n for n in range(LEN)]
    fam['Fibonacci'] = list(ks.fibonacci(LEN))
    fam['Gematria primes cycled 2,3,5..109'] = [pr[i % 29] for i in range(LEN)]
    fam['decimal digits of pi'] = [int(d) for d in str(pi_digits(LEN))[:LEN]]
    import random
    rng = random.Random(1)
    fam['uniform random (reference)'] = [rng.randrange(N) for _ in range(LEN)]
    return fam


def pi_digits(n):
    """Integer containing the first n decimal digits of pi (Machin)."""
    def arctan_inv(x, scale):
        total = term = scale // x
        k, sign, x2 = 3, -1, x * x
        while term:
            term //= x2
            total += sign * (term // k)
            sign, k = -sign, k + 2
        return total
    scale = 10 ** (n + 10)
    return (16 * arctan_inv(5, scale) - 4 * arctan_inv(239, scale)) // 10 ** 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', default='/home/user/relikd/LiberPrayground')
    args = ap.parse_args()

    corpus = [INDEX[ch] for ch in open(
        os.path.join(args.sources, 'data', 'baseline-rune-stream.txt'),
        encoding='utf-8').read() if ch in INDEX][:600000]
    E = hist(corpus)
    Ediff = hist([(b - a) % N for a, b in zip(corpus, corpus[1:])])

    pages = [RuneText.from_page(args.sources, n).indices for n in UNSOLVED]
    allc = [v for p in pages for v in p]
    cdiff = [(b - a) % N for p in pages for a, b in zip(p, p[1:])]
    n_uni, n_dif = len(allc), len(cdiff)

    obs_h = hist(allc)
    obs_d = hist(cdiff)
    chi_uni = n_uni * N * sum((x - 1 / N) ** 2 for x in obs_h)
    tot = sum(obs_d[1:])
    chi_dif = n_dif * 28 * sum((obs_d[d] / tot - 1 / 28) ** 2 for d in range(1, N))

    print('=' * 86)
    print('KEY FINGERPRINTS: value spectrum and difference spectrum')
    print('=' * 86)
    print()
    print('lag-1 difference histogram of the unsolved pages, C[i+1]-C[i] mod 29')
    cnt = [round(x * n_dif) for x in obs_d]
    e = n_dif / N
    sd = math.sqrt(n_dif * (1 / N) * (1 - 1 / N))
    print('  ' + '  '.join(f'd{d}:{cnt[d]}({(cnt[d]-e)/sd:+.1f})' for d in range(0, 8)))
    print('  ' + '  '.join(f'd{d}:{cnt[d]}({(cnt[d]-e)/sd:+.1f})' for d in range(8, 16)))
    print('  ' + '  '.join(f'd{d}:{cnt[d]}({(cnt[d]-e)/sd:+.1f})' for d in range(16, 23)))
    print('  ' + '  '.join(f'd{d}:{cnt[d]}({(cnt[d]-e)/sd:+.1f})' for d in range(23, 29)))
    best = max(range(1, N), key=lambda d: cnt[d])
    print(f'  missing doubles: {round(e) - cnt[0]}.  A fixed "bump" by +k would put them all in one')
    print(f'  bin (~+17 sd). Largest non-zero bin is d{best} at {(cnt[best]-e)/sd:+.1f} sd: they are spread')
    print('  evenly -> the encoder SKIPPED/REDREW, it did not bump.')
    print()
    print(f'{"candidate key family":44s} {"chi^2 of runes":>15s} {"chi^2 of diffs":>15s}  verdict')
    print(f'{"":44s} {"(df 28)":>15s} {"(df 27)":>15s}')
    print('-' * 86)
    print(f'{"UNSOLVED PAGES (observed)":44s} {chi_uni:15.1f} {chi_dif:15.1f}')
    print('-' * 86)
    for name, seq in families().items():
        kv = [v % N for v in seq]
        q = hist(kv)
        qd = hist([(b - a) % N for a, b in zip(kv, kv[1:])])
        worst_u = min(exp_chi2(conv(E, q, s), n_uni) for s in (1, -1))
        worst_d = min(exp_chi2(conv(Ediff, qd, s), n_dif, skip_zero=True)
                      for s in (1, -1))
        # 3-sigma-ish thresholds for chi^2 with 28 / 27 df
        dead = worst_u > 28 + 3 * math.sqrt(56) or worst_d > 27 + 3 * math.sqrt(54)
        why = []
        if worst_u > 28 + 3 * math.sqrt(56):
            why.append('values')
        if worst_d > 27 + 3 * math.sqrt(54):
            why.append('differences')
        verdict = ('RULED OUT (' + ' + '.join(why) + ')') if dead else 'survives'
        print(f'{name:44s} {worst_u:15.1f} {worst_d:15.1f}  {verdict}')
    print()
    print('reading')
    print('  A family is ruled out at EVERY starting offset when either fingerprint')
    print('  would leave the pages measurably lopsided. Survivors must look random')
    print('  in both their values and their step-to-step changes: base-29 digit')
    print('  expansions, hash chains, cryptographic PRNGs -- or something not yet')
    print('  imagined that shares those properties.')


if __name__ == '__main__':
    sys.exit(main())
