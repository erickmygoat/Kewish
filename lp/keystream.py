"""Integer sequences used as (or tested as) Liber Primus keystreams."""
from itertools import count


def primes(limit=None):
    """Infinite (or bounded) prime generator via incremental sieve."""
    composites = {}
    n = 2
    emitted = 0
    while limit is None or emitted < limit:
        if n not in composites:
            yield n
            emitted += 1
            composites[n * n] = n
        else:
            p = composites.pop(n)
            x = n + p
            while x in composites:
                x += p
            composites[x] = p
        n += 1


def totient_of_primes(limit=None):
    """phi(p) = p - 1 for prime p. This is the 'An End' keystream."""
    for p in primes(limit):
        yield p - 1


def fibonacci(limit=None):
    a, b = 1, 1
    for i in count():
        if limit is not None and i >= limit:
            return
        yield a
        a, b = b, a + b


def lucas(limit=None):
    a, b = 2, 1
    for i in count():
        if limit is not None and i >= limit:
            return
        yield a
        a, b = b, a + b


def constant(value):
    while True:
        yield value


def keyword(indices):
    """Cycle a fixed list of shifts forever."""
    while True:
        for v in indices:
            yield v


def hash_stream(seed, algo='sha256'):
    """Infinite stream of values 0..28 from a hash chain seeded by `seed`.

    state_0 = H(seed); state_{k+1} = H(state_k). Each digest byte b < 232
    (= 8*29) yields b % 29; bytes >= 232 are discarded so the output is
    exactly uniform. This is the kind of key that would look like the
    unsolved pages -- flat, aperiodic -- while still being fully determined
    by a short, meaningful seed.
    """
    import hashlib
    state = hashlib.new(algo, seed.encode('utf-8') if isinstance(seed, str)
                        else seed).digest()
    while True:
        for b in state:
            if b < 232:
                yield b % 29
        state = hashlib.new(algo, state).digest()
