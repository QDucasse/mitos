from newLexer import NewLexer
from newParser import NewParser

class Visitor:

    def visit(self,grammar):
        grammar.accept(self,grammar)

    def visitGrammar(self,grammar):
        # Visits grammar
        syntax = grammar.syntax
        syntax.accept(self,syntax)

    def visitSyntax(self,syntax):
        # Visits all syntax rules
        for syntaxRule in syntax.syntaxRules:
            syntaxRule.accept(self,syntaxRule)

    def visitSyntaxRule(self,syntaxRule):
        # Visits identifier
        id   = syntaxRule.identifier
        # Visits all definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)

    def visitDefinitions(self,definitions):
        # Visits all definitions
        for definition in definitions.definitions:
            definition.accept(self,definition)

    def visitDefinition(self,definition):
        # Visits all terms
        for term in definition.terms:
            term.accept(self,term)

    def visitTerm(self,term):
        # Visits the factor
        term.factor.accept(self,term.factor)
        # Visits the exception
        exception = term.exception
        if exception != None:
            term.exception.accept(self,term.exception)

    def visitException(self,exception):
        # Visits the exception
        exception.factor.accept(self,exception.factor)

    def visitFactor(self,factor):
        # Visits the primary
        factor.primary.accept(self,factor.primary)

    def visitPrimary(self,primary):
        if primary.optionalSeq != None:
            primary.optionalSeq.accept(self,primary.optionalSeq)
        elif primary.identifier != None:
            primary.identifier.accept(self,primary.identifier)
        elif primary.repeatedSeq != None:
            primary.repeatedSeq.accept(self,primary.repeatedSeq)
        elif primary.groupedSeq != None:
            primary.groupedSeq.accept(self,primary.groupedSeq)
        elif primary.specialSeq != None:
            primary.specialSeq.accept(self,primary.specialSeq)
        elif primary.terminalString != None:
            primary.terminalString.accept(self,primary.terminalString)
        elif primary.empty != None:
            primary.empty.accept(self,primary.empty)

    def visitOptionalSeq(self,optionalSeq):
        optionalSeq.definitions.accept(self,optionalSeq.definitions)

    def visitRepeatedSeq(self,repeatedSeq):
        repeatedSeq.definitions.accept(self,repeatedSeq.definitions)

    def visitGroupedSeq(self,groupedSeq):
        groupedSeq.definitions.accept(self,groupedSeq.definitions)

    def visitSpecialSeq(self,specialSeq):
        pass

    def visitTerminalString(self,terminalString):
        pass

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        pass
        # lexemToTest = terminalStringSQuote.value
        # regexExpressions = lexemDictionary.regexExpressions
        # match = None
        # for tokenRegex in regexExpressions:
        #     pattern, tag = tokenRegex
        #     regex = re.compile(pattern)
        #     match = regex.match(line, position)
        #     if match:
        #         data = match.group(0)
        #         if tag:
        #             # Ajout à la liste des lexemes -> Fichier py
        #         break
        # if not match:
        #     print(inputText[position])
        #     print("No match")
        #     sys.exit(1)

    def visitTerminalStringDQuote(self,terminalStringDQuote):
        pass

    def visitIdentifier(self,identifier):
        pass


    def visitEmpty(self,empty):
        pass

    def visitInteger(self,integer):
        pass
