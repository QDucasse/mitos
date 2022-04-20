# -*- coding: utf-8 -*-
"""
Lexer that transforms raw source code to lexems
@author: Quentin Ducasse & Kevin Bedin
"""


import re
import sys

regex_expressions = [
    # Comments and whitespaces
    (r'\(\*[\s\S]*?\*\)', 'COMMENT'),
    (r'[ \n\t]+', None),

    # Special characters
    (r'\;', 'TERMINATOR'),
    (r'\,', 'CONCATENATION'),
    (r'\=', 'ASSIGN'),
    (r'\-', 'EXCEPT'),
    (r'\*', 'REPETITION'),
    (r'\|', 'SEPARATOR'),

    # Groups
    (r'\(',                 'LPAREN'),
    (r'\)',                 'RPAREN'),
    (r'\{',                 'LBRACE'),
    (r'\}',                 'RBRACE'),
    (r'\[',                 'LBRACKET'),
    (r'\]',                 'RBRACKET'),

    # Special sequences
    (r'\?[^\?]*\?',  "SPECIAL"),
    (r'(\').*?(\')', "STRING"),
    (r'(\").*?(\")', "STRING"),
    (r'[a-zA-Z]\w*', "IDENTIFIER"),
    (r'\d+',         "INTEGER")
]


class Lexem:
    """
    Our token definition:
    lexem (tag and value) + position in the program raw text

    Parameters
    ----------
    tag: string
        Name of the lexem's type, e.g. IDENTIFIER

    value: string
        Value of the lexem,       e.g. integer1

    position: integer tuple
        Tuple to point out the lexem in the input file (line number, position)
    """
    def __init__(self, tag, value, position):
        self.tag = tag
        self.value = value
        self.position = position

    def __repr__(self):
        return self.tag


class Lexer:
    """
    Creates a lexem list from raw program text
    """

    def __init__(self):
        self.lexems = []

    def lex(self, input_text):
        # Crawl through the input file
        for line_number, line in enumerate(input_text):
            line_number += 1
            position = 0
            # Crawl through the line
            while position < len(line):
                match = None
                for lexem_regex in regex_expressions:
                    pattern, tag = lexem_regex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        # This condition is needed to avoid the creation of whitespace lexems
                        if tag:
                            lexem = Lexem(tag, data, [line_number, position])
                            self.lexems.append(lexem)
                        # Renew the position
                        position = match.end(0)
                        break
                # No match detected --> Wrong syntax in the input file
                if not match:
                    print("No match detected on line and position:")
                    print(line[position:])
                    sys.exit(1)

        print("Lexer: analysis successful!")
        return self.lexems
