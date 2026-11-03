# Cicada 3301 — research dossier

A consolidated reference for the Cicada 3301 puzzles, their history, and the
cryptographic machinery behind them, with the Liber Primus as the focus.

**How to read the claim levels.** This file mixes things I computed from
primary data with things other people report, and keeps them separate:

| mark | meaning |
|---|---|
| **[V]** | **Verified here** — computed from local primary data by a script in this repo. Re-runnable. |
| **[P]** | **Primary** — quoted from a PGP-signed Cicada message or an archived original document. |
| **[R]** | **Reported** — secondary sources (press, wikis, community). Treat as claim, not fact. |

Where [R] sources contradict each other, that is noted rather than smoothed over.

---

## 1. What Cicada 3301 was

**[P]** Cicada described itself, in the email sent to the 2012 winners
(`2012/additional docs/The Leaked Email/2012 winners leak.txt` — a leak, so
the framing is the leaker's, but the message body is PGP-era Cicada text):

> "we are an international group we have no name we have no symbol we have no
> membership rosters we do not have a public website and we do not advertise
> ourselves … drawn together by common beliefs … that tyranny and oppression
> of any kind must end that censorship is wrong and that privacy is an
> inalienable right."

> "We are not a *hacker* group nor are we a *warez* group we do not engage in
> illegal activity … our primary focus is on researching and developing
> techniques to aid the ideas we advocate liberty privacy security"

The three screening questions it then asked were about the right to privacy
and anonymity, whether information should be free, and whether censorship
harms humanity.

**[P]** When press tied Cicada to a person called "Necrome" in 2012, Cicada
issued a signed denial
(`2012/additional docs/accusation of cyberterrorism/…`):

> "We do not engage in illegal activities. We are not associated with this
> individual. Anyone involved in illegal activities would be cut off from our
> fellowship immediately."

---

## 2. Timeline

| date | event | level |
|---|---|---|
| 2012-01-04 | First image posted to 4chan. Round 1 begins, runs ~1 month. | [R] |
| 2012-02 | Round 1 ends; winners emailed. "Thus our month-long journey ends. For now." | [P] |
| 2013-01-04/05 | Round 2 begins, one year and a day later. | [R] |
| 2013-03 | Gematria Primus published as an image; rune cipher work begins. | [V] file present |
| 2014-01-04/06 | Round 3 begins — on **Twitter**, not 4chan. | [R] |
| 2014 | Liber Primus released. Most of it has never been decrypted. | [V] |
| 2015-01-04 | **No** puzzle published. | [R] |
| 2016-01-05 | A clue posted on Twitter. | [R] |
| 2017-04 | Final verified signed message: *"Beware false paths."* | [P] |
| 2017→now | No verified puzzle since. | [R] |

**[R]** Sources disagree on exact start dates (Jan 4 vs 5 vs 6) and on which
4chan board (/x/ vs /b/) carried the first post. The Jan-4 /x/ reading is the
more commonly attested; treat the rest as unsettled.

---

## 3. The original post (2012)

**[R]** The image was plain white monospaced text on black, 509 × 503 px,
posted anonymously. The text is widely quoted as:

> "Hello. We are looking for highly intelligent individuals. To find them, we
> have devised a test. There is a message hidden in this image. Find it, and
> it will lead you on the road to finding us. We look forward to meeting the
> few that will make it all the way through. Good luck."

I could not retrieve a verbatim archived copy of the 4chan thread, so the
closing sentences in particular should be treated as [R], not [P]. Wordings
differ between secondary sources.

---

## 4. The puzzle chains

### 2012
Steganography (OutGuess) on the first image → a book code → the riddle
naming the book. **[P]** The riddle, from the signed message in
`2013/additional docs/signed messages/Hidden content of original image…`:

> "A book whose study is forbidden / Once dictated to a beast; / To be read
> once and then destroyed / Or you shall have no peace."

That points to Aleister Crowley's *Liber AL vel Legis* (The Book of the Law).
The chain also used **The Mabinogion** — the archive holds both the
Vigenère-enciphered transcript and its plaintext
(`2012/02/mabinogion_transcript`, `…_translation`); the plaintext is "The Lady
of the Fountain", opening *"King Arthur was at Caerlleon upon Usk"*. Later
stages involved telephone numbers, an answering machine, MIDI, and physical
posters with QR codes in multiple cities (the archive has poster photos from
Seattle, Warsaw, Miami, Paris, and others).

**[P]** The round closed with a signed message whose postscript is a 131-digit
number. **[V]** That number is 432 bits, composite, and has no prime factor
below 200,000; Pollard *p*−1 at B=200k and three Pollard-ρ runs of 4M
iterations each failed to split it. That profile is consistent with a balanced
RSA-style semiprime, which would need ECM or GNFS rather than these methods.
I did not factor it, and I am not claiming it is a semiprime — only that it is
composite with no small factors.

### 2013
**[R]** Bootable Linux CD images, posters on lamp posts worldwide, Crowley's
writings, riddles in audio. The archive contains the Cicada OS shell scripts,
the `761.MP3` audio, and the full 2013 Twitter feed. **[V]** `3301.iso` in
`rtkd/iddqd` is a **Git LFS pointer stub** (136,398,848 bytes upstream), not
the image itself — anonymous clones do not fetch LFS objects.

**[V]** A curiosity: the 2013 files `2013/02/wisdom` and `2013/02/folly` are
**byte-identical** (both 3,368 bytes, md5 `0c7d18e8…`). Whatever distinguishes
them is not in their contents.

### 2014
**[V]** The chain, from the archive's own stage notes
(`assets/2014/stage01…10/README.md`):

```
Twitter @1231507051321 → i.imgur.com/zN4h51m.jpg → outguess
  → auqgnxjtvdbll3pv.onion  (+ /1033.jpg, outguess)
  → cu343l33nqaekrnw.onion  (the "growing string")
  → fv7lyucmeozzd5j4.onion  (/server-status → reversed hexdump → matrix)
  → avowyfgl5lkzfj3n.onion
  → q4utgdi2n4m4uim5.onion  (gpg → reversed hexdump → mp3)
  → ut3qtzbrvs7dtvzp.onion
```

**[R]** OutGuess on the initial JPEG yields a quote from Emerson's
*Self-Reliance* plus numbers and a PGP signature. **[P]** The round's final
message gave one more onion and nothing else:

> "Hello. Your enlightenment awaits you. ky2khlqdf7qdznac.onion — We look
> forward to hearing from you. Good luck. 3301"

**[R]** The 2014 round is generally considered unsolved.

---

## 5. Authenticity: the PGP key

**[P]** The 2017 message is the standing authenticity rule:

> "Beware false paths. Always verify PGP signature from 7A35090F. 3301"

**[V]** That checks out mechanically. Every Cicada signature block contains
the base64 run `EBgfAeV6NQkP`, which decodes to the OpenPGP issuer key-ID
subpacket `18 1F 01 E5 7A 35 09 0F` — long key ID **181F01E57A35090F**, short
ID **7A35090F**. **41** files in the archive carry it. So the short ID in the
2017 text is not a separate assertion to take on faith; it is literally the
issuer field of the signatures.

This matters practically: the corpus contains hoaxes and trolls (the archive
files them under "troll message", "french trolls", "unverified claims"), and
signature provenance is the only reliable filter.

---

## 6. The Gematria Primus

**[V]** 29 Anglo-Saxon futhorc runes, assigned the **first 29 primes** in
alphabet order. Verified to be exactly the primes 2…109, and the master
transcription contains exactly these 29 codepoints and no others across the
whole book.

| rune | ᚠ | ᚢ | ᚦ | ᚩ | ᚱ | ᚳ | ᚷ | ᚹ | ᚻ | ᚾ | ᛁ | ᛄ | ᛇ | ᛈ | ᛉ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| letter | F | U/V | TH | O | R | C/K | G | W | H | N | I | J | EO | P | X |
| prime | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 41 | 43 | 47 |

| rune | ᛋ | ᛏ | ᛒ | ᛖ | ᛗ | ᛚ | ᛝ | ᛟ | ᛞ | ᚪ | ᚫ | ᚣ | ᛡ | ᛠ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| letter | S/Z | T | B | E | M | L | NG/ING | OE | D | A | AE | Y | IO/IA | EA |
| prime | 53 | 59 | 61 | 67 | 71 | 73 | 79 | 83 | 89 | 97 | 101 | 103 | 107 | 109 |

**[V]** Sum of all 29 primes = **1480**.

**[V] Validation.** A word's gematria value is the sum of its runes' primes.
Running that over every annotated sentence in the solved corpus reproduces the
community's published values **102 / 102**. (`scripts/gematria_check.py`)

**[V]** Number properties the puzzle leans on:

- **3301** is prime, and an **emirp** — its reversal **1033** is also prime.
  Cicada used both (the 2014 onion served `1033.jpg`).
- **761** (the 2013 MP3) is prime, and an emirp (reversal 167 is prime).
- φ(*p*) = *p*−1 for prime *p*. This is the keystream that solves "An End":
  shifts φ(*p*) mod 29 over successive primes = 1, 2, 4, 6, 10, 12, 16, 18,
  22, 28, 1, 7, …

---

## 7. The 5×5 magic square

**[V]** Transcribed on the Loss of Divinity page group. Secondary sources
disagree about its constant (3301 vs 1033), so here it is computed:

```
  434  1311   312   278   966   = 3301
  204   812   934   280  1071   = 3301
  626   620   809   620   626   = 3301
 1071   280   934   812   204   = 3301
  966   278   312  1311   434   = 3301
 3301  3301  3301  3301  3301   ← column sums
 diagonals: 3301, 3301
```

**[V]** Fully magic, constant **3301**. Additional structure: the grid is
invariant under 180° rotation, and holds only **13 distinct values** across
25 cells. Centre cell 809.

**[V] A circulating claim that is false.** It is sometimes said that
"3301 minus each entry is prime". It is not: of the 13 distinct values, only
one complement (3301 − 278 = 3023) is prime. (`scripts/magic_square.py`)

---

## 8. The four 2048-bit byte strings

**[V]** Commonly referred to as "the 256-byte page", there are **four**, all
exactly 256 bytes = 2048 bits, labelled in `rtkd/iddqd`:

| # | origin |
|---|---|
| 1 | Hidden Service 2 — `cu343l33nqaekrnw.onion` |
| 2 | Hidden Service 3 — `fv7lyucmeozzd5j4.onion` |
| 3 | Hidden Service 4 — `avowyfgl5lkzfj3n.onion` |
| 4 | **Liber Primus pages 49–51 matrix**, converted to hex |

Three come from the 2014 onion chain and one from inside the book, yet all
four share the same width — which is the genuinely suggestive part.

**[V]** The decisive test is distinctness, not randomness. A permutation of
0..255 (an S-box or RC4-style state table — key material, not a message)
would show 256 distinct byte values. 256 uniform random draws are expected to
show 256·(1−(255/256)²⁵⁶) = **162.0**. Measured: **158, 157, 172, 161**.

All four sit on the random expectation, so **none is a permutation**. They
behave like ciphertext or digests. (`scripts/byte_strings.py`)

On the RSA-2048 reading: 2048 bits is the right width, but a bare ciphertext
block with no published modulus is not attackable even in principle. Every
solved Cicada stage has been solvable from material in hand, so if RSA is
intended, a modulus has to exist somewhere in the corpus. That makes
"find a 2048-bit modulus" a concrete search target rather than a vibe — and
it is not the 131-digit 2012 number, which is only 432 bits.

---

## 9. The "An End" bounty

**[P]** Liber Primus page 56 ("An End"), decrypted via the totient keystream:

> "WITHIN THE DEEP WEB, THERE EXISTS A PAGE THAT HASHES TO
> `36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4`
> IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE"

**[V]** 128 hex chars = 512 bits → **SHA-512**. The page hashing to it has
never been located. This is the puzzle's outstanding open bounty, and unlike
the rune pages it is not a cryptanalysis problem — it is a search problem,
and unsolvable by analysis alone.

---

## 10. Liber Primus status

**[V]** 74 pages. Nine are solved; **56 are not**. 2,979 solved runes against
**12,956** unsolved. Of the nine solved pages, only five are enciphered at
all — four are printed as plain rune-for-letter text.

**[V]** Ciphers used on the five enciphered pages:

| page | method |
|---|---|
| A Warning | atbash ("invert Gematria") |
| Welcome | Vigenère, key **DIVINITY**, with interrupts |
| A Koan (1) | atbash + Vigenère, key length 1 |
| jpg107-167 | Vigenère, key **FIRFUMFERENFE**, with interrupts |
| An End | sequence cipher, φ(prime) keystream |

**[V]** The "interrupt": on three pages Cicada left some plaintext `ᚠ`
unencrypted. Such a rune passes through *and consumes no key value*, shifting
the alignment of everything after it. Which `ᚠ` are interrupts is not
derivable from the ciphertext — it is a per-page set found by search.

**[V]** Why the remaining 56 resist: they are statistically flat to the limit
of measurement (index of coincidence 0.03448 against a uniform 1/29 =
0.03448; χ² = 26.4 on 28 df), with one sharp exception — adjacent identical
runes are suppressed ~5× (z = −17.4) while every other lag sits at chance.
See [FINDINGS.md](FINDINGS.md) for the full analysis and what it rules out.

---

## 11. Who was behind it

**[R]** Never established. No one has produced verified attribution. The
recurring theories:

1. **Intelligence-agency recruitment** (NSA, CIA, GCHQ, MI6). The most
   popular theory. Against it: no agency has ever claimed it, and the
   recruitment pitch Cicada actually sent emphasised *anti*-surveillance
   values — privacy, anti-censorship, opposition to state oppression — which
   sits awkwardly with a signals-intelligence employer.
2. **A privacy/cryptography collective.** Closest to Cicada's own
   self-description [P], which names liberty, privacy and security as its
   research focus and explicitly disclaims illegality.
3. **An ARG or social experiment.**

**[R]** Marcus Wanner, then 15, is the best-known named solver: he completed
the 2013 round with the IRC team `#decipher` and was admitted to a private
3301 forum. The archive holds a directory of his work
(`2012/marcus wanner's CAKES/`). Joel Eriksson, a Swedish security
researcher, is reported to have reached the late stages of 2012 but missed the
registration window.

Note the asymmetry worth holding onto: Cicada's *stated* purpose (recruit
people, give them projects) implies the 2012 and 2013 winners know far more
than the public does, and the 2014 round was never completed by anyone who
has said so publicly.

