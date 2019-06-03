import re
import sys


class LexemDictionary():

    regexExpressions = [
        # White space
        # (r'[\t]+', None),
        # (r'[ ]+', None),
        (r'[\n]+',   None),
        # Punctuation
        (r'\:\=',   ':='),
        (r'\&\&',   '&&'),
        (r'\<\=',   '<='),
        (r'\>\=',   '>='),
        (r'\!\=',   '!='),
        (r'\|\|',   '||'),
        (r'\-\-',   '--'),
        (r'\-\=',   '-='),
        (r'\+\+',   '++'),
        (r'\+\=',   '+='),
        (r'\=\=',   '=='),
        (r'\(',   '('),
        (r'\)',   ')'),
        (r'\{',   '{'),
        (r'\}',   '}'),
        (r'^\[$', '['),
        (r'\]',   ']'),
        (r'\;' ,  ';'),
        (r'\:',   ':'),
        (r'\,',   ','),
        (r'\.',   '.'),
        (r'\=',   '='),
        (r'\+',   '+'),
        (r'\-',   '-'),
        (r'\!',   '!'),
        (r'\?',   '?'),
        (r'\*',   '*'),
        (r'\/',   '/'),
        (r'\<',   '<'),
        (r'\>',   '>'),
        (r'\&',   '&'),
        (r'\|',    '|'),
        (r'\#',   '#'),
        (r'\\',   '\\'),
        (r'\/',   '/'),
        (r'\'',   "'"),
        (r'\"',   '"')
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
