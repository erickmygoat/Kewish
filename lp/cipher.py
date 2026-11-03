"""Decryption primitives for Liber Primus.

Everything here works on rune *indices* mod 29.

The one non-obvious mechanic is the **interrupt**. On three solved pages the
author left some plaintext `ᚠ` (index 0) unencrypted. Such a rune passes
through untouched *and does not consume a key value*, so it shifts the
alignment of everything after it. Which `ᚠ` occurrences are interrupts is
not derivable from the ciphertext alone -- it is a per-page set, given here
as 1-based occurrence numbers (`interrupts={4, 5, ...}` means the 4th and
5th `ᚠ` in the page are interrupts).
"""
from .alphabet import INTERRUPT_INDEX

N = 29


def _interrupt_mask(indices, interrupts):
    """True where a rune is an interrupt and must be skipped."""
    mask = [False] * len(indices)
    if not interrupts:
        return mask
    seen = 0
    for i, v in enumerate(indices):
        if v == INTERRUPT_INDEX:
            seen += 1
            if seen in interrupts:
                mask[i] = True
    return mask


def vigenere_decrypt(indices, key, interrupts=None, key_offset=0):
    """plaintext = (cipher - key) mod 29, skipping interrupts.

    `key` is a list of shift values. `key_offset` rotates the starting
    position within the key.
    """
    if not key:
        return list(indices)
    mask = _interrupt_mask(indices, interrupts)
    out = []
    k = key_offset
    for v, skip in zip(indices, mask):
        if skip:
            out.append(v)
        else:
            out.append((v - key[k % len(key)]) % N)
            k += 1
    return out


def sequence_decrypt(indices, stream, interrupts=None):
    """plaintext = (cipher - stream[n]) mod 29, skipping interrupts.

    `stream` is any iterable of integers consumed one per non-interrupt
    rune -- this is the shape that solves "An End" (totient of primes).
    """
    mask = _interrupt_mask(indices, interrupts)
    it = iter(stream)
    out = []
    for v, skip in zip(indices, mask):
        if skip:
            out.append(v)
        else:
            out.append((v - next(it)) % N)
    return out


def invert(indices):
    """Atbash on rune values (the 'invert Gematria' operation)."""
    return [(28 - v) % N for v in indices]


def vigenere_encrypt(indices, key, key_offset=0):
    """Inverse of `vigenere_decrypt` with no interrupts -- used to build
    known-answer test fixtures."""
    if not key:
        return list(indices)
    return [(v + key[(i + key_offset) % len(key)]) % N
            for i, v in enumerate(indices)]
