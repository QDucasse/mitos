import sys
import argparse
from lexer import Lexer
from parser import Parser
from visitor import Visitor


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

    visitor = Visitor()
    visitor.visit(grammar)
    # print(grammar)

    # print("--------TEST AST PRINT---------")
    # print(grammar)
    # syntax = grammar.syntax
    # print(syntax)
    # syntaxRuleAlph = syntax.syntaxRules[5]
    # print(syntaxRuleAlph.identifier.value)
    # definitions = syntaxRuleAlph.definitions
    # print(definitions)
    # definitionList = definitions.definitions
    # print(definitionList)
    # definitionA = definitionList[0]
    # print(definitionA)
    # terms = definitionA.terms
    # print(terms)
    # termA = terms[0]
    # print("TERM: ",termA)
    # print("\tEXCEPTION: ",termA.exception)
    # factor = termA.factor
    # print("\tFACTOR: ",factor)
    # print("\t\tINTEGER: ",factor.integer)
    # primary = factor.primary
    # print("PRIMARY: ",primary)
    # print("\tOPTIONALSEQ: ",primary.optionalSeq)
    # print("\tREPEATEDSEQ: ",primary.repeatedSeq)
    # print("\tGROUPEDSEQ: ",primary.groupedSeq)
    # print("\t",primary.specialSeq)
    # print("\t",primary.terminalString)
    # print("\t",primary.identifier)
    # print("\t",primary.empty)
    # print(primary.identifier.value)
