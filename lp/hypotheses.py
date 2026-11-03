"""Candidate models for the lag-1 repeat deficit, and a place to add your own.

MEASURED CONTEXT (see scripts/doubles_control.py)
-------------------------------------------------
Unsolved pages suppress adjacent identical runes to 0.19x chance
(z = -17.4), with lags 2-6 sitting exactly at chance. Genuinely
polyalphabetic *solved* pages sit near chance (0.85x pooled), which is what
theory predicts: a uniform independent keystream pushes the doubles rate
toward 1/29 from either side. Nothing uniform and independent produces
0.19x. So the unsolved stream was built with a rule that forbids, or nearly
forbids, emitting the same rune twice in a row.

Three mechanisms produce a lag-1-only deficit, and they imply DIFFERENT
attacks. That is why the choice matters rather than being a detail:

  (a) KEY_SKIP      -- on collision, discard that key value and take the
                       next one. The keystream then contains skips at
                       positions an attacker cannot see, so every candidate
                       key must be searched together with its skip pattern
                       (combinatorial, like the known interrupt search).

  (b) KEY_BUMP      -- on collision, perturb the key value deterministically
                       (e.g. +1 mod 29). The keystream stays in lockstep
                       with position, so a candidate key is testable exactly
                       and cheaply. Far more attackable than (a).

  (c) PLAINTEXT_AVOID -- the author composed plaintext that happens not to
                       collide. Then the deficit says nothing about the key
                       and keystream search should ignore it entirely.

Distinguishing (a) from (b) is the highest-value open question in this
repo: (b) makes brute-force over key sequences viable, (a) mostly does not.
"""
from .alphabet import N


def apply_rejection(plain, keystream, model='KEY_BUMP'):
    """Encipher `plain` under `keystream` with a no-adjacent-repeat rule.

    Used to generate known-answer fixtures: encipher English under a model,
    then check whether the corresponding decoder recovers it. If a model is
    right, its decoder should recover simulated text at ~100%.
    """
    out = []
    ks = list(keystream)
    k = 0
    for p in plain:
        c = (p + ks[k % len(ks)]) % N
        k += 1
        if out and c == out[-1]:
            if model == 'KEY_SKIP':
                c = (p + ks[k % len(ks)]) % N
                k += 1
            elif model == 'KEY_BUMP':
                c = (c + 1) % N
        out.append(c)
    return out


def undo_key_bump(cipher, keystream):
    """Decoder for model (b), with one honest ambiguity.

    When c[i] == c[i-1] + 1 the rune was EITHER bumped off a collision OR
    naturally landed one above its neighbour; the ciphertext cannot say
    which. This decoder always assumes a bump, so it mis-decodes the natural
    cases -- about 1 rune in 29. That costs a correct key a little score but
    does not hide it, which is all a screening decoder needs.
    """
    out = []
    ks = list(keystream)
    for i, c in enumerate(cipher):
        k = ks[i % len(ks)]
        if i > 0 and cipher[i - 1] == (c - 1) % N:
            # This position may have been bumped; try the unbumped value.
            cand = ((c - 1) - k) % N
            out.append(cand)
        else:
            out.append((c - k) % N)
    return out


# ---------------------------------------------------------------------------
# YOUR TURN
# ---------------------------------------------------------------------------
def my_keystream(n):
    """Return the first `n` key values (each 0..28) of a keystream to test.

    Run it with:  python3 -I scripts/battery.py
    It is tried on all 9 unsolved pages at start offsets 0..299, decoded both
    plainly and with the KEY_BUMP rule undone, and compared against random
    streams pushed through the identical procedure. A real break scores far
    above that random maximum (the calibration hit is about +47).

    WHAT IS ALREADY RULED OUT, so you don't spend a guess on it:
      * any fixed meaning per rune, in any language     (flat histogram)
      * a rune standing for a whole word                (scripts/word_structure.py)
      * an ordinary text used as-is as the key          (scripts/running_key.py)
      * any repeating keyword up to length 500          (scripts/periodicity.py)
      * primes / Fibonacci-style integer sequences      (flat at lags 2..500)

    WHAT SURVIVES: a key that looks random but is fully determined by a
    short, meaningful seed. `lp.keystream.hash_stream(seed)` builds exactly
    that -- a hash chain turning any phrase into a flat, aperiodic stream.
    This is where philosophy can legitimately matter: the math says the key
    must be scrambled, but nothing says the SEED isn't a verse, a koan, or a
    line of Nagarjuna. Choosing the seed is the part only a person can do.

    Decisions that are yours:
      - which seed text (exact wording, spelling, case, spacing all change
        the hash -- e.g. a translation of the MMK dedicatory verse, a line
        from the solved pages, "3301", the An End hash itself)
      - sha256 vs sha512 (Cicada quoted a SHA-512 on "An End")
      - one stream for the whole book, or reseeded per section
    """
    # TODO(you): 3-10 lines. Sketch:
    #   from itertools import islice
    #   from .keystream import hash_stream
    #   seed = "..."            # <- the meaningful choice
    #   return list(islice(hash_stream(seed, 'sha512'), n))
    raise NotImplementedError('fill in my_keystream()')
