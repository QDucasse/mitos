import sys
from MiniCppLexer import Lexer
from MiniCppParser import Parser

if __name__ == '__main__':
    testFileName = 'Programme.cpp'

    try:
      with open(testFileName, 'r') as testFile:
          testFileData = testFile.readlines()
    except FileNotFoundError:
      print('Error: test file {} does not exist'.format(testFileName))
      sys.exit()

    lexer = Lexer()
    tokens = lexer.lex(testFileData)
    print(tokens)
    verbose = True
    parser = Parser(verbose)
    parser.parse(tokens,True)


