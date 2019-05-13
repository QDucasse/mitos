import sys
import argparse
from lexer import Lexer
from parser import Parser


if __name__ == '__main__':
    testFileName = 'test/pascal_grammar.ebnf'

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
    print(grammar)
