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
		(r'#include','#include'),
		(r'\<','<'),
		(r'\>','>'),
		(r'using','using'),
		(r'namespace','namespace'),
		(r'\;',';'),
		(r'int','int'),
		(r'double','double'),
		(r'\-','-'),
		(r'cos','cos'),
		(r'sin','sin'),
		(r'pow','pow'),
		(r'sqrt','sqrt'),
		(r'\(','('),
		(r'\,',','),
		(r'\)',')'),
		(r'std::','std::'),
		(r'cout','cout'),
		(r'\<<','<<'),
		(r'endl','endl'),
		(r'\=\=','=='),
		(r'\=','='),
		(r'\+','+'),
		(r'\:',':'),
		(r'\<\=','<='),
		(r'\>\=','>='),
		(r'\/','/'),
		(r'\*','*'),
		(r'if','if'),
		(r'\{','{'),
		(r'\}','}'),
		(r'else if','else if'),
		(r'else','else'),
		(r'for','for'),
		(r'while','while'),
		(r'return','return'),
		(r'main','main'),
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
		(r'a','a'),
		(r'b','b'),
		(r'c','c'),
		(r'd','d'),
		(r'e','e'),
		(r'f','f'),
		(r'g','g'),
		(r'h','h'),
		(r'i','i'),
		(r'j','j'),
		(r'k','k'),
		(r'l','l'),
		(r'm','m'),
		(r'n','n'),
		(r'o','o'),
		(r'p','p'),
		(r'q','q'),
		(r'r','r'),
		(r's','s'),
		(r't','t'),
		(r'u','u'),
		(r'v','v'),
		(r'w','w'),
		(r'x','x'),
		(r'y','y'),
		(r'z','z'),
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
		(r'\.','.'),
		(r'\"','"'),
		(r'\?','?'),
		(r'_','_'),
		(r'\!','!')]

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
