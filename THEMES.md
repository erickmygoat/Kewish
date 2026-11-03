# The Liber Primus: how it was solved, what it keeps repeating, and what that means for the 56

A deep dive across every solved page, the 2012–2014 puzzle record, and the
unsolved pages. Claims are marked as in RESEARCH.md: **[V]** verified by a
script in this repo, **[P]** quoted from Cicada's own text or signed messages,
**[R]** reported by the solving community or other secondary sources.

---

## 1. How each solved page was actually solved

| page | protection | key | where the key came from |
|---|---|---|---|
| A WARNING | atbash (alphabet reversed) | — | — |
| WELCOME | Vigenère + plaintext F left unencrypted | **DIVINITY** | the 2013 Parable: *"find the divinity within"* |
| SOME WISDOM | none — plain runes | — | — |
| A KOAN | atbash + shift 3 | — | — |
| THE LOSS OF DIVINITY | none | — | — |
| A KOAN (2) | Vigenère + plaintext F left unencrypted | **FIRFUMFERENFE** — CIRCUMFERENCE with each C turned into F | the 2013 Parable: *"shed our own circumferences"*; this page's own plaintext says *"the I is the voice of the circumference"* |
| AN INSTRUCTION | none | — | — |
| AN END | stream cipher: φ(prime) mod 29, one F left unencrypted | **totient of the primes** | SOME WISDOM: *"THE TOTIENT FUNCTION IS SACRED"* |
| PARABLE | none | — | published in 2013, a year before the book |

**[V]** All nine reproduce from this repo's own code (`scripts/verify_ground_truth.py`).

**[P]/[R] The decisive fact, from the 2013 record.** The book's final page,
the Parable, was released in **2013**, a year before the Liber Primus, in the
ID tag of `761.mp3` (*"The Instar Emergence"*). An IRC log from 2013-01-07
quotes it. It contains both words that later became keyword keys, DIVINITY
and CIRCUMFERENCE. **Every key used in the solved pages was announced in
plain English before it was needed.** The totient key was announced inside
the book itself.

**[R]** Some pages were gated. Solvers had to submit "the three magic squares"
(§3) to a Cicada server before the encrypted koan (107.jpg, 167.jpg) was
released. The 2014 write-up describes the koan's break: frequency analysis
looked almost English except for A, R, S and T, because the F's in
FIRFUMFERENFE are shifts of zero, so 4 of every 13 runes come through
unchanged.

---

## 2. What the text keeps saying

**[P]** Read in order, the solved pages form a short course with a single arc:

- **Within → emergence.** *"JOURNEY DEEP WITHIN AND YOU WILL ARRIVE OUTSIDE."*
  *"LIKE THE INSTAR, IT IS ONLY THROUGH GOING WITHIN THAT WE MAY EMERGE."*
  *"FIND THE DIVINITY WITHIN AND EMERGE."* *"DISCOVER TRUTH INSIDE
  YOURSELF."* [R] The community wiki calls the first chapter *Intus* (Latin,
  "within"); I couldn't trace that title to a primary source.
- **The circumference is the self that must be shed.** *"THE I IS THE VOICE OF
  THE CIRCUMFERENCE."* *"THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS WHICH
  CAUSE THE LOSS OF DIVINITY"* — consumption, preservation, adherence. *"WE
  MUST SHED OUR OWN CIRCUMFERENCES."*
- **Primality is divinity.** *"…THAT HAVE US LOSE OUR PRIMALITY, AND THUS OUR
  DIVINITY."* *"THE PRIMES ARE SACRED."* The spiritual claim and the
  mathematics are the same claim.
- **Hold no possession and no position.** *"NEVER BECOME ATTACHED TO WHAT YOU
  OWN. BE PREPARED TO DESTROY ALL THAT YOU OWN."* *"THERE IS NOTHING TO BE
  RIGHT ABOUT. TO BELONG IS DEATH."* The first koan strips away the student's
  name, profession, species and description until he can say nothing, and only
  then is he admitted.
- **The insect's life cycle.** [R] The unsolved sections are illustrated, in
  order: crosses/signs, sprouts, **roots**, a Möbius strip, dots and
  **mayflies**, a **wing**, cuneiform, plants. A cicada nymph lives on roots,
  tunnels up, sheds its exoskeleton (each stage is an *instar*) and emerges
  winged. Periodical cicadas surface on **prime** cycles (13 and 17 years).

An interpretive note for the Nagarjuna line of thought: *"THERE IS NOTHING TO
BE RIGHT ABOUT"* is very close to Mūlamadhyamakakārikā 13.8, where emptiness
is "the relinquishing of all views". The koan's method of negating every
self-description is the Madhyamaka method in Zen form. This is a parallel in
ideas, not evidence about any key.

---

## 3. How the book is built

