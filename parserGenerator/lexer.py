import re
import sys
from token1 import Token

regexExpressions = [
    (r'\(\*[\s\S]*?\*\)', 'COMMENT'),
    # Whitespaces
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


class Lexer:

    def __init__(self):
        self.tokens = []

    # inputText = open("testFile.c").readlines()
    def lex(self, inputText):

        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            # print(line)
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                        break
                if not match:
                    print(inputText[position])
                    print("No match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("Lexer: analysis successful!")
        return self.tokens
