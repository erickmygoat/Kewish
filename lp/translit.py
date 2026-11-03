"""English text -> rune indices, for turning candidate keywords into keys.

Greedy longest-match over Cicada's digraph runes (ING/NG, TH, EO, OE, AE,
IO/IA, EA), then single letters. C/K -> ᚳ, U/V -> ᚢ, S/Z -> ᛋ, Q -> ᚳ
(the solved pages spell QUESTION as CWESTIAN). Non-letters are dropped.

`digraphs=False` maps letter by letter instead, since a keyword's intended
spelling is ambiguous (Cicada spelled DIVINITY one rune per letter).
"""
from .alphabet import INDEX

_MULTI = [('QU', 'ᚳᚹ'), ('ING', 'ᛝ'), ('NG', 'ᛝ'), ('TH', 'ᚦ'), ('EO', 'ᛇ'), ('OE', 'ᛟ'),
          ('AE', 'ᚫ'), ('IO', 'ᛡ'), ('IA', 'ᛡ'), ('EA', 'ᛠ')]
_SINGLE = {'F': 'ᚠ', 'U': 'ᚢ', 'V': 'ᚢ', 'O': 'ᚩ', 'R': 'ᚱ', 'C': 'ᚳ',
           'K': 'ᚳ', 'Q': 'ᚳ', 'G': 'ᚷ', 'W': 'ᚹ', 'H': 'ᚻ', 'N': 'ᚾ',
           'I': 'ᛁ', 'J': 'ᛄ', 'P': 'ᛈ', 'X': 'ᛉ', 'S': 'ᛋ', 'Z': 'ᛋ',
           'T': 'ᛏ', 'B': 'ᛒ', 'E': 'ᛖ', 'M': 'ᛗ', 'L': 'ᛚ', 'D': 'ᛞ',
           'A': 'ᚪ', 'Y': 'ᚣ'}


def to_runes(text, digraphs=True):
    s = ''.join(ch for ch in text.upper() if ch.isalpha())
    out, i = [], 0
    while i < len(s):
        if digraphs:
            for latin, rune in _MULTI:
                if s.startswith(latin, i):
                    out.append(rune)
                    i += len(latin)
                    break
            else:
                out.append(_SINGLE[s[i]])
                i += 1
        else:
            out.append(_SINGLE[s[i]])
            i += 1
    return ''.join(out)


def to_indices(text, digraphs=True):
    return [INDEX[r] for r in to_runes(text, digraphs)]
