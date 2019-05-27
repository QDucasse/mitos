from visitor import Visitor
from lexemDictionary import LexemDictionary
import re

class SaveFile():
    def __init__(self,name):
        self.f=open(name,"w")

    def write(self,data):
        self.f.write(data)

    def close(self):
        self.f.close()

class LexerWriter(Visitor):

    def __init__(self,name="lexerWriter_output"):
        self.lexemList = []
        self.lexemDictionary = LexemDictionary()
        self.file=SaveFile(name)

    def write(self,lexemList):
        self.file.write("""import re
        import sys
        from token import Token

        class LexerTemplate:

            regexExpressions = [""")
        for lexem in self.lexemList:
            self.file.write(lexem)
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
            return self.tokens""")

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        lexemToTest = terminalStringSQuote.value[1:-1] # to reomve quotes
        print(lexemToTest)
        regexExpressions = self.lexemDictionary.regexExpressions
        match = None
        for tokenRegex in regexExpressions:
            pattern, tag = tokenRegex
            regex = re.compile(pattern)
            match = regex.match(lexemToTest)
            if match:
                data = match.group(0)
                if tag:
                    print(tokenRegex)
                    self.lexemList.append((tokenRegex[0],"'"+tokenRegex[1]+"'"))
                break
        if not match:
            self.lexemList.append((lexemToTest,"'" + lexemToTest.upper() + "'"))


    def visitTerminalStringDQuote(self,terminalStringDQuote):
        lexemToTest = terminalStringDQuote.value[1:-1] # to reomve quotes
        print(lexemToTest)
        regexExpressions = self.lexemDictionary.regexExpressions
        match = None
        for tokenRegex in regexExpressions:
            pattern, tag = tokenRegex
            regex = re.compile(pattern)
            match = regex.match(lexemToTest)
            if match:
                data = match.group(0)
                if tag:
                    print(tokenRegex)
                    self.lexemList.append((tokenRegex[0],"'" +tokenRegex[1] +"'"))
                break
        if not match:
            self.lexemList.append((lexemToTest,"'" + lexemToTest.upper() + "'"))
