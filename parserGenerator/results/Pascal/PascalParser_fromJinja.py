import sys
import copy
from ast    import *
from indent import Indent
from colors import Colors


class Parser:


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
        output = Colors.FAIL + token.value + Colors.ENDC
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
        while(self.testAssignment()):
            self.parseAssignment()
            self.expect(";")
            self.parseWhitespace()
            
            
        self.expect('END.')
        
        self.indentator.dedent()


    def testProgram(self):
        next=self.show_next().kind
        testing_list=['PROGRAM']
        test=(next in testing_list)
        return(test)


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        self.parseAlphabeticcharacter()
        while(self.testAlphabeticcharacter() or self.testDigit()):
            if(self.testAlphabeticcharacter()):
                self.parseAlphabeticcharacter()
            elif(self.testDigit()):
                self.parseDigit()
            
            
        
        self.indentator.dedent()


    def testIdentifier(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        test=(test or self.testAlphabeticcharacter())
        return(test)


    def parseNumber(self):
        self.indentator.indent('Parsing Number')
        if(self.show_next().kind == "-"):
            self.expect("-")
            
            
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
            
        
        self.indentator.dedent()


    def testNumber(self):
        next=self.show_next().kind
        testing_list=['-']
        test=(next in testing_list)
        test=(test or self.testDigit())
        return(test)


    def parseString(self):
        self.indentator.indent('Parsing String')
        self.expect('"')
        while(self.testAllcharacters()):
            self.parseAllcharacters()
            
            
        self.expect('"')
        
        self.indentator.dedent()


    def testString(self):
        next=self.show_next().kind
        testing_list=['"']
        test=(next in testing_list)
        return(test)


    def parseAssignment(self):
        self.indentator.indent('Parsing Assignment')
        self.parseIdentifier()
        self.expect(":=")
        if(self.testNumber()):
            self.parseNumber()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testString()):
            self.parseString()
        
        
        self.indentator.dedent()


    def testAssignment(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        test=(test or self.testIdentifier())
        return(test)


    def parseAlphabeticcharacter(self):
        self.indentator.indent('Parsing Alphabeticcharacter')
        if(self.show_next().kind == "A"):
            self.expect("A")
        elif(self.show_next().kind == "B"):
            self.expect("B")
        elif(self.show_next().kind == "C"):
            self.expect("C")
        elif(self.show_next().kind == "D"):
            self.expect("D")
        elif(self.show_next().kind == "E"):
            self.expect("E")
        elif(self.show_next().kind == "F"):
            self.expect("F")
        elif(self.show_next().kind == "G"):
            self.expect("G")
        elif(self.show_next().kind == "H"):
            self.expect("H")
        elif(self.show_next().kind == "I"):
            self.expect("I")
        elif(self.show_next().kind == "J"):
            self.expect("J")
        elif(self.show_next().kind == "K"):
            self.expect("K")
        elif(self.show_next().kind == "L"):
            self.expect("L")
        elif(self.show_next().kind == "M"):
            self.expect("M")
        elif(self.show_next().kind == "N"):
            self.expect("N")
        elif(self.show_next().kind == "O"):
            self.expect("O")
        elif(self.show_next().kind == "P"):
            self.expect("P")
        elif(self.show_next().kind == "Q"):
            self.expect("Q")
        elif(self.show_next().kind == "R"):
            self.expect("R")
        elif(self.show_next().kind == "S"):
            self.expect("S")
        elif(self.show_next().kind == "T"):
            self.expect("T")
        elif(self.show_next().kind == "U"):
            self.expect("U")
        elif(self.show_next().kind == "V"):
            self.expect("V")
        elif(self.show_next().kind == "W"):
            self.expect("W")
        elif(self.show_next().kind == "X"):
            self.expect("X")
        elif(self.show_next().kind == "Y"):
            self.expect("Y")
        elif(self.show_next().kind == "Z"):
            self.expect("Z")
        
        self.indentator.dedent()


    def testAlphabeticcharacter(self):
        next=self.show_next().kind
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        test=(next in testing_list)
        return(test)


    def parseDigit(self):
        self.indentator.indent('Parsing Digit')
        if(self.show_next().kind == "0"):
            self.expect("0")
        elif(self.show_next().kind == "1"):
            self.expect("1")
        elif(self.show_next().kind == "2"):
            self.expect("2")
        elif(self.show_next().kind == "3"):
            self.expect("3")
        elif(self.show_next().kind == "4"):
            self.expect("4")
        elif(self.show_next().kind == "5"):
            self.expect("5")
        elif(self.show_next().kind == "6"):
            self.expect("6")
        elif(self.show_next().kind == "7"):
            self.expect("7")
        elif(self.show_next().kind == "8"):
            self.expect("8")
        elif(self.show_next().kind == "9"):
            self.expect("9")
        
        self.indentator.dedent()


    def testDigit(self):
        next=self.show_next().kind
        testing_list=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        test=(next in testing_list)
        return(test)


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        while(self.show_next().kind == " "):
            self.expect(" ")
            self.parseWhitespace()
            
            
        
        self.indentator.dedent()


    def testWhitespace(self):
        next=self.show_next().kind
        testing_list=[' ']
        test=(next in testing_list)
        return(test)


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        if(self.show_next().kind == "[a-zA-Z0-9 \W]"):
            self.expect("[a-zA-Z0-9 \W]")
        elif(self.testAlphabeticcharacter()):
            self.parseAlphabeticcharacter()
        elif(self.testWhitespace()):
            self.parseWhitespace()
        
        self.indentator.dedent()


    def testAllcharacters(self):
        next=self.show_next().kind
        testing_list=['[a-zA-Z0-9 \\W]']
        test=(next in testing_list)
        test=(test or self.testAlphabeticcharacter())
        test=(test or self.testWhitespace())
        return(test)

    def parse(self, tokens):
        '''
        Main function: launches the parsing operation
        ---
        Args:
        Returns
        '''
        self.tokens = tokens
        #print(self.tokens)
        self.tokens = self.remove_comments()
        self.parseProgram()