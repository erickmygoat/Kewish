#!/usr/bin/env python3
"""Regression tests. Run directly (python3 -I tests/test_ground_truth.py)
or under pytest.

The important one is test_all_solved_pages_reproduce: if that fails, every
measurement in this repo is suspect, because the same code paths produce
them.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

from lp import cipher, keystream                       # noqa: E402
from lp.alphabet import INDEX, RUNES, PRIMES, N        # noqa: E402
from lp.hypotheses import apply_rejection              # noqa: E402
from lp.runetext import RuneText, SOLVED               # noqa: E402

SOURCES = os.environ.get('LP_SOURCES', '/home/user/relikd/LiberPrayground')


def test_alphabet_is_29_distinct_runes():
    assert len(RUNES) == N == 29
    assert len(set(RUNES)) == 29
    assert len(PRIMES) == 29
    assert PRIMES[0] == 2 and PRIMES[-1] == 109
    assert INDEX['ᚠ'] == 0


def test_invert_is_an_involution():
    vals = list(range(N))
    assert cipher.invert(cipher.invert(vals)) == vals


def test_vigenere_roundtrip():
    plain = [i % N for i in range(200)]
    key = [3, 14, 15, 9, 26]
    ct = cipher.vigenere_encrypt(plain, key)
    assert cipher.vigenere_decrypt(ct, key) == plain


def test_interrupt_passes_through_and_shifts_alignment():
    """An interrupt rune is emitted unchanged AND consumes no key value,
    so every rune after it shifts one position along the key.

    Hand-computed: ct = [0, 1, 2, 3], key = [10, 20].
      no interrupt  -> [(0-10), (1-20), (2-10), (3-20)] mod 29
      interrupt #1  -> rune 0 passes through; the rest re-align to key[0]
    """
    ct = [0, 1, 2, 3]
    key = [10, 20]
    assert cipher.vigenere_decrypt(ct, key) == [19, 10, 21, 12]
    assert cipher.vigenere_decrypt(ct, key, interrupts={1}) == [0, 20, 11, 22]


def test_interrupt_only_fires_on_listed_occurrences():
    """The 2nd F is an interrupt, the 1st is not."""
    ct = [0, 5, 0, 5]
    key = [1]
    out = cipher.vigenere_decrypt(ct, key, interrupts={2})
    assert out[0] == (0 - 1) % 29   # encrypted normally
    assert out[2] == 0              # passed through


def test_totient_of_primes_stream():
    assert list(keystream.totient_of_primes(6)) == [1, 2, 4, 6, 10, 12]


def test_rejection_rule_suppresses_doubles():
    plain = [(i * 7 + 3) % N for i in range(4000)]
    ks = [(i * 11 + 5) % N for i in range(97)]
    ct = apply_rejection(plain, ks, model='KEY_BUMP')
    doubles = sum(1 for a, b in zip(ct, ct[1:]) if a == b)
    assert doubles == 0, 'absolute KEY_BUMP must leave no adjacent repeats'


def test_all_solved_pages_reproduce():
    from verify_ground_truth import SOLUTIONS, decrypt
    for name in SOLVED:
        page = RuneText.from_page(SOURCES, name)
        expect = RuneText.from_page(SOURCES, 'solved_' + name)
        got = decrypt(page, SOLUTIONS[name])
        assert got == expect.indices, f'{name} did not reproduce'


def test_gematria_primus_is_first_29_primes():
    from lp import gematria as g
    assert PRIMES[:5] == [2, 3, 5, 7, 11]
    assert sum(PRIMES) == 1480
    assert g.value('\u16a0') == 2            # F
    assert g.value('\u16e0') == 109          # EA
    assert g.value('\u16a0\u16e0') == 111


def test_3301_is_prime_and_emirp():
    from lp import gematria as g
    assert g.is_prime(3301)
    assert g.is_emirp(3301)
    assert g.reverse(3301) == 1033
    assert g.is_prime(1033)


def test_totient_of_prime_is_p_minus_one():
    from lp import gematria as g
    for p in (2, 3, 5, 7, 11, 3301):
        assert g.totient(p) == p - 1


def test_magic_square_constant_is_3301():
    from magic_square import SQUARE_5
    n = len(SQUARE_5)
    sums = [sum(r) for r in SQUARE_5]
    sums += [sum(SQUARE_5[i][j] for i in range(n)) for j in range(n)]
    sums.append(sum(SQUARE_5[i][i] for i in range(n)))
    sums.append(sum(SQUARE_5[i][n - 1 - i] for i in range(n)))
    assert set(sums) == {3301}, f'not magic: {sorted(set(sums))}'


def test_an_end_hash_is_sha512_width():
    from magic_square import AN_END_HASH
    assert len(AN_END_HASH) == 128
    int(AN_END_HASH, 16)  # must be valid hex


def test_translit_reproduces_published_keys():
    """Spelling the keywords one rune per letter gives Cicada's exact keys,
    which pins down how Cicada turned words into shift sequences."""
    from lp.translit import to_indices
    assert to_indices('DIVINITY', False) == [23, 10, 1, 10, 9, 10, 16, 26]
    assert to_indices('FIRFUMFERENFE', False) == [0, 10, 4, 0, 1, 19, 0, 18,
                                                   4, 18, 9, 0, 18]


def test_translit_digraphs():
    from lp.translit import to_runes
    assert to_runes('THING') == '\u16a6\u16dd'       # TH + ING
    assert to_runes('QUESTION').startswith('\u16b3\u16b9')   # QU -> CW


def test_hash_stream_is_deterministic_in_range_and_flat():
    from itertools import islice
    from lp.keystream import hash_stream
    a = list(islice(hash_stream('3301'), 29 * 400))
    b = list(islice(hash_stream('3301'), 29 * 400))
    assert a == b
    assert min(a) >= 0 and max(a) <= 28
    from collections import Counter
    c = Counter(a)
    assert len(c) == 29
    assert max(c.values()) < 2 * min(c.values())    # no gross bias
    assert list(islice(hash_stream('3302'), 50)) != a[:50]


def test_three_magic_squares():
    from magic_square import SQUARE_5, SQUARE_WORDS, SQUARE_7, words_to_numbers

    def lines(sq):
        n = len(sq)
        out = [sum(r) for r in sq] + [sum(sq[i][j] for i in range(n)) for j in range(n)]
        return set(out + [sum(sq[i][i] for i in range(n)),
                          sum(sq[i][n - 1 - i] for i in range(n))])
    assert lines(SQUARE_5) == {3301}
    assert lines(words_to_numbers(SQUARE_WORDS)) == {1033}
    assert lines(SQUARE_7) == {1033}


def test_2013_parable_numbers():
    """The Parable printed with 761.mp3: each line sums to a prime and their
    product is the number Cicada attached to it; the mp3's title sums to 761."""
    from lp import gematria as g
    from lp.translit import to_runes
    lines = ['LIKE THE INSTAR TUNNELING TO THE SURFACE',
             'WE MUST SHED OUR OWN CIRCUMFERENCES',
             'FIND THE DIVINITY WITHIN AND EMERGE']
    vals = [g.value(to_runes(x)) for x in lines]
    assert vals == [1259, 1031, 1229]
    assert all(g.is_prime(v) for v in vals)
    assert vals[0] * vals[1] * vals[2] == 1595277641
    assert g.value(to_runes('THE INSTAR EMERGENCE')) == 761


def test_skip_decoder_recovers_text_and_naive_decode_fails():
    import random
    from lp.decode import encrypt_key_skip, undo_key_skip
    from lp.score import Scorer
    sc = Scorer(os.path.join(SOURCES, 'data'), n=3)
    plain = RuneText.from_page(SOURCES, 'solved_jpg107-167').indices
    rng = random.Random(5)
    ks = [rng.randrange(29) for _ in range(int(len(plain) * 1.3))]
    ct = encrypt_key_skip(plain, ks, 0.8, random.Random(9))
    got = undo_key_skip(ct, ks, sc, beam=8)
    acc = sum(a == b for a, b in zip(got, plain)) / len(plain)
    assert acc > 0.97, acc
    naive = cipher.vigenere_decrypt(ct, ks[:len(ct)])
    assert sum(a == b for a, b in zip(naive, plain)) / len(plain) < 0.5


if __name__ == '__main__':
    fns = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f'PASS  {fn.__name__}')
        except Exception as e:
            failed += 1
            print(f'FAIL  {fn.__name__}: {e}')
    print(f'\n{len(fns) - failed}/{len(fns)} passed')
    sys.exit(1 if failed else 0)