---

## 12. Open problems, ranked by tractability

1. **Separate the two rejection models** for the lag-1 repeat deficit in the
   unsolved pages. Testable now, no key guess needed; decides whether
   brute-force over keystreams is viable at all. See FINDINGS.md §6.
2. **Find a 2048-bit modulus** anywhere in the corpus. Would make the four
   byte strings attackable; without one they are inert.
3. **Factor the 131-digit 2012 number** (432-bit). Needs ECM/GNFS, not the
   elementary methods tried here. May be meaningless even if factored.
4. **The SHA-512 page.** A search problem over the deep web, not analysis.
   Likely dead unless the page still exists somewhere.

---

## 13. Primary source inventory (local)

| path | contents |
|---|---|
| `rtkd/iddqd` | master transcription, page scans, keys, index, outguess dumps, byte strings, 2012–2016 media |
| `relikd/LiberPrayground` | solved plaintexts, published keys, rune n-gram corpora, solver tooling |
| `cicada-solvers/the-complete-cicada3301-archive` | 1,244 files: per-year puzzle archives 2012–2017, signed messages, 4chan threads, IRC logs, leaked emails, media coverage, wiki pages |

Fetch all three with `./scripts/fetch_sources.sh` (the third needs adding; it
clones the two Liber Primus repos today).

