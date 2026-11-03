"""Calibrated English-likeness scoring for candidate rune plaintext.

Scores are mean log10 probability per n-gram, computed over rune n-grams
from a transliterated English corpus (relikd/LiberPrayground `data/p-*gram`).
Higher (closer to zero) is more English-like.

A raw score is meaningless on its own, so `Scorer.z` reports how many
standard deviations a candidate sits above a null distribution built from
random 29-ary streams of the same length. That makes results comparable
across pages and across cipher hypotheses.
"""
import math
import os
import random
from collections import Counter

from .alphabet import RUNES

N = 29


class Scorer:
    def __init__(self, data_dir, n=3, null_samples=200, seed=3301):
        self.n = n
        path = os.path.join(data_dir, f'p-{n}gram.txt')
        counts = {}
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.split()
                if len(parts) == 2:
                    counts[parts[0]] = int(parts[1])
        total = sum(counts.values()) or 1
        self.table = {k: math.log10(v / total) for k, v in counts.items()}
        self.floor = math.log10(0.01 / total)
        self._null_cache = {}
        self.null_samples = null_samples
        self.rng = random.Random(seed)

    def raw(self, indices):
        s = ''.join(RUNES[i % N] for i in indices)
        g = [s[i:i + self.n] for i in range(len(s) - self.n + 1)]
        if not g:
            return self.floor
        return sum(self.table.get(x, self.floor) for x in g) / len(g)

    def _null(self, length):
        """Mean/sd of the score for uniform random streams of this length."""
        bucket = max(64, min(4096, 1 << (length.bit_length())))
        if bucket not in self._null_cache:
            vals = []
            for _ in range(self.null_samples):
                vals.append(self.raw([self.rng.randrange(N) for _ in range(bucket)]))
            mu = sum(vals) / len(vals)
            var = sum((v - mu) ** 2 for v in vals) / max(1, len(vals) - 1)
            self._null_cache[bucket] = (mu, math.sqrt(var))
        return self._null_cache[bucket]

    def z(self, indices):
        """Standard deviations above random. English text lands far above 0."""
        mu, sd = self._null(len(indices))
        return (self.raw(indices) - mu) / sd if sd else 0.0
