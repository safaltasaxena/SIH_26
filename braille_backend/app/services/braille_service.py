# Based on the project's existing 6-dot Braille mapping.
# The original prototype uses the same style of binary representation.

from typing import List, Tuple


BRAILLE = {
    'a': [1, 0, 0, 0, 0, 0],
    'b': [1, 1, 0, 0, 0, 0],
    'c': [1, 0, 0, 1, 0, 0],
    'd': [1, 0, 0, 1, 1, 0],
    'e': [1, 0, 0, 0, 1, 0],
    'f': [1, 1, 0, 1, 0, 0],
    'g': [1, 1, 0, 1, 1, 0],
    'h': [1, 1, 0, 0, 1, 0],
    'i': [0, 1, 0, 1, 0, 0],
    'j': [0, 1, 0, 1, 1, 0],
    'k': [1, 0, 1, 0, 0, 0],
    'l': [1, 1, 1, 0, 0, 0],
    'm': [1, 0, 1, 1, 0, 0],
    'n': [1, 0, 1, 1, 1, 0],
    'o': [1, 0, 1, 0, 1, 0],
    'p': [1, 1, 1, 1, 0, 0],
    'q': [1, 1, 1, 1, 1, 0],
    'r': [1, 1, 1, 0, 1, 0],
    's': [0, 1, 1, 1, 0, 0],
    't': [0, 1, 1, 1, 1, 0],
    'u': [1, 0, 1, 0, 0, 1],
    'v': [1, 1, 1, 0, 0, 1],
    'w': [0, 1, 0, 1, 1, 1],
    'x': [1, 0, 1, 1, 0, 1],
    'y': [1, 0, 1, 1, 1, 1],
    'z': [1, 0, 1, 0, 1, 1],
    ' ': [0, 0, 0, 0, 0, 0],
}

NUMBER_PREFIX = [0, 1, 1, 1, 1, 1]

NUMBERS_MAP = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
    '7': 'g',
    '8': 'h',
    '9': 'i',
    '0': 'j',
}

PUNCTUATION = {
    '.': [0, 1, 0, 0, 1, 1],
    ',': [0, 1, 0, 0, 0, 0],
    ';': [0, 1, 1, 0, 0, 0],
    ':': [0, 1, 0, 0, 1, 0],
    '?': [0, 1, 1, 0, 0, 1],
    '!': [0, 1, 1, 0, 1, 0],
    '-': [0, 0, 1, 0, 0, 1],
    "'": [0, 0, 1, 0, 0, 0],
    '"': [0, 0, 1, 0, 1, 0],
    '(': [0, 1, 1, 1, 0, 1],
    ')': [0, 1, 1, 1, 0, 1],
}

CUSTOM = {
    '/': [0, 0, 1, 1, 0, 0],
    '@': [0, 1, 0, 1, 1, 1],
    '#': [1, 0, 1, 1, 1, 0],
    '&': [1, 0, 1, 0, 1, 1],
    '%': [0, 1, 1, 0, 1, 1],
    '*': [0, 0, 1, 1, 1, 0],
    '+': [0, 0, 1, 1, 1, 1],
    '=': [0, 1, 1, 1, 0, 0],
}


def convert_text_to_braille(text: str) -> Tuple[List[List[int]], List[str]]:
    data = []
    unsupported = []

    for char in text.lower():
        if char in NUMBERS_MAP:
            data.append(NUMBER_PREFIX)
            data.append(BRAILLE[NUMBERS_MAP[char]])

        elif char in BRAILLE:
            data.append(BRAILLE[char])

        elif char in PUNCTUATION:
            data.append(PUNCTUATION[char])

        elif char in CUSTOM:
            data.append(CUSTOM[char])

        elif char.isspace():
            data.append(BRAILLE[' '])

        else:
            unsupported.append(char)
            # Show a question mark instead of silently dropping it.
            data.append(PUNCTUATION['?'])

    return data, sorted(set(unsupported))


def binary_to_unicode(binary: List[List[int]]) -> str:
    result = []

    for cell in binary:
        value = 0

        for index, dot in enumerate(cell):
            if dot:
                value |= 1 << index

        result.append(chr(0x2800 + value))

    return "".join(result)
