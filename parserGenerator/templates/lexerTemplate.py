import re
import sys
from token1 import Token
from lexemDictionary import LexemDictionary

class LexerTemplate:

    regexExpressions = []

    def __init__(self):
        self.tokens = []


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
