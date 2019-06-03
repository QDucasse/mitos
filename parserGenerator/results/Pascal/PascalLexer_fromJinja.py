import sys
import re

class Token:

    def __init__(self, kind, value, position):
        self.kind = kind
        self.value = value
        self.position = position

    def __repr__(self):
        return self.kind

class Lexer:

    regexExpressions = [(r'[\n]+',None),
		(r'PROGRAM','PROGRAM'),
		(r'BEGIN','BEGIN'),
		(r'\;',';'),
		(r'END.','END.'),
		(r'\-','-'),
		(r'\"','"'),
		(r'\:\=',':='),
		(r'A','A'),
		(r'B','B'),
		(r'C','C'),
		(r'D','D'),
		(r'E','E'),
		(r'F','F'),
		(r'G','G'),
		(r'H','H'),
		(r'I','I'),
		(r'J','J'),
		(r'K','K'),
		(r'L','L'),
		(r'M','M'),
		(r'N','N'),
		(r'O','O'),
		(r'P','P'),
		(r'Q','Q'),
		(r'R','R'),
		(r'S','S'),
		(r'T','T'),
		(r'U','U'),
		(r'V','V'),
		(r'W','W'),
		(r'X','X'),
		(r'Y','Y'),
		(r'Z','Z'),
		(r'0','0'),
		(r'1','1'),
		(r'2','2'),
		(r'3','3'),
		(r'4','4'),
		(r'5','5'),
		(r'6','6'),
		(r'7','7'),
		(r'8','8'),
		(r'9','9'),
		(r' ',' '),
		(r'[a-zA-Z0-9 \W]','[a-zA-Z0-9 \W]')]

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
                for tokenRegex in self.regexExpressions:
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
                    print(line[position])
                    print("No match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("Lexer: analysis successful!")
        return self.tokens
