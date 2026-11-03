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

Three mechanisms were on the table; the data has now chosen between them
(scripts/diff_spectrum.py):

  (a) KEY_SKIP      -- on collision, discard that key value and take the
                       next one (equivalently, redraw).  CONSISTENT.
                       The ~360 missing doubles reappear spread evenly over
                       the other 28 difference values, exactly as a redraw
                       predicts. Contrary to what this file first claimed,
                       it is NOT combinatorial: given the right keystream a
                       skip is possible only where C[i]-K[j+1]+K[j] == C[i-1]
                       (about 1 position in 29), so decoding branches rarely
                       and a beam search resolves it. See lp/decode.py.

  (b) KEY_BUMP      -- on collision, add a fixed +k.  RULED OUT for every k:
                       it would pile the missing doubles into the single bin
                       d=k (~+17 sd). No bin exceeds +3.1 sd.

  (c) PLAINTEXT_AVOID -- the author composed plaintext that never collides.
                       RULED OUT: a uniform independent key would erase any
                       plaintext property from C, and the deficit is the same
                       inside words (0.18x), across word gaps (0.24x), at line
                       breaks (0.21x) and at sentence ends (0.24x).

The rule leaks about 1 collision in 5, evenly everywhere (dispersion index
0.98): no passage is rule-free. Why 80% rather than 100% is unexplained.

The practical consequence: any keystream must be tested with skip-aware
decoding. Decoded the ordinary way, the RIGHT key scores like noise.
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
    """Decoder for model (b) -- which the data has since RULED OUT. Kept so the
    fixtures and tests that compare the two models still run.

    One honest ambiguity:

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
    plainly and SKIP-AWARE (lp.decode.undo_key_skip), and compared against random
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
