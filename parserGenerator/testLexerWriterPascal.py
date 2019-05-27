import re
import sys
import argparse
from lexer import Lexer
from parser import Parser
#from visitor import Visitor
from lexerWriter import LexerWriter
from prettyPrinter import PrettyPrinter

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

    writer = LexerWriter("results/lexerWriter/pascalLexer.py")
    writer.visit(grammar)
    print(writer.lexemList)
    writer.write(writer.lexemList)

    pp = PrettyPrinter("results/prettyPrinter/pascal_grammar_pp.ebnf")
    pp.visit(grammar)
