"""Gematria Primus: the rune-to-prime mapping and sums built on it.

Cicada's Gematria Primus assigns the **first 29 primes** to the 29 runes in
alphabet order -- 2, 3, 5, ... 109. A word's gematria value is the sum of its
runes' primes. Cicada used these sums as self-checks throughout Liber Primus,
and "3301" itself is prime, as is 1033 (its digit rotation) -- both facts the
puzzle leans on repeatedly.

Everything here is derived from `lp.alphabet`, so the prime table is not
duplicated.
"""
from .alphabet import INDEX, PRIMES, PRIME_OF, RUNES, is_rune

# Sanity: the Gematria Primus is exactly the first 29 primes.
_FIRST_29_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
assert PRIMES == _FIRST_29_PRIMES, 'Gematria Primus must be the first 29 primes'


def value(text):
    """Gematria sum of every rune in `text`; non-runes contribute nothing."""
    return sum(PRIME_OF[ch] for ch in text if is_rune(ch))


def value_of_indices(indices):
    return sum(PRIMES[i % 29] for i in indices)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def reverse(n):
    return int(str(n)[::-1])


def is_emirp(n):
    """Prime whose digit reversal is a different prime."""
    r = reverse(n)
    return is_prime(n) and is_prime(r) and r != n


def totient(n):
    """Euler's phi. phi(p) = p-1 for prime p -- the 'An End' keystream."""
    result, p, m = n, 2, n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


def rune_totient_stream(primes_seq):
    """phi(p) mod 29 for each prime -- the shift sequence of 'An End'."""
    return [(p - 1) % 29 for p in primes_seq]


def words(text):
    """Split rune text into words on any non-rune glyph."""
    out, cur = [], []
    for ch in text:
        if is_rune(ch):
            cur.append(ch)
        elif cur:
            out.append(''.join(cur))
            cur = []
    if cur:
        out.append(''.join(cur))
    return out
