import re
import sys

class LexemDictionary():

    regexExpressions = [
        # White space
        (r'[ \n\t]+', None),
        (r'#[^\n]*', None),  #Commentaires
        # Punctuation
        (r'\(',   'LPAREN'),
        (r'\)',   'RPAREN'),
        (r'\{',   'LBRACE'),
        (r'\}',   'RBRACE'),
        (r'\[',   'LBRACKET'),
        (r'\]',   'RBRACKET'),
        (r'\;',   'SEMICOLON'),
        (r'\:',   'COLON'),
        (r'\,',   'COMMA'),
        (r'\.',   'DOT'),
        (r'\=\=', 'EQ'),
        (r'\=',   'ASSIGN'),
        (r'\+\+', 'ADDADD'),
        (r'\+\=', 'ADDEQ'),
        (r'\+',   'ADD'),
        (r'\-\-', 'SUBSUB'),
        (r'\-\=', 'SUBEQ'),
        (r'\-',   'SUB'),
        (r'\!',   'NOT'),
        (r'\*',   'MUL'),
        (r'\/',   'DIV'),
        (r'\!\=', 'NEQ'),
        (r'\|\|', 'DBAR'),
        (r'\<',   'LT'),
        (r'\<\=', 'LTE'),
        (r'\>',   'GT'),
        (r'\>\=', 'GTE'),
        (r'\&',   'AMPERSAND'),
        (r'\&\&', 'DAMPERSAND'),
        (r'\#',   'SHARP'),
        (r'\\',   'BSLASH'),
        (r'\/',   'FSLASH'),
        # Identifiant, chaines de
        (r'[a-zA-Z]\w*', 'IDENTIFIER'),
        (r'\d+\.\d+',    'FLOAT_LIT'),
        (r'\d+',         'INTEGER_LIT'),
        (r'\"[^\"]*\"',  'STRING_LIT'),
        (r'\'[^\"]*\'',  'CHAR_LIT')
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
