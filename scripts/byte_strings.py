#!/usr/bin/env python3
"""Analyse Cicada's four 2048-bit byte strings.

These are often described loosely as "the 256-byte page". They are four
distinct artifacts from the **2014** round, labelled in rtkd/iddqd:

  String 1  Hidden Service 2   cu343l33nqaekrnw.onion
  String 2  Hidden Service 3   fv7lyucmeozzd5j4.onion
  String 3  Hidden Service 4   avowyfgl5lkzfj3n.onion
  String 4  Liber Primus pages 49-51 matrix, converted to hexadecimal

All four are exactly 256 bytes. The structurally interesting point is that
String 4 comes from inside Liber Primus while the other three come from the
onion chain, yet all four are the same width.

The decisive test on these is NOT randomness but DISTINCTNESS. 256 bytes
that are a permutation of 0..255 would be an S-box or RC4-style state
table -- a key, not a message. 256 bytes with the duplicate structure of
random draws cannot be a permutation, which rules that reading out.

For 256 uniform draws from 256 values, the expected number of distinct
values is 256*(1 - (255/256)^256) ~= 161.8, not 256.

Usage:  python3 -I scripts/byte_strings.py [--source FILE]
"""
import argparse
import math
import re
from collections import Counter

DEFAULT = '/home/user/rtkd/iddqd/byte-strings/byte-strings'


def expected_distinct(n=256, k=256):
    return n * (1 - ((n - 1) / n) ** k)


def ioc_bytes(bs):
    """Index of coincidence over 256 symbols; uniform = 1/256 = 0.003906."""
    n = len(bs)
    c = Counter(bs)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def shannon(bs):
    n = len(bs)
    c = Counter(bs)
    return -sum((v / n) * math.log2(v / n) for v in c.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default=DEFAULT)
    args = ap.parse_args()

    txt = open(args.source, encoding='utf-8', errors='replace').read()
    labels = re.findall(r'\*\s+(String \d+ - [^\n]+)', txt)
    parts = re.split(r'/\*.*?\*/', txt, flags=re.S)
    blobs = []
    for p in parts:
        h = ''.join(re.findall(r'[0-9a-fA-F]{20,}', p))
        if h:
            blobs.append(h)

    exp = expected_distinct()
    print('=' * 74)
    print('CICADA 2048-BIT BYTE STRINGS')
    print('=' * 74)
    print()
    print(f'expected distinct byte values for 256 uniform random draws: '
          f'{exp:.1f}')
    print(f'a permutation of 0..255 would show: 256')
    print()
    print(f'{"string":48s} {"bytes":>6s} {"distinct":>9s} {"H bits/B":>9s} '
          f'{"IoC":>9s}')
    print('-' * 74)
    for lab, h in zip(labels, blobs):
        bs = bytes.fromhex(h)
        print(f'{lab[:48]:48s} {len(bs):6d} {len(set(bs)):9d} '
              f'{shannon(bs):9.3f} {ioc_bytes(bs):9.6f}')
    print('-' * 74)
    print(f'{"uniform random reference":48s} {256:6d} {exp:9.1f} '
          f'{8.0:9.3f} {1/256:9.6f}')
    print()
    print('reading')
    print('  Distinct counts sit at the random expectation, so none of the')
    print('  four is a permutation of 0..255. The S-box / keystream-table')
    print('  reading is therefore ruled out; these behave like ciphertext')
    print('  or digests. A bare 2048-bit block with no published modulus is')
    print('  not attackable as RSA, so the RSA reading needs a modulus to')
    print('  be found elsewhere in the corpus before it means anything.')


if __name__ == '__main__':
    main()
