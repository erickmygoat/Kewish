"""Loading and slicing Liber Primus rune text.

Two input shapes are supported:

* **Page files** (relikd/LiberPrayground `pages/*.txt`) -- runes interleaved
  with punctuation glyphs and newlines, one file per page group.
* **Master transcription** (rtkd/iddqd) -- one file for the whole book with
  explicit delimiters: `%` page, `§` chapter, `$` segment, `&` paragraph,
  `.` clause, `-` word, `/` line.

Both reduce to the same thing: a list of rune indices (0..28) with the
non-rune glyphs kept alongside so output can be re-rendered readably.
"""
import os
from .alphabet import INDEX, RUNES, is_rune

# Page groups as named by relikd/LiberPrayground.
SOLVED = ['0_warning', '0_welcome', '0_wisdom', '0_koan_1',
          '0_loss_of_divinity', 'jpg107-167', 'jpg229',
          'p56_an_end', 'p57_parable']
UNSOLVED = ['p0-2', 'p3-7', 'p8-14', 'p15-22', 'p23-26',
            'p27-32', 'p33-39', 'p40-53', 'p54-55']

MASTER_DELIMS = {'%': 'page', '§': 'chapter', '$': 'segment',
                 '&': 'paragraph', '.': 'clause', '-': 'word', '/': 'line'}


class RuneText:
    """A rune stream plus the glyphs around it.

    `tokens` is the original character sequence. `indices` holds only the
    rune values, and `positions` maps each rune back to its token offset,
    so a decrypted stream can be stitched back into the original layout.
    """

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.indices = []
        self.positions = []
        for i, ch in enumerate(self.tokens):
            if is_rune(ch):
                self.positions.append(i)
                self.indices.append(INDEX[ch])

    def __len__(self):
        return len(self.indices)

    @classmethod
    def from_string(cls, s):
        return cls(s)

    @classmethod
    def from_page(cls, root, name):
        with open(os.path.join(root, 'pages', name + '.txt'), encoding='utf-8') as f:
            return cls(f.read())

    def inverted(self):
        """Atbash on the rune values: index -> 28 - index."""
        out = list(self.tokens)
        for pos, idx in zip(self.positions, self.indices):
            out[pos] = RUNES[28 - idx]
        return RuneText(out)

    def with_indices(self, new_indices):
        """Return a copy where rune slots are replaced by `new_indices`."""
        assert len(new_indices) == len(self.indices)
        out = list(self.tokens)
        for pos, idx in zip(self.positions, new_indices):
            out[pos] = RUNES[idx % 29]
        return RuneText(out)

    @property
    def runes(self):
        return ''.join(RUNES[i] for i in self.indices)

    def render(self):
        from .alphabet import to_letters
        return to_letters(''.join(self.tokens))


def load_master(path):
    """Parse the iddqd master transcription into {segment_id: RuneText}.

    Segments are delimited by `$` and are the unit the published key list
    (`liber-primus__keys.txt`) is indexed by.
    """
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    # Drop the delimiter legend header: content starts at the first rune.
    first = next(i for i, ch in enumerate(raw) if is_rune(ch))
    body = raw[first:]
    segments = {}
    chapter = 0
    seg = 0
    buf = []
    for ch in body:
        if ch == '§':
            if buf:
                segments[f'{chapter}.{seg}'] = RuneText(buf)
                buf = []
            chapter += 1
            seg = 0
        elif ch == '$':
            segments[f'{chapter}.{seg}'] = RuneText(buf)
            buf = []
            seg += 1
        else:
            buf.append(ch)
    if any(is_rune(c) for c in buf):
        segments[f'{chapter}.{seg}'] = RuneText(buf)
    return segments
