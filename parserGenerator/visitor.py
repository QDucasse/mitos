from lexemDictionary import LexemDictionary

class Visitor:
    def __init__(self):
        lexemDictionary = LexemDictionary()

    def visit(self,grammar):
        grammar.accept(self,grammar)

    def visitGrammar(self,grammar):
        # Visits grammar
        syntax = grammar.syntax
        syntax.accept(self,syntax)
        # ARGS
        # self.syntax = syntax

    def visitSyntax(self,syntax):
        # Visits all syntax rules
        for syntaxRule in syntax.syntaxRules:
            syntaxRule.accept(self,syntaxRule)
        # ARGS
        # self.syntaxRules = syntaxRules

    def visitSyntaxRule(self,syntaxRule):
        # Visits identifier
        id   = syntaxRule.identifier
        # Visits all definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)
        # ARGS
        # self.identifier  = identifier
        # self.definitions = definitions

    def visitDefinitions(self,definitions):
        # Visits all definitions
        for definition in definitions.definitions:
            definition.accept(self,definition)
        # ARGS
        # self.definitions = definitions

    def visitDefinition(self,definition):
        # Visits all terms
        for term in definition.terms:
            term.accept(self,term)
        # ARGS
        #self.terms = []

    def visitTerm(self,term):
        # Visits the factor
        term.factor.accept(self,term.factor)
        # Visits the exception
        exception = term.exception
        if exception != None:
            term.exception.accept(self,term.exception)
        # ARGS
        # self.factor    = factor
        # self.exception = exception

    def visitException(self,exception):
        # Visits the exception
        exception.factor.accept(self,exception.factor)
        # ARGS
        # self.factor = factor

    def visitFactor(self,factor):
        # Visits the primary
        factor.primary.accept(self,factor.primary)
        # ARGS
        # self.integer = integer
        # self.primary = primary

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
        # ARGS
        # self.optionalSeq    = optionalSeq
        # self.repeatedSeq    = repeatedSeq
        # self.groupedSeq     = groupedSeq
        # self.specialSeq     = specialSeq
        # self.terminalString = terminalString
        # self.identifier     = identifier
        # self.empty          = empty

    def visitOptionalSeq(self,optionalSeq):
        optionalSeq.definitions.accept(self,optionalSeq.definitions)
        # ARGS
        # self.definitions = definitions

    def visitRepeatedSeq(self,repeatedSeq):
        repeatedSeq.definitions.accept(self,repeatedSeq.definitions)
        # ARGS
        # self.definitions = definitions

    def visitGroupedSeq(self,groupedSeq):
        groupedSeq.definitions.accept(self,groupedSeq.definitions)
        # ARGS
        # self.definitions = definitions

    def visitSpecialSeq(self,specialSeq):
        pass
        # ARGS
        # self.definitions = definitions

    def visitTerminalString(self,terminalString):
        
        # ARGS
        # self.value = value

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        pass
        # ARGS
        # self.value = value

    def visitTerminalStringDQuote(self,terminalStringDQuote):
        pass
        # ARGS
        # self.value = value

    def visitIdentifier(self,identifier):
        pass
        # ARGS
        # self.value = value

    def visitEmpty(self,empty):
        pass

    def visitInteger(self,integer):
        pass
        # ARGS
        # self.value = value
