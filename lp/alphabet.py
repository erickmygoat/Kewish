"""The 29-rune Anglo-Saxon futhorc alphabet used throughout Liber Primus.

Rune order is the Gematria Primus order; index i in 0..28 carries prime
PRIMES[i]. Source of truth for ordering/letters: relikd/LiberPrayground
LP/Alphabet.py, cross-checked against rtkd/iddqd's master transcription
(which contains exactly these 29 codepoints and no others).
"""

# (prime, rune, [letter forms]) -- last letter form is the display form.
ALPHABET = [
    (2, 'ᚠ', ['F']),      (3, 'ᚢ', ['V', 'U']),   (5, 'ᚦ', ['TH']),
    (7, 'ᚩ', ['O']),      (11, 'ᚱ', ['R']),       (13, 'ᚳ', ['K', 'C']),
    (17, 'ᚷ', ['G']),     (19, 'ᚹ', ['W']),       (23, 'ᚻ', ['H']),
    (29, 'ᚾ', ['N']),     (31, 'ᛁ', ['I']),       (37, 'ᛄ', ['J']),
    (41, 'ᛇ', ['EO']),    (43, 'ᛈ', ['P']),       (47, 'ᛉ', ['X']),
    (53, 'ᛋ', ['Z', 'S']),(59, 'ᛏ', ['T']),       (61, 'ᛒ', ['B']),
    (67, 'ᛖ', ['E']),     (71, 'ᛗ', ['M']),       (73, 'ᛚ', ['L']),
    (79, 'ᛝ', ['ING', 'NG']), (83, 'ᛟ', ['OE']),  (89, 'ᛞ', ['D']),
    (97, 'ᚪ', ['A']),     (101, 'ᚫ', ['AE']),     (103, 'ᚣ', ['Y']),
    (107, 'ᛡ', ['IO', 'IA']), (109, 'ᛠ', ['EA']),
]

N = 29
assert len(ALPHABET) == N

RUNES = [r for _, r, _ in ALPHABET]
PRIMES = [p for p, _, _ in ALPHABET]
INDEX = {r: i for i, r in enumerate(RUNES)}
LETTERS = {r: ls[-1] for _, r, ls in ALPHABET}
PRIME_OF = {r: p for p, r, _ in ALPHABET}

# Non-rune glyphs that carry punctuation/structure rather than a rune value.
PUNCT = {'•': ' ', '⁘': '.', '⁚': ',', '⁖': ';', '⁜': '#', '-': '', '/': '\n'}

INTERRUPT = 'ᚠ'          # the rune left unencrypted on some solved pages
INTERRUPT_INDEX = 0

def is_rune(ch):
    return ch in INDEX

def to_letters(runes):
    """Render a rune string as its latin transliteration."""
    out = []
    for ch in runes:
        if ch in LETTERS:
            out.append(LETTERS[ch])
        elif ch in PUNCT:
            out.append(PUNCT[ch])
        else:
            out.append(ch)
    return ''.join(out)
