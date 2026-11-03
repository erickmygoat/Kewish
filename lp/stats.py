"""Statistics for telling encrypted rune text from plaintext rune text.

The central fact these measure: natural language uses its letters very
unevenly, and every classical cipher that reuses key material leaves some
of that unevenness behind. A keystream that never repeats erases it
completely, which is what the unsolved pages look like.
"""
import math
from collections import Counter

N = 29


def frequencies(indices):
    c = Counter(indices)
    total = len(indices) or 1
    return [c.get(i, 0) / total for i in range(N)]


def index_of_coincidence(indices):
    """Probability two runes drawn without replacement match.

    Uniform random over 29 symbols gives 1/29 = 0.03448. English rune text
    runs far higher (~0.06+). Normalising is deliberately skipped so the
    number stays comparable to 1/29.
    """
    n = len(indices)
    if n < 2:
        return 0.0
    c = Counter(indices)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def chi_squared_uniform(indices):
    """Chi-squared of the rune histogram against a flat distribution.

    Low means indistinguishable from uniform (i.e. well encrypted);
    high means structure survives. 28 degrees of freedom, so a value near
    28 is what pure randomness produces.
    """
    n = len(indices)
    if n == 0:
        return 0.0
    expected = n / N
    c = Counter(indices)
    return sum((c.get(i, 0) - expected) ** 2 / expected for i in range(N))


def doubles_rate(indices):
    """Observed vs expected rate of two identical runes in a row.

    Returns (observed, expected, ratio). For a uniform independent stream
    the expected rate is 1/29. A ratio well below 1 means the generator
    avoided doubles -- that is a real, exploitable deviation.
    """
    if len(indices) < 2:
        return 0.0, 0.0, 0.0
    pairs = len(indices) - 1
    obs = sum(1 for a, b in zip(indices, indices[1:]) if a == b) / pairs
    exp = 1.0 / N
    return obs, exp, (obs / exp if exp else 0.0)


def load_ngram(path):
    """Load a LiberPrayground ngram count file into log-probabilities."""
    counts = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                counts[parts[0]] = int(parts[1])
    total = sum(counts.values()) or 1
    floor = math.log10(0.01 / total)
    return {k: math.log10(v / total) for k, v in counts.items()}, floor


def ngram_score(text, table, floor, n):
    """Mean log10 probability per n-gram. Higher (less negative) = more
    English-like. Scoring per-gram keeps texts of different length
    comparable."""
    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    if not grams:
        return floor
    return sum(table.get(g, floor) for g in grams) / len(grams)
