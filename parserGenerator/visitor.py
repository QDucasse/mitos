

class Visitor:

    def visit():
        pass

    def visitGrammar():
        pass
        # ARGS
        # self.syntax = syntax

    def visitSyntax():
        pass
        # ARGS
        # self.syntaxRules = syntaxRules

    def visitSyntaxRule():
        pass
        # ARGS
        # self.identifier  = identifier
        # self.definitions = definitions

    def visitDefinitions():
        pass
        # ARGS
        # self.definitions = definitions

    def visitDefinition():
        pass
        # ARGS
        #self.terms = []

    def visitTerm():
        pass
        # ARGS
        # self.factor    = factor
        # self.exception = exception

    def visitException():
        pass
        # ARGS
        # self.factor = factor

    def visitFactor():
        pass
        # ARGS
        # self.integer = integer
        # self.primary = primary

    def visitPrimary():
        pass
        # ARGS
        # self.optionalSeq    = optionalSeq
        # self.repeatedSeq    = repeatedSeq
        # self.groupedSeq     = groupedSeq
        # self.specialSeq     = specialSeq
        # self.terminalString = terminalString
        # self.identifier     = identifier
        # self.empty          = empty

    def visitOptionalSeq():
        pass
        # ARGS
        # self.definitions = definitions

    def visitRepeatedSeq(Node):
        pass
        # ARGS
        # self.definitions = definitions

    def visitGroupedSeq(Node):
        pass
        # ARGS
        # self.definitions = definitions

    def visitSpecialSeq(Node):
        pass
        # ARGS
        # self.definitions = definitions

    def visitTerminalString():
        pass
        # ARGS
        # self.value = value

    def visitIdentifier():
        pass
        # ARGS
        # self.value = value

    def visitEmpty():
        pass

    def visitInteger():
        pass
        # ARGS
        # self.value = value
