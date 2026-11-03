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
    """Decoder for model (b). Deterministic, so no search is needed."""
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

    This is picked up automatically by scripts/battery.py, which runs it
    against all 9 unsolved pages at every key offset and reports a
    null-calibrated z. Known plaintext scores z = +87; noise is |z| < 3.

    CONSTRAINT WORTH KNOWING BEFORE YOU CHOOSE (measured, not assumed):
    the unsolved pages are flat at every lag but 1. Any keystream whose
    successive values are *correlated* -- slowly growing integer sequences,
    most notably -- leaves a lag-2+ signature that these pages do not have.
    That is evidence against plain prime/Fibonacci-style streams taken mod
    29, and in favour of streams whose consecutive values are effectively
    independent: digit expansions of irrationals in base 29, hash chains,
    or a long text used as a running key.

    The catch, honestly: those all need the exact seed or source text, so
    the search only pays off if the seed is guessable from the book itself
    (3301, the magic-square constants, the 512-bit hash on "An End").
    """
    # TODO(you): 5-10 lines. e.g. digits of pi in base 29, a hash chain
    # seeded from 3301, or a running key from a text Cicada pointed to.
    raise NotImplementedError('fill in my_keystream()')
