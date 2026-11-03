# Hypothesis ledger

A running list of every idea about the unsolved Liber Primus pages: what it
predicts, the test, the result, and whether it is still alive. Add an idea by
adding a row. An idea is **ruled out** only if a test that *would* have caught
it on known text came back empty on the unsolved pages.

---

See [THEMES.md](THEMES.md) for how the solved pages were broken and how
their habits translate into these tests.

## Where we are, in one paragraph

The 56 unsolved pages are written in the same 29 runes as the solved ones, in
real words with English-shaped word lengths. But every rune's meaning changes
from position to position. The letter counts are perfectly flat, nothing
repeats at any spacing from 2 to 500, and the same short word (almost
certainly *A* or *I*) is written with all 29 different runes. That is the
signature of a key that never repeats and looks random. There is one crack:
two identical runes in a row are five times rarer than chance (z = −17), which
means the key was generated with a rule. Our best guess at that rule is "avoid
emitting a repeat", applied about 80% of the time. The rule turned out to
be a skip, not a bump. It is tractable to decode, but it hides the right
key from any test that ignores it. Everything else follows from those facts.

## The one rule that kills most ideas

> **Anything that treats each rune by itself, the same way every time, can
> only shuffle the letter counts. It cannot change their shape.**

Give a rune a different letter, a letter from another language, a whole word,
its prime value, any number, any meaning. If the rule is "this rune always
becomes that thing", the counts move between columns, and the *shape* of
the histogram survives. Every human language has a lopsided histogram
(English E ≈ 12.8%, X ≈ 0.2%). The unsolved pages have a flat one (every rune
3.1–3.8%). You can't shuffle flat into lopsided.

So whatever unlocks these pages has to depend on **where** a rune is, or
**what is next to it**. That's what a key is. This isn't an opinion about
cipher fashion; it follows from counting.

---

## Ledger

