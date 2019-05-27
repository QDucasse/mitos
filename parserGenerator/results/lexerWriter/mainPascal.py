import re
import sys
import argparse
from pascalLexer import LexerTemplate

if __name__ == '__main__':
    testFileName = 'results/lexerWriter/pascalTestProgram.pas'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = LexerTemplate()
    tokens = lexer.lex(testFileData)
    print(tokens)
    # verbose = False
    # parser = Parser(verbose)
    # grammar = parser.parse(tokens)
