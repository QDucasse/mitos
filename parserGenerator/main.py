import sys
import argparse
from lexer import Lexer
from parser import Parser


if __name__ == '__main__':

    # adding test file name as command line argument
    argParser = argparse.ArgumentParser()
    argParser.add_argument('testFileName')
    args = argParser.parse_args()

    # testFileName = 'test/pascal_grammar.ebnf'
    testFileName = args.testFileName
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
    # print("--------TEST AST PRINT---------")
    # print(grammar)
    # syntax = grammar.syntax
    # print(syntax)
    # syntaxRuleAlph = syntax.syntaxRules[5]
    # print(syntaxRuleAlph)
    # print(syntaxRuleAlph.identifier)
    # definitions = syntaxRuleAlph.definitions
    # print(definitions)
    # definitionA = definitions.definitions[0]
    # print(definitionA)
    # terms = definitionA.terms
    # print(terms)
    # termA = terms[0]
    # print("TERM: ",termA)
    # print("\t",termA.exception)
    # factor = termA.factor
    # print("FACTOR: ",factor)
    # print("\t",factor.integer)
    # primary = factor.primary
    # print("PRIMARY: ",primary)
    # print("\t",primary.optionalSeq)
    # print("\t",primary.repeatedSeq)
    # print("\t",primary.groupedSeq)
    # print("\t",primary.specialSeq)
    # print("\t",primary.terminalString)
    # print("\t",primary.identifier)
    # print("\t",primary.empty)
