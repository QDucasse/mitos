import re
import sys
import argparse
from lexer import Lexer
from parser import Parser
#from visitor import Visitor
from lexerWriterV2 import LexerWriter
from prettyprinter import PrettyPrinter

if __name__ == '__main__':
    testFileName = 'grammars/pascal_grammar.ebnf'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = Lexer()
    tokens = lexer.lex(testFileData)

    verbose = False
    parser = Parser(verbose)
    grammar = parser.parse(tokens)

    writer = LexerWriter("results/lexerWriter/PascalLexer_fromJinja.py")
    writer.visit(grammar)
    writer.write(writer.lexemList)

    pp = PrettyPrinter("results/prettyPrinter/pascal_grammar_pp.ebnf")
    pp.visit(grammar)
