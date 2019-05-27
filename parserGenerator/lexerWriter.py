import re
from visitor import Visitor
from lexemDictionary import LexemDictionary
from file import File

class LexerWriter(Visitor):

    def __init__(self,name="results/lexerWriter/lexerWriter_output.py"):
        self.lexemDictionary = LexemDictionary()
        self.lexemList = [(r'[\n]+', "None")]
        self.file=File(name)

    def write(self,lexemList):
        self.file.write("""import re
import sys

class Token:

	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __repr__(self):
		return self.kind

class LexerTemplate:

    regexExpressions = [\n\t\t""")
        for lexem in self.lexemList[0:-1]:
            self.file.write('(r\''+lexem[0]+'\','+lexem[1]+'),\n\t\t')
        self.file.write('(r\''+lexemList[-1][0]+'\','+lexemList[-1][1]+')')
        self.file.write("""]

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
        return self.tokens""")

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        lexemToTest = terminalStringSQuote.value[1:-1] # to reomve quotes
        regexExpressions = self.lexemDictionary.regexExpressions
        match = None
        end = False
        for tokenRegex in regexExpressions:
            pattern, tag = tokenRegex
            regex = re.compile(pattern)
            match = regex.match(lexemToTest)
            if match:
                if (tokenRegex[0],"'"+tokenRegex[1]+"'") in self.lexemList:
                    end = True
                    break
                data = match.group(0)
                if tag:
                    self.lexemList.append((tokenRegex[0],"'"+tokenRegex[1]+"'"))
                    break
        if not(match) and not(end) and not((lexemToTest,"'"+lexemToTest.upper()+"'") in self.lexemList):
            self.lexemList.append((lexemToTest,"'" + lexemToTest.upper() + "'"))


    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.visitTerminalStringSQuote(terminalStringDQuote)