1. **[P]/[V] Words are numbers.** *"DO NOT EDIT OR CHANGE THIS BOOK … EITHER
   THE WORDS OR THEIR NUMBERS. FOR ALL IS SACRED."* The SOME WISDOM square
   mixes words and numbers. Replace each word with its Gematria Primus value
   (SHADOWS = 341, VOID = 130, MOBIUS = 226, …) and it is a perfect magic
   square with constant **1033**. Words were picked in matched pairs to make
   the symmetry work: SHADOWS = CABAL = 341, BUFFERS = MOURNFUL = 199,
   CARNAL = ANALOG = 320.

2. **[V] Sentences were written to be prime.** 45 of the 102 solved sentences
   have prime gematria sums. Ordinary English sentences of the same lengths
   give 14.2 — **z = +8.8**. The Warning is 9 of 10; the Parable 4 of 4; the
   Instruction page 5 of 6. The two koan *stories* sit exactly at chance
   (3 of 22, 2 of 7). The doctrinal lines were composed with a gematria
   calculator in hand; the stories were not. (`scripts/theme_checks.py`)

3. **[V] The emirp pair 3301 ↔ 1033 runs through everything.** Three magic
   squares, all perfect and all symmetric under a half-turn: 3301 (the
   Instruction page), 1033 (the SOME WISDOM word square), 1033 (a 7×7 hidden
   in an MP3). The 2013 Parable's three lines sum to the primes 1259, 1031 and
   1229, and their product, **1,595,277,641**, is the number Cicada printed
   beside it. *"THE INSTAR EMERGENCE"* sums to **761**, the MP3's filename.

4. **[V] ᚠ (F) is the "nothing" rune.** It is the first rune and is worth 0 as
   a shift. In FIRFUMFERENFE it is a no-shift. In three pages, plaintext F
   passes through unencrypted and consumes no key.

5. **[V] Each page is one step harder.** Reversed alphabet → reversed alphabet
   plus a shift → a keyword → a keyword with unencrypted F's → a keyword with
   built-in nulls → an infinite mathematical stream. The unsolved pages are
   the next step.

---

## 4. What the themes predicted for the 56 — and what testing showed

Each habit above suggests where the next key might be. Each suggestion was
turned into a test that would have caught a real answer on a known page.

| the habit suggests… | test | result |
|---|---|---|
| a word from the text as the key (like DIVINITY) | key-value flatness + periodicity scan | **ruled out** — any word or phrase, any length |
| the An End key, φ(primes), continued | difference fingerprint, any offset | **ruled out** (likelihood ratio e⁻³⁶) |
| MOBIUS (from the 1033 square; also a section image) → Möbius μ(n) or Mertens | value + difference fingerprints | **ruled out** at every offset |
| primes, π(n), Fibonacci, squares, Gematria primes cycled, decimal π | same | **ruled out** at every offset |
| φ(n), φ(φ(n)), n·φ(n), σ(n), running sum of primes, p(p(n)), base-29 π / e / √2 / golden ratio | pass both fingerprints → decrypted directly, skip-aware, 112,480 cells | **nothing**: best +7.47 vs +7.72 for random keys; a real break scores ~+20 |
| a rune left unencrypted (like F) | over-representation of each rune | **none** (max +2.2 sd) |
| the chapter's own headings reused (A KOAN, SOME WISDOM…) as cribs | word-length patterns of the 14 unsolved headings | **0 of 14 fit** |
| mayflies, *Ephemeridae* → an ephemeral, use-once key | the statistics | **consistent**: flat, aperiodic, never repeats |

### The biggest finding: the no-repeat rule is a *skip*, and that changes past tests

**[V]** The unsolved pages avoid repeating a rune ~80% of the time. The
difference histogram shows the missing repeats spread evenly over every other
value. A deterministic "bump" is ruled out. The encoder **skipped ahead in its
key** (or redrew) whenever it was about to repeat. (`scripts/diff_spectrum.py`)

**[V]** That has a consequence for every sequence test anyone has run. On a
test page encrypted this way, the **correct** key decoded the ordinary way
scores **z = −1.4**, indistinguishable from noise. Decoded skip-aware it
recovers **99.9%** of the text. A candidate key tested naively since 2014
could have been the right one and been thrown away. This repo now decodes
skip-aware everywhere (`lp/decode.py`).

---

## 5. What to do next, ranked

1. **Re-run the community's tested sequences skip-aware.** Every candidate list
   tried since 2014 was presumably decoded without modelling the skip. They are
   all worth one cheap re-run. Of everything here, this is the most likely to
   contain a missed answer.
2. **Seeds from the text.** The book always announced its keys in plain
   English, and the key must look random. That combination points to a key
   *derived from* an announced phrase — a hash chain or a PRNG seeded by a
   sentence. `my_keystream()` + `scripts/battery.py` is set up for exactly this.
3. **Use prime sentences as a second check.** A correct decryption of a
   doctrinal page should show many sentences with prime gematria sums,
   independently of the English score.
4. **Factor the 2012 432-bit number** — the same size as the 2014 RSA key
   solvers factored. A GNFS job.

---

Sources for [R] items: the Complete Cicada3301 Archive (2014 "What Happened"
parts 1–2, "The complete story of onion 6", 2013 IRC logs, the solved-pages
wiki), rtkd/iddqd's index and key notes, and relikd/LiberPrayground.
