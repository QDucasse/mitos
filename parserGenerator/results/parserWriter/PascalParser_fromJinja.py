import sys
import copy
from ast    import *
from indent import Indent
from colors import Colors


class Parser:

    TERMINAL_STRING = [ 'SQUOTE','DQUOTE' ]

    def __init__(self, verbose=False):
        '''
        Parser constructor
        ---
        Args:    boolean verbose
        Returns: None
        '''
        self.indentator = Indent(verbose)
        self.tokens = []
        self.errors = 0

    def show_next(self, n=1):
        '''
        Returns the next token in the list while not poping it output
        ---
        Args   : int n (optional) the index of the targetted token
        Returns: token with index n from the tokens list
        '''
        try:
            return self.tokens[n - 1]
        except IndexError:
            print('ERROR: no more tokens left!')
            sys.exit(1)

    def expect(self, kind):
        '''
        Pops the next token from the tokens list and tests its type
        ---
        Args   : string kind, the wanted kind
        Returns: next token from the list
        '''
        actualToken = self.show_next()
        actualKind = actualToken.kind
        actualPosition = actualToken.position
        if actualKind == kind:
            return self.accept_it()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(actualPosition), kind, actualKind))
            sys.exit(1)

    # same as expect() but no error if not correct kind
    def maybe(self, kind):
        '''
        Pops the next token from the tokens list without raising error on its type
        ---
        Args   : string kind, the wanted kind
        Returns: next token from the list
        '''
        if self.show_next().kind == kind:
            return self.accept_it()

    def accept_it(self):
        '''

        '''
        token = self.show_next()
        output = Colors.FAIL + str(token.kind) + ' ' + token.value + Colors.ENDC
        self.indentator.say(output)
        return self.tokens.pop(0)

    def remove_comments(self):
        '''
        Removes the comments from the token list
        ---
        Args:    None
        Return : None
        '''
        result = []
        for token in self.tokens:
            if token.kind == 'COMMENT':
                pass
            else:
                result.append(token)
        return result
        

    def parseProgram(self):
        self.indentator.indent('Parsing Program')
        self.expect('PROGRAM')
        self.parseWhitespace()
        self.parseIdentifier()
        self.parseWhitespace()
        self.expect('BEGIN')
        self.parseWhitespace()
        while():
            self.parseAssignment()
            self.expect(";")
            self.parseWhitespace()
            
        self.expect('END.')
        self.indentator.dedent()


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        self.parseAlphabeticcharacter()
        while():
            self.parseAlphabeticcharacter()
            self.parseDigit()
            
        self.indentator.dedent()


    def parseNumber(self):
        self.indentator.indent('Parsing Number')
        if():
            self.expect("-")
            
        self.parseDigit()
        while():
            self.parseDigit()
            
        self.indentator.dedent()


    def parseString(self):
        self.indentator.indent('Parsing String')
        self.expect('"')
        while():
            self.parseAllcharacters()
            self.expect('"')
            
        self.expect('"')
        self.indentator.dedent()


    def parseAssignment(self):
        self.indentator.indent('Parsing Assignment')
        self.parseIdentifier()
        self.expect(":=")
        self.parseNumber()
        self.parseIdentifier()
        self.parseString()
        self.indentator.dedent()


    def parseAlphabeticcharacter(self):
        self.indentator.indent('Parsing Alphabeticcharacter')
        self.expect("A")
        self.expect("B")
        self.expect("C")
        self.expect("D")
        self.expect("E")
        self.expect("F")
        self.expect("G")
        self.expect("H")
        self.expect("I")
        self.expect("J")
        self.expect("K")
        self.expect("L")
        self.expect("M")
        self.expect("N")
        self.expect("O")
        self.expect("P")
        self.expect("Q")
        self.expect("R")
        self.expect("S")
        self.expect("T")
        self.expect("U")
        self.expect("V")
        self.expect("W")
        self.expect("X")
        self.expect("Y")
        self.expect("Z")
        self.indentator.dedent()


    def parseDigit(self):
        self.indentator.indent('Parsing Digit')
        self.expect("0")
        self.expect("1")
        self.expect("2")
        self.expect("3")
        self.expect("4")
        self.expect("5")
        self.expect("6")
        self.expect("7")
        self.expect("8")
        self.expect("9")
        self.indentator.dedent()


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        self.expect(" ")
        self.indentator.dedent()


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        self.expect("[a-zA-Z0-9 \W]")
        self.indentator.dedent()

