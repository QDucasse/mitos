from lexemDictionary import LexemDictionary
from visitor import Visitor

class SaveFile():
    def __init__(self,name):
        self.f=open(name,"w")
    
    def write(self,data):
        self.f.write(data)
     
    def close(self):
        self.f.close()

class PrettyPrinter(Visitor):
    def __init__(self,name="prettyprinter_input"):
        lexemDictionary = LexemDictionary()
        self.file=SaveFile(name)




    def visitSyntaxRule(self,syntaxRule):
        id   = syntaxRule.identifier
        defs = syntaxRule.definitions
        id.accept(self,id)
        self.file.write("=")
        defs.accept(self,defs)
        self.file.write(";\n")


    def visitDefinitions(self,definitions):
        # Visits all definitions
        for definition in definitions.definitions[0:-1]:
            definition.accept(self,definition)
            self.file.write("|")
        definitions.definitions[-1].accept(self,definitions.definitions[-1])


    def visitDefinition(self,definition):
        # Visits all terms
        for term in definition.terms[0:-1]:
            term.accept(self,term)
            self.file.write(",")
        definition.terms[-1].accept(self,definition.terms[-1])



    def visitException(self,exception):
        # Visits the exception
        self.file.write("-")
        super().visitException(exception)

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

    def visitSpecialSeq(self,specialSeq):
        self.file.write(specialSeq.value)


    def visitTerminalStringSQuote(self,terminalStringSQuote):
        self.file.write(" "+terminalStringSQuote.value+" ")


    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.file.write(" "+terminalStringDQuote.value+" ")


    def visitIdentifier(self,identifier):
        self.file.write(" "+identifier.value+" ")


    def visitInteger(self,integer):
        self.file.write(" "+integer.value+" ")

