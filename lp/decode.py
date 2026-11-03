"""Decoders for the no-repeat rule found in the unsolved pages.

MEASURED (scripts/diff_spectrum.py): adjacent identical runes occur at 0.19x
chance, and the missing doubles are spread EVENLY over the other 28
difference values. A deterministic "bump" (+k on collision) would pile them
into one bin; no bin is elevated. So the encoder skipped ahead / redrew,
about 4 times in 5, uniformly across words, lines and sentences.

Model (KEY_SKIP):  c = P[i] + K[j]; j += 1
                   if c == C[i-1] (and, ~80% of the time):  c = P[i] + K[j]; j += 1

Decoding with the right keystream is NOT combinatorial. A skip at position
i is possible only if  C[i] - K[j+1] + K[j] == C[i-1], which happens by
chance about 1 time in 29. So the decoder only branches there, and a beam
search with an English n-gram score resolves the branches. A wrong choice
desynchronises the key for everything after it, which is exactly why the
score separates the branches within a few runes.
"""
N = 29


def encrypt_key_skip(plain, keystream, p_apply=0.8, rng=None):
    """Reference encoder, for building known-answer fixtures."""
    import random
    rng = rng or random.Random(0)
    out, j = [], 0
    for x in plain:
        c = (x + keystream[j]) % N
        j += 1
        if out and c == out[-1] and rng.random() < p_apply:
            c = (x + keystream[j]) % N
            j += 1
        out.append(c)
    return out


def undo_key_skip(cipher, keystream, scorer, beam=8):
    """Beam-search decode under KEY_SKIP. Returns the best plaintext indices.

    `scorer` is an lp.score.Scorer; its n-gram table scores partial text.
    `keystream` must be at least ~1.1x as long as `cipher` (skips eat keys).
    """
    from .alphabet import RUNES
    n = scorer.n
    table, floor = scorer.table, scorer.floor
    # state: (score, key_index, plaintext list)
    states = [(0.0, 0, [])]
    for i, c in enumerate(cipher):
        nxt = []
        for score, j, pt in states:
            if j + 1 >= len(keystream):
                continue
            options = [(j, j + 1)]                      # no skip
            if i > 0 and (c - keystream[j + 1] + keystream[j]) % N == cipher[i - 1]:
                options.append((j + 1, j + 2))          # a skip was possible
            for kj, nj in options:
                x = (c - keystream[kj]) % N
                new = pt + [x]
                inc = 0.0
                if len(new) >= n:
                    gram = ''.join(RUNES[v] for v in new[-n:])
                    inc = table.get(gram, floor)
                nxt.append((score + inc, nj, new))
        if not nxt:
            break
        nxt.sort(key=lambda s: -s[0])
        # keep distinct key indices so the beam doesn't collapse onto one path
        seen, states = set(), []
        for s in nxt:
            if s[1] not in seen:
                states.append(s)
                seen.add(s[1])
            if len(states) >= beam:
                break
    return max(states, key=lambda s: s[0])[2] if states else []
