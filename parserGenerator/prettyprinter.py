from lexemDictionary import LexemDictionary

class SaveFile():
    def __init__(self,name):
        self.f=open(name,"w")
    
    def write(self,data):
        self.f.write(data)
     
    def close(self):
        self.f.close()

class PrettyPrinter:
    def __init__(self,name="prettyprinter_input"):
        lexemDictionary = LexemDictionary()
        self.file=SaveFile(name)

    def visit(self,grammar):
        grammar.accept(self,grammar)
        self.file.close()

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
        self.file.write("=")
        defs.accept(self,defs)
        self.file.write(";\n")
        # ARGS
        # self.identifier  = identifier
        # self.definitions = definitions

    def visitDefinitions(self,definitions):
        # Visits all definitions
        for definition in definitions.definitions[0:-1]:
            definition.accept(self,definition)
            self.file.write("|")
        definitions.definitions[-1].accept(self,definitions.definitions[-1])
        # ARGS
        # self.definitions = definitions

    def visitDefinition(self,definition):
        # Visits all terms
        for term in definition.terms[0:-1]:
            term.accept(self,term)
            self.file.write(",")
        definition.terms[-1].accept(self,definition.terms[-1])
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
        self.file.write("-")
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
            self.file.write("[")
            primary.optionalSeq.accept(self,primary.optionalSeq)
            self.file.write("]")
        elif primary.identifier != None:
            primary.identifier.accept(self,primary.identifier)
        elif primary.repeatedSeq != None:
            self.file.write("{")
            primary.repeatedSeq.accept(self,primary.repeatedSeq)
            self.file.write("}")
        elif primary.groupedSeq != None:
            self.file.write("(")
            primary.groupedSeq.accept(self,primary.groupedSeq)
            self.file.write(")")
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
        self.file.write(specialSeq.value)
        pass
        # ARGS
        # self.definitions = definitions

    def visitTerminalString(self,terminalString):
        pass
        # ARGS
        # self.value = value

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        self.file.write(" "+terminalStringSQuote.value+" ")
        pass
        # ARGS
        # self.value = value

    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.file.write(" "+terminalStringDQuote.value+" ")
        pass
        # ARGS
        # self.value = value

    def visitIdentifier(self,identifier):
        self.file.write(" "+identifier.value+" ")
        pass
        # ARGS
        # self.value = value

    def visitEmpty(self,empty):
        pass

    def visitInteger(self,integer):
        self.file.write(" "+integer.value+" ")
        pass
        # ARGS
        # self.value = value