**Caveat on the archive:** it is a community compilation. Its *signed*
messages are verifiable against key 7A35090F [V]; its narrative articles,
wiki pages and IRC logs are [R] and include material the compilers themselves
mark as unverified or as trolling.

---

## Sources

Secondary sources consulted for [R] claims:

- [Cicada 3301 — Wikipedia](https://en.wikipedia.org/wiki/Cicada_3301)
- [Uncovering Cicada Wiki — What Happened (2012)](https://uncovering-cicada.fandom.com/wiki/What_Happened_(2012))
- [The Complete Cicada3301 Archive](https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive)
- [rtkd/iddqd](https://github.com/rtkd/iddqd)
- [relikd/LiberPrayground](https://github.com/relikd/LiberPrayground)
- [Boxentriq — Cicada 3301 Liber Primus guide](https://www.boxentriq.com/guides/cicada-3301-liber-primus)
- [Boxentriq — Gematria Primus translator](https://www.boxentriq.com/encodings/gematria-primus-translator)
- [The Register — Cicada 3301 2014](https://www.theregister.com/2014/01/11/cicada_3301_2014/)
- [SlashGear — strange history of Cicada 3301](https://www.slashgear.com/1428322/strange-history-cicada-3301/)
- [All That's Interesting — Cicada 3301](https://allthatsinteresting.com/cicada-3301)
- [Discovery UK — Cicada 3301](https://www.discoveryuk.com/mysteries/cicada-3301-the-internets-most-elegant-rabbit-hole/)
- [krisyotam/cicada3301](https://github.com/krisyotam/cicada3301)
