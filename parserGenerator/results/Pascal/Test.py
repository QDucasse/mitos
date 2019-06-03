import sys
from PascalLexer_fromJinja import Lexer
from PascalParser_fromJinja import Parser

if __name__ == '__main__':
    testFileName = 'pascalTestProgram.pas'

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
    parser.parse(tokens)


