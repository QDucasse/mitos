import re
import sys
import argparse
from lexer import Lexer
from parser import Parser
#from visitor import Visitor
from lexerWriterV2 import LexerWriter
from parserWriter import ParserWriter
from prettyprinter import PrettyPrinter

if __name__ == '__main__':
    testFileName = 'grammars/MiniJava_grammar.ebnf'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = Lexer()
    tokens = lexer.lex(testFileData)

    verbose = True
    parser = Parser(verbose)
    grammar = parser.parse(tokens)

    writer = LexerWriter("results/Java/MiniJavaLexer.py")
    writer.visit(grammar)
    writer.write(writer.lexemList)
    
    writerParser = ParserWriter(writer.lexemList,"results/Java/MiniJavaParser.py")
    writerParser.visit(grammar)

    pp = PrettyPrinter("results/Java/java_grammar_pp.ebnf")
    pp.visit(grammar)
