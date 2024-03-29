# -*- coding: utf-8 -*-
"""
Compiler of the project, organizes the passes
@author: Quentin Ducasse
"""


from mitos.lexer import Lexer
from mitos.parser import Parser
from mitos.prettyprinter import PrettyPrinter
from mitos.visitor import Visitor


class Compiler:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser(verbose=True)
        self.pretty_printer = PrettyPrinter()
        self.visitor = Visitor()

    def compile(self, source_file):
        lexems = self.lexer.lex(source_file)
        ast = self.parser.parse(lexems)
        self.pretty_printer.pretty_print(ast)
        self.visitor.visit(ast)
        return ast
