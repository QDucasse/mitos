from visitor import Visitor
from lexemDictionary import LexemDictionary

class LexerWriter(Visitor):

    def write(self,lexemList):
        pass

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        lexemToTest = terminalStringSQuote.value
        regexExpressions = lexemDictionary.regexExpressions
        match = None
        for tokenRegex in regexExpressions:
            pattern, tag = tokenRegex
            regex = re.compile(pattern)
            match = regex.match(line, position)
            if match:
                data = match.group(0)
                if tag:
                    # Ajout à la liste des lexemes -> Fichier py
                break
        if not match:
            print(inputText[position])
            print("No match")
            sys.exit(1)