| # | idea | what it predicts | test | result | status |
|---|---|---|---|---|---|
| 1 | Give each rune one fixed letter ("set the runes equal", simple substitution) | lopsided rune counts | χ² vs uniform | unsolved χ² **26.4**; English **2,351** | **ruled out** |
| 2 | Same, but the letters are from another language (Latin, Old English, Sanskrit…) | lopsided counts in *that* language's shape | same theorem as #1 | every natural language is lopsided | **ruled out** for any fixed mapping |
| 3 | Set each rune equal to its prime / a number, then do math per rune | any per-rune function is a fixed mapping | same theorem | — | **ruled out** unless the math also uses position or neighbours (then it *is* a key, and see #10) |
| 4 | A rune stands for a whole word | separated groups would be phrases; word lengths would not look like English | `word_structure.py` | word-length distance from English **0.079** (solved English 0.041; random breaks 0.261) | **ruled out** |
| 4b | — same, one-rune words | under any fixed meaning they pile onto 2–3 runes (A, I) | `word_structure.py` | solved: 28 tokens on **3** runes. Unsolved: 87 tokens on **all 29** | **ruled out**, and the clearest single picture of "there is a key" |
| 5 | The key is an existing text used as-is: Nagarjuna, Crowley, Emerson, the Mabinogion, a bible… | ciphertext stays measurably lopsided | `running_key.py` | running key χ² **571 ± 39**; unsolved **26.4**; z = **−13.9** | **ruled out** as plain text (run on English) |
| 6 | The key is a repeating keyword of any length ≤ 500 | coincidence spike at the key length | `periodicity.py` | real keywords: z +7 to +10. Unsolved max **+2.9** (noise ≈ 3.5) | **ruled out**. The skip rule (#11) blurs long periods, but keywords fail independently: any key spelled from words has lopsided *values*, which would show in the flat rune counts whatever the skips (#5) |
| 6b | — specifically Nagarjuna / Zen / Cicada / Emerson / Crowley words (SUNYATA, MADHYAMAKA, THE MIDDLE WAY, KOAN, INSTAR, CIRCUMFERENCE, SELFRELIANCE, THELEMA…) | high English score on decryption | `battery.py`, 16,380 cells | best THE MIDDLE WAY **+4.78**; random keys, same procedure: **+5.29, +4.82, +5.01** | **ruled out** — see the note below |
| 7 | Ciphertext autokey | lag-1-only constraint, trivial inversion | `autokey.py` | best of 45 cells **+2.97** | **ruled out** |
| 8 | The 256-byte strings are an S-box / key table | 256 distinct byte values | `byte_strings.py` | **158 / 157 / 172 / 161** (random expects 162) | **ruled out** |
| 9 | "3301 minus each magic-square entry is prime" | 13/13 prime | `magic_square.py` | **1/13** | **false** |
| 10 | A scrambled key from a meaningful seed: a hash chain, or a text that was itself encrypted | flat, aperiodic — exactly what we see | `battery.py` + `my_keystream()` (skip-aware) | not yet tried | **open** — your move. Every solved key was announced in plain English first, which fits a seed-from-a-sentence design |
| 11 | No-repeat rule: KEY_SKIP vs KEY_BUMP | a bump piles missing repeats into one difference bin; a skip spreads them | `diff_spectrum.py` | missing repeats spread evenly; no bin above +3.1 sd | **resolved: skip.** Bump ruled out for every +k |
| 11b | The skip makes the cipher intractable | — | `lp/decode.py` fixture | given the right key a skip is detectable (1 position in 29 branches); beam decode recovers **99.9%** | **wrong** — and the right key decoded *naively* scores z −1.4, so naive tests can miss it |
| 14 | The An End key (totient of primes) continues into the unsolved pages | prime-gap-shaped difference histogram | `diff_spectrum.py`, any offset | log-likelihood ratio −35.6 | **ruled out** |
| 15 | MOBIUS (a word in the 1033 square; also a section image) → Möbius μ(n) / Mertens as key | lopsided values / differences | `diff_spectrum.py` | μ −176.9, Mertens −240.5 | **ruled out** |
| 16 | Primes, π(n), Fibonacci, squares, Gematria primes cycled, decimal π | lopsided values or differences | `diff_spectrum.py` | all far from flat | **ruled out** at every offset |
| 17 | φ(n), φ(φ(n)), n·φ(n), σ(n), running sum of primes, p(p(n)), base-29 π / e / √2 / golden ratio | pass both fingerprints, so must be decrypted | `sacred_battery.py`, skip-aware, 112,480 cells | best +7.47; random keys +7.72; real break ≈ +20 | **ruled out** at section starts (0–199 + 3301, 1033, 761…) and as one continuous stream |
| 18 | The unsolved headings reuse the solved ones (A KOAN, AN INSTRUCTION, SOME WISDOM, KNOW THIS) | matching word lengths | `theme_checks.py` | **0 of 14** match | **ruled out** |
| 19 | Any rune (not just F) left unencrypted | that rune over-represented | `theme_checks.py` | max +2.2 sd (OE) | **ruled out** for any rune with real frequency |
| 20 | Doctrinal sentences have prime gematria sums by design | prime share above chance | `theme_checks.py` | **45/102 vs 14.2, z +8.8**; koan stories at chance | **confirmed** — usable to validate a decryption |
| 12 | A 2048-bit RSA modulus is hidden in the corpus | would make the 4 byte strings attackable | search | not yet run | **open** |
| 13 | Interrupt sets (unencrypted F) on the unsolved pages | F share would be well above 3.45% | `report.py` | F = **3.54%**, about chance | **mostly ruled out** — at most a few dozen across 56 pages (see #19 for every other rune) |

**About row 6b.** "THE MIDDLE WAY" topped the keyword list, and it's the name
of Nagarjuna's own school. That's exactly the situation where you want to
believe it. Its decryption reads `NY YILAESEO ABIA IACTNGF…`, and random keys
run through the identical procedure scored *higher* in two of three runs.
Out of 16,000 tries something always comes out on top, and our minds are
good at finding meaning in whichever name that is. `battery.py` now runs the
random-key comparison by default for this reason.

### Claims relayed from an earlier session, not reproduced here

These come from the conversation transcript and are *plausible*, but no code
in this repo has re-derived them yet. Don't build on them until one does:
line-by-line / sentence key resets; a Latin scorer; "Rosetta stone" cribs from
section titles; "18 of 45 classic sequences ruled out at any offset".

---

## Where philosophy fits — and where it can't

The solved pages aren't decoration. They are a short spiritual curriculum,
and its sources are identifiable:

| tradition | where it shows up in the solved text |
|---|---|
| **Zen** | Two pages are literally titled *A KOAN*. The master–student exchange is the classic koan form. |
| **Madhyamaka (Nagarjuna)** | The koan's logic. The student offers his name, his job, his species. The master rejects each one: *"THAT IS NOT WHAT YOU ARE, THAT IS ONLY WHAT YOU ARE CALLED."* Separating what a thing is *called* from what it *is* is Nagarjuna's two truths: names are conventional designations, not essences (no *svabhāva*). Zen tradition counts Nagarjuna as its 14th Indian patriarch, though that lineage is hagiography, not history. |
| **Emerson** | The 2014 round's OutGuess layer quotes *Self-Reliance*. Echoed in *"DISCOVER TRUTH INSIDE YOURSELF. FOLLOW YOUR TRUTH."* |
| **Crowley / Thelema** | The 2013 book code points to *Liber AL vel Legis*. Echoed in *"YOU ARE A LAW UNTO YOURSELF"*, whose wording comes from Romans 2:14 (KJV) but whose sense is Thelemic. |
| **Gnostic / mystical** | *"EACH INTELLIGENCE IS HOLY. FOR ALL THAT LIVES IS HOLY."* *"IT IS ONLY THROUGH GOING WITHIN THAT WE MAY EMERGE."* |
| **Number mysticism** | *"THE PRIMES ARE SACRED."* The Gematria Primus, the 3301 magic square, the totient key. And the name itself: periodical cicadas emerge on **prime-numbered** cycles (13 and 17 years). An *instar* is the stage between molts, and the "instar emergence" theme is the insect's own life cycle. |

So your instinct that this is a philosophical text is right, and Nagarjuna is
a reasonable member of the family. The koan in particular reads like
Madhyamaka in Zen dress.

**What philosophy can't do:** change the counting argument above.
Reinterpreting what a rune *means* can't make a flat histogram into
language, because reinterpretation is a fixed mapping.

**What philosophy *can* do, and where it might genuinely be the missing piece:**

1. **Pick the seed.** The data says the key must look random. A hash chain
   looks random *and* is fully determined by a short phrase. A dedicatory
   verse, a koan, the eight negations, the line *"that is only what you are
   called"* — each is a seed nobody can guess without reading the right book.
   That is idea #10, and `my_keystream()` is where it goes.
2. **Supply cribs.** Once a candidate key decrypts a stretch, philosophical
   expectations about *what the text should say* help judge partial hits.
3. **Interpret the answer.** Cicada's stated aim was to find people who would
   understand the content, not just decrypt it.

Philosophy is a good source of guesses. The random-key comparison is how we
check them, and #6b shows why the guesses need checking.
