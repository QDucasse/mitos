import re
from visitor import Visitor
from lexemDictionary import LexemDictionary
from jinja2 import Environment, FileSystemLoader

class ParserWriter(Visitor):
    def __init__(self,lexer,name="results/parserWriter/parserWriter_output.py"):
        self.lexer=lexer
        self.saving_file=open(name,"w")
        file_loader = FileSystemLoader('templates/parser')#On se place dans le bon dossier 
        self.env = Environment(loader=file_loader)
        self.template = self.env.get_template('body.py')#On ouvre le template
        self.output = self.template.render()#On remplace les champs du template
        self.saving_file.write(self.output)
        self.to_generate=[]

    def visitSyntaxRule(self,syntaxRule):
        # Visits identifier
        id   = syntaxRule.identifier
        # Visits all definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)
        self.template = self.env.get_template('method.py')
        self.output=self.template.render(name=id.value.capitalize(),generator=self.to_generate[1::])
        self.saving_file.write(self.output)
        self.to_generate=[]

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        self.to_generate.append((terminalStringSQuote.value,1))#1=Expected , 0=For Parsing
    
    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.visitTerminalStringSQuote(terminalStringDQuote)
        
    def visitPrimary(self,primary):
        if primary.optionalSeq != None:
            self.to_generate.append("opt-begin")
            primary.optionalSeq.accept(self,primary.optionalSeq)
            self.to_generate.append("opt-end")
        elif primary.identifier != None:
            primary.identifier.accept(self,primary.identifier)
        elif primary.repeatedSeq != None:
            self.to_generate.append("rep-begin")
            primary.repeatedSeq.accept(self,primary.repeatedSeq)
            self.to_generate.append("rep-end")
        elif primary.groupedSeq != None:
            #self.to_generate.append("grp-begin")
            primary.groupedSeq.accept(self,primary.groupedSeq)
            #self.to_generate.append("grp-end")
        elif primary.specialSeq != None:
            #self.to_generate.append("spe-begin")
            primary.specialSeq.accept(self,primary.specialSeq)
            #self.to_generate.append("spe-end")
        elif primary.terminalString != None:
            primary.terminalString.accept(self,primary.terminalString)
        elif primary.empty != None:
            primary.empty.accept(self,primary.empty)
            
    def visitIdentifier(self,identifier):
        self.to_generate.append((identifier.value.capitalize(),0))


