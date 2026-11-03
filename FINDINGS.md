# Findings

Every number here was produced by the scripts in this repo against the
upstream transcription, on a toolkit that reproduces all nine published
solutions (`scripts/verify_ground_truth.py`). Re-run any of them to check.

## 1. The corpus

| part | runes |
|---|---|
| solved pages (9) | 2,979 |
| unsolved pages (56) | 12,956 |

The master transcription contains **exactly 29 distinct rune codepoints** and
no others, across the whole book — solved and unsolved alike. So the unsolved
pages are not using a different or extended alphabet.

## 2. The unsolved pages are flat to the limit of measurement

`scripts/report.py`:

| statistic | solved plaintext | unsolved | uniform random |
|---|---|---|---|
| index of coincidence | 0.06139 | **0.03448** | 0.03448 |
| χ² vs uniform (df 28) | 2351.5 | **26.4** | ≈ 28 |
| most common rune | ᛖ 12.76% | ᛟ 3.80% | 3.45% |
| least common rune | ᚫ 0.07% | ᛇ 3.08% | 3.45% |

The IoC matches 1/29 to five decimal places and χ² sits *below* its own
degrees of freedom. This is the central obstacle: a repeating key of any
length leaves periodic structure, and none is present. Whatever enciphered
these pages did not reuse key material in a detectable way.

This also disposes of two classes of idea quickly:

- **A different plaintext language will not explain it.** Latin, English,
  or an invented language all use their letters unevenly. Flatness this
  complete is a property of the key, not the language.
- **Simple substitution cannot explain it.** A fixed rune→letter mapping
  preserves the frequency histogram, so no substitution and no rearrangement
  of a flat histogram yields a language.

## 3. One statistic is not flat, and it is not subtle

`scripts/doubles.py` — repeats at each lag, unsolved pages:

| lag | observed | expected | ratio | z |
|---|---|---|---|---|
| **1** | **86** | **446.7** | **0.19** | **−17.37** |
| 2 | 441 | 446.7 | 0.99 | −0.27 |
| 3 | 439 | 446.7 | 0.98 | −0.37 |
| 4 | 459 | 446.6 | 1.03 | +0.60 |
| 5 | 479 | 446.6 | 1.07 | +1.56 |
| 6 | 455 | 446.6 | 1.02 | +0.41 |

Adjacent identical runes are suppressed roughly fivefold. Every other lag is
at chance. The deficit holds on all nine unsolved page groups individually
(z from −2.4 to −8.6), so it is not one page dragging the pool.

### 3a. It is a property of the unsolved cipher, not of the book

`scripts/doubles_control.py`. This is the control that matters, because
Liber Primus plaintext *itself* mildly disfavours doubles (ratio 0.75):

| material | runes | ratio | z |
|---|---|---|---|
| enciphered solved pages, ciphertext | 1,883 | 0.71 | −2.39 |
| unsolved pages | 12,956 | **0.19** | **−17.37** |

And the solved pages explain their own 0.71 without any special rule: two of
them (`0_warning`, `0_koan_1`) are **monoalphabetic** — atbash, or atbash plus
a length-1 key — which preserves the doubles count *exactly* (5→5 and 14→14
observed). The three genuinely polyalphabetic solved pages pool to ratio 0.85,
i.e. pushed toward chance, which is what theory predicts.

So polyalphabetic encryption moves the doubles rate *toward* 1/29. The
unsolved pages move sharply *away* from it. A uniform independent keystream
cannot do that.

### 3b. The rule is probabilistic, not absolute

`scripts/simulate.py`. An absolute "never emit a repeat" rule gives ratio
0.000 (KEY_BUMP) or 0.030 (KEY_SKIP, which can re-collide). The measured value
is 0.193 — low, but not zero. Sweeping the probability the rule is applied:

| p | 0.0 | 0.3 | 0.5 | 0.7 | **0.8** | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|
| resulting ratio | 0.93 | 0.67 | 0.53 | 0.31 | **0.23** | 0.13 | 0.03 |

**p ≈ 0.8** reproduces the observation. Whatever produced these pages
suppressed about four collisions in five.

## 4. What has been ruled out

- **Autokey family** — `scripts/autokey.py`. This was the most attractive
  hypothesis, because ciphertext autokey (`C[i] = P[i] + C[i−1]`) predicts a
  lag-1-only constraint for free: adjacent ciphertext runes are equal exactly
  when the plaintext rune is `ᚠ`. It is also trivially invertible — plaintext
  is just the first difference. Tested across all 9 page groups × 5 variants
  with a scorer calibrated at **z = +86.98 on known plaintext** and **z = −0.98
  on known ciphertext**: the best of 45 cells was **z = +2.97**, which is what
  the maximum of 45 noise draws looks like. Refuted.

  The appeal was quantitative too, and it is worth recording why it fails on
  its own terms: the predicted doubles rate equals the plaintext `ᚠ` rate,
  measured at 1.61% on solved plaintext, against 0.66% observed — a factor of
  2.4 out, in addition to the scorer finding nothing.

- **Correlated integer keystreams.** Primes, Fibonacci and similar sequences
  taken mod 29 have correlated successive values, which would leave a lag-2+
  signature. Lags 2–6 are flat (|z| < 1.6), so these are disfavoured on
  structural grounds rather than by exhaustive trial. Note φ(prime) is the
  key that solved "An End", so its exclusion here is informative.

## 5. Corrections to claims circulating about this puzzle

Checked against the data, not inherited:

- **"The 256-byte page is a Liber Primus page."** The three 256-byte strings
  in `rtkd/iddqd` are the **2012–2013 hidden-service byte strings**
  (`byte-strings/byte-strings`), not pages of the Liber Primus. All three are
  exactly 512 hex characters = 256 bytes = 2048 bits. They are a separate
  artifact from the unsolved rune pages and should not be pooled with them.
- **"RSA-2048 block."** Possible but weakly motivated: a bare 2048-bit
  ciphertext block with no published modulus is unsolvable by construction,
  and every solved Cicada stage has been solvable from material in hand. If
  RSA is intended, the modulus has to be somewhere — which makes the
  3301-derived grids a specific thing to search for rather than a curiosity.
- **"All nine solved pages decrypt, so the toolkit is validated."** True but
  weak: four of the nine are plaintext. The meaningful validation is the five
  enciphered pages, three of them polyalphabetic.

## 6. The open question

The deficit is real, large, local to lag 1, and reproduced by a rejection rule
applied ~80% of the time. Two mechanisms fit, and they differ in how
attackable they are:

- **KEY_SKIP** — on collision, discard the key value and take the next.
  The keystream then contains skips at positions invisible to an attacker, so
  every candidate key must be searched jointly with its skip pattern. Roughly
  as expensive as the known interrupt search, i.e. mostly intractable.
- **KEY_BUMP** — on collision, perturb the key deterministically. The
  keystream stays in lockstep with position, so a candidate key is testable
  exactly and cheaply. **This is the case worth hoping for**, and
  `lp/hypotheses.undo_key_bump` already implements the decoder.

Separating these is the highest-value next step, and it is testable without
guessing a key: the two models leave different residual statistics on
simulated text. `lp/hypotheses.apply_rejection` generates fixtures for both.
