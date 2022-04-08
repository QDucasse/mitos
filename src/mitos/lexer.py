# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import re
import sys

regexExpressions = [
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
    (r'\'[^\']*\'',         'SQUOTE'),
    (r'\"[^\"]*\"',         'DQUOTE'),
    (r'\?[^\?]*\?',         'SPECIAL'),
    (r'\(',                 'LPAREN'),
    (r'\)',                 'RPAREN'),
    (r'\{',                 'LBRACE'),
    (r'\}',                 'RBRACE'),
    (r'\[',                 'LBRACKET'),
    (r'\]',                 'RBRACKET'),

    # Identifiers & Integers
    (r'[a-zA-Z]\w*', 'IDENTIFIER'),
    (r'\d+',         'INTEGER'),
]


class Lexem(object):
    '''
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
    '''
    def __init__(self, tag, value, position):
        self.tag      = tag
        self.value    = value
        self.position = position

    def __repr__(self):
        return self.tag


class Lexer:
    '''
    Creates a lexem list from raw program text
    '''

    def __init__(self):
        self.lexems = []

    def lex(self, inputText):
        '''
        Main lexer function:
        Creates a lexem for every detected regular expression
        The lexems are composed of:
            - tag
            - values
            - position
        SEE lexem for more info
        '''
        # Crawl through the input file
        for lineNumber, line in enumerate(inputText):
            lineNumber += 1
            position = 0
            # Crawl through the line
            while position < len(line):
                match = None
                for lexemRegex in regexExpressions:
                    pattern, tag = lexemRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        # This condition is needed to avoid the creation of whitespace lexems
                        if tag:
                            lexem = Lexem(tag, data, [lineNumber, position])
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
