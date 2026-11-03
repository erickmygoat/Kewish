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
