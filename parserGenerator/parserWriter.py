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
        self.expecting=[]

    def visitSyntaxRule(self,syntaxRule):
        # Visits identifier
        id   = syntaxRule.identifier
        # Visits all definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)
        self.template = self.env.get_template('method.py')
        self.output=self.template.render(name=id.value.capitalize(),expecting=self.expecting)
        self.saving_file.write(self.output)
        self.expecting=[]

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        self.expecting.append(terminalStringSQuote.value)
    
    
    def visitTerminalStringDQuote(self,terminalStringDQuote):
        self.visitTerminalStringSQuote(terminalStringDQuote)

