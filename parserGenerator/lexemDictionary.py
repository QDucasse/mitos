import re
import sys


class LexemDictionary():

    regexExpressions = [
        # White space
        # (r'[\t]+', None),
        # (r'[ ]+', None),
        (r'[\n]+',   None),
        # Punctuation
        (r'\:\=',   'ALLOCATE'),
        (r'\&\&',   'DAMPERSAND'),
        (r'\<\=',   'LTE'),
        (r'\>\=',   'GTE'),
        (r'\!\=',   'NEQ'),
        (r'\|\|',   'DBAR'),
        (r'\-\-',   'SUBSUB'),
        (r'\-\=',   'SUBEQ'),
        (r'\+\+',   'ADDADD'),
        (r'\+\=',   'ADDEQ'),
        (r'\=\=',   'EQ'),
        (r'\(',   'LPAREN'),
        (r'\)',   'RPAREN'),
        (r'\{',   'LBRACE'),
        (r'\}',   'RBRACE'),
        (r'^\[$', 'LBRACKET'),
        (r'\]',   'RBRACKET'),
        (r'\;' ,  'SEMICOLON'),
        (r'\:',   'COLON'),
        (r'\,',   'COMMA'),
        (r'\.',   'DOT'),
        (r'\=',   'ASSIGN'),
        (r'\+',   'ADD'),
        (r'\-',   'SUB'),
        (r'\!',   'NOT'),
        (r'\?',   'INTERROGATION'),
        (r'\*',   'MUL'),
        (r'\/',   'DIV'),
        (r'\<',   'LT'),
        (r'\>',   'GT'),
        (r'\&',   'AMPERSAND'),
        (r'\|',    'PIPE'),
        (r'\#',   'SHARP'),
        (r'\\',   'BSLASH'),
        (r'\/',   'FSLASH'),
        (r'\'',   'SQUOTE'),
        (r'\"',   'DQUOTE')
        # Identifiant, chaines de
        # (r'\d+\.\d+',    'FLOAT_LIT'),
        # (r'\d+',         'INTEGER_LIT'),
        # (r'\"[^\"]*\"',  'STRING_LIT'),
        # (r'\'[^\"]*\'',  'CHAR_LIT')
    ]

    def associateExpression(self,expression):
        match = None
        for tokenTuple in lexemDictionary:
            pattern, tag = tokenTuple
            regex = re.compile(pattern)
            match = regex.match(line, position)
            if match:
                data = match.group(0)
                if tag:
                    return tokenTuple
                break
            if not match:
                print(inputText[position])
                print("No match")
                sys.exit(1)
