import re
import sys

class Token:

	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __repr__(self):
		return self.kind

class LexerTemplate:

    regexExpressions = [
		(r'[\n]+',None),
		(r'\=','ASSIGN'),
		(r'\;','SEMICOLON'),
		(r'\|','PIPE'),
		(r'\,','COMMA'),
		(r'\-','SUB'),
		(r'\*','MUL'),
		(r'^\[$','LBRACKET'),
		(r'\]','RBRACKET'),
		(r'\{','LBRACE'),
		(r'\}','RBRACE'),
		(r'\(','LPAREN'),
		(r'\)','RPAREN'),
		(r'\?','INTERROGATION'),
		(r'\'','SQUOTE'),
		(r'\"','DQUOTE'),
		(r'\\','BSLASH')]

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