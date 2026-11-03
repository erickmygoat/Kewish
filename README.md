# Kewish — a Liber Primus analysis toolkit

Tooling for statistical cryptanalysis of the unsolved pages of Cicada 3301's
**Liber Primus**, built so that every claim it makes can be re-derived by
running it.

The Liber Primus is a 74-page book written in a 29-rune Anglo-Saxon futhorc.
Nine pages are solved and public. **Fifty-six are not**, and have resisted
analysis since 2014. This repo does not solve them. What it does is make the
negative results precise and reproducible, which is the part usually missing.

## Design rule: calibrate before you conclude

A null result only means something if the same code finds a real answer when
one is present. So nothing here reports a measurement on unsolved material
without first reproducing a known one:

```
$ python3 -I scripts/verify_ground_truth.py
page                   protection        runes  result
------------------------------------------------------------------------
0_warning              atbash              184  OK  "A WARNNG#BELIEUE NOTHNG FROM  THIS BOO"
0_welcome              vigenere            515  OK  "WELCOME#WELCOME,PIL GRIM,TO THE GREAT"
0_wisdom               plain               157  OK  "SOME WISDOM#THE PRIMES ARE SAC RED.THE"
0_koan_1               atbash+vigenere     780  OK  "A COAN#A MAN DECIDED TO  GO AND STUDY"
0_loss_of_divinity     plain               755  OK  "THE LOSS OF DIUINITY#THE CIRCU MFERENC"
jpg107-167             vigenere            319  OK  "A COAN#DURNG A LESSON,THE MAS TER EXPL"
jpg229                 plain                89  OK  "AN INSTRUCTIAN#CWESTIAN ALL  THNGS.DIS"
p56_an_end             sequence             85  OK  "AN END#WITHIN THE DEEP WEB, TH ERE EXI"
p57_parable            plain                95  OK  "PARABLE#LICE THE INSTAR T UNNELNG TO T"
------------------------------------------------------------------------
ALL SOLVED PAGES REPRODUCED
```

Worth noting, because summaries of this puzzle often blur it: **four of the
nine "solved" pages are not enciphered at all.** They are plain rune-for-letter
text. Only five involve a key, and only three of those are polyalphabetic.
"All nine decrypt correctly" is a weaker statement than it sounds.

## Quick start

```bash
./scripts/fetch_sources.sh              # clone the two upstream data repos
python3 -I scripts/verify_ground_truth.py   # must pass before anything else
python3 -I tests/test_ground_truth.py       # 8 regression tests
python3 -I scripts/report.py                # solved vs unsolved statistics
python3 -I scripts/doubles.py               # the one real anomaly, by lag
python3 -I scripts/doubles_control.py       # is it the cipher, or the book?
python3 -I scripts/simulate.py              # what rule reproduces it
python3 -I scripts/autokey.py               # autokey family (refuted)
```

No dependencies beyond the Python 3 standard library. Scripts take
`--sources DIR` if you cloned the data elsewhere.

## Layout

| path | what it is |
|---|---|
| `lp/alphabet.py` | the 29 runes, their Gematria primes and letter forms |
| `lp/runetext.py` | page-file and master-transcription parsing |
| `lp/cipher.py` | vigenère, atbash, sequence decryption, interrupt handling |
| `lp/keystream.py` | primes, totients, Fibonacci, Lucas, keyword streams |
| `lp/stats.py` | IoC, χ², rune frequencies, adjacent-repeat rate |
| `lp/score.py` | null-calibrated English scorer over rune n-grams |
| `lp/hypotheses.py` | models for the repeat deficit — **and where to add yours** |
| `scripts/` | runnable analyses, each self-documenting |
| `tests/` | regression tests; the key one re-derives all 9 solved pages |

## Findings

See [FINDINGS.md](FINDINGS.md). The short version: the unsolved pages are
statistically flat in every respect but one, and that one exception is sharp,
large, and not explained by any cipher family tested here.

## Data sources

Neither is vendored — `scripts/fetch_sources.sh` clones both.

- [rtkd/iddqd](https://github.com/rtkd/iddqd) — master transcription, page scans
- [relikd/LiberPrayground](https://github.com/relikd/LiberPrayground) — solved
  plaintexts, published keys, rune n-gram corpora

Published solutions and the rune ordering are upstream's; the analysis code
here is independent and validated against them.
