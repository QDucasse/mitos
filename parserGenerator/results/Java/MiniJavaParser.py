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

    def remove_comments_whitespace(self):
        '''
        Removes the comments and the whitespaces from the token list
        ---
        Args:    None
        Return : None
        '''
        result = []
        for token in self.tokens:
            if token.kind == 'COMMENT' or token.value==" ":
                pass
            else:
                result.append(token)
        return result
        

    def parseGoal(self):
        self.indentator.indent('Parsing Goal')
        self.parseMainclass()
        while(self.testClassdeclaration()):
            self.parseClassdeclaration()
            
        self.parseEof()
        self.indentator.dedent()


    def testGoal(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testMainclass())
        return(test)


    def parseMainclass(self):
        self.indentator.indent('Parsing Mainclass')
        self.expect("class")
        self.parseIdentifier()
        self.expect("{")
        self.expect("public")
        self.expect("static")
        self.expect("void")
        self.expect("main")
        self.expect("(")
        self.expect("String")
        self.expect("[")
        self.expect("]")
        self.parseIdentifier()
        self.expect(")")
        self.expect("{")
        self.parseStatement()
        self.expect("}")
        self.expect("}")
        self.indentator.dedent()


    def testMainclass(self):
        next=self.show_next().kind
        testing_list=['class']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseClassdeclaration(self):
        self.indentator.indent('Parsing Classdeclaration')
        self.expect("class")
        self.parseIdentifier()
        if(self.show_next().kind == "extends"):
            self.expect("extends")
            self.parseIdentifier()
            
        self.expect("{")
        while(self.testVardeclaration()):
            self.parseVardeclaration()
            
        while(self.testMethoddeclaration()):
            self.parseMethoddeclaration()
            
        self.expect("}")
        self.indentator.dedent()


    def testClassdeclaration(self):
        next=self.show_next().kind
        testing_list=['class']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseVardeclaration(self):
        self.indentator.indent('Parsing Vardeclaration')
        self.parseType()
        self.parseIdentifier()
        self.expect(";")
        self.indentator.dedent()


    def testVardeclaration(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testType())
        return(test)


    def parseMethoddeclaration(self):
        self.indentator.indent('Parsing Methoddeclaration')
        self.expect("public")
        self.parseType()
        self.parseIdentifier()
        self.expect("(")
        if(self.testType()):
            self.parseType()
            self.parseIdentifier()
            while(self.show_next().kind == ","):
                self.expect(",")
                self.parseType()
                self.parseIdentifier()
                
            
        self.expect(")")
        self.expect("{")
        while(self.testVardeclaration()):
            self.parseVardeclaration()
            
        while(self.testStatement()):
            self.parseStatement()
            
        self.expect("return")
        self.parseExpression()
        self.expect(";")
        self.expect("}")
        self.indentator.dedent()


    def testMethoddeclaration(self):
        next=self.show_next().kind
        testing_list=['public']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseType(self):
        self.indentator.indent('Parsing Type')
        if(self.show_next().kind == "int"):
            self.expect("int")
            if(self.show_next().kind == "["):
                self.expect("[")
                self.expect("]")
                
        elif(self.show_next().kind == "boolean"):
            self.expect("boolean")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            
        self.indentator.dedent()


    def testType(self):
        next=self.show_next().kind
        testing_list=['int', 'boolean']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
        return(test)


    def parseStatement(self):
        self.indentator.indent('Parsing Statement')
        if(self.show_next().kind == "{"):
            self.expect("{")
            while(self.testStatement()):
                self.parseStatement()
                
            self.expect("}")
        elif(self.show_next().kind == "if"):
            self.expect("if")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.parseStatement()
            self.expect("else")
            self.parseStatement()
        elif(self.show_next().kind == "while"):
            self.expect("while")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.parseStatement()
        elif(self.show_next().kind == "System.out.println"):
            self.expect("System.out.println")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.expect(";")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            self.expect("=")
            self.parseExpression()
            self.expect(";")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            self.expect("[")
            self.parseExpression()
            self.expect("]")
            self.expect("=")
            self.parseExpression()
            self.expect(";")
            
        self.indentator.dedent()


    def testStatement(self):
        next=self.show_next().kind
        testing_list=['{', 'if', 'while', 'System.out.println']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
        test=(test or self.testIdentifier())
        return(test)


    def parseExpression(self):
        self.indentator.indent('Parsing Expression')
        if(self.testExpression1()):
            self.parseExpression1()
        elif(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testSpecial()):
            self.parseSpecial()
        elif(self.show_next().kind == "!"):
            self.expect("!")
            self.parseExpression()
        elif(self.show_next().kind == "("):
            self.expect("(")
            self.parseExpression()
            self.expect(")")
        elif(self.testExpression2()):
            self.parseExpression2()
        elif(self.testExpression3()):
            self.parseExpression3()
        elif(self.testExpression4()):
            self.parseExpression4()
            
        self.indentator.dedent()


    def testExpression(self):
        next=self.show_next().kind
        testing_list=['!', '(']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression1())
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testSpecial())
        test=(test or self.testExpression2())
        test=(test or self.testExpression3())
        test=(test or self.testExpression4())
        return(test)


    def parseExpression1(self):
        self.indentator.indent('Parsing Expression1')
        if(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
            
        if(self.show_next().kind == "&&" or self.show_next().kind == "<" or self.show_next().kind == "+" or self.show_next().kind == "-" or self.show_next().kind == "*"):
            if(self.show_next().kind == "&&"):
                self.expect("&&")
            elif(self.show_next().kind == "<"):
                self.expect("<")
            elif(self.show_next().kind == "+"):
                self.expect("+")
            elif(self.show_next().kind == "-"):
                self.expect("-")
            elif(self.show_next().kind == "*"):
                self.expect("*")
                
            
        if(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testBool()):
            self.parseBool()
        elif(self.testSpecial()):
            self.parseSpecial()
        elif(self.testExpression5()):
            self.parseExpression5()
            
        self.indentator.dedent()


    def testExpression1(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testBool())
        test=(test or self.testSpecial())
        test=(test or self.testExpression5())
        return(test)


    def parseExpression2(self):
        self.indentator.indent('Parsing Expression2')
        self.parseExpression()
        self.expect("[")
        self.parseExpression()
        self.expect("]")
        self.indentator.dedent()


    def testExpression2(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression3(self):
        self.indentator.indent('Parsing Expression3')
        self.parseExpression()
        self.expect(".")
        self.expect("length")
        self.indentator.dedent()


    def testExpression3(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression4(self):
        self.indentator.indent('Parsing Expression4')
        self.parseExpression()
        if(self.show_next().kind == "("):
            self.expect("(")
            if(self.testExpression1()):
                self.parseExpression1()
                
            self.expect(")")
            
        self.expect(".")
        self.parseIdentifier()
        self.expect("(")
        if(self.testExpression()):
            self.parseExpression()
            while(self.show_next().kind == ","):
                self.expect(",")
                self.parseExpression()
                
            
        self.expect(")")
        self.indentator.dedent()


    def testExpression4(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression5(self):
        self.indentator.indent('Parsing Expression5')
        self.expect("new")
        if(self.show_next().kind == "int"):
            self.expect("int")
            self.expect("[")
            self.parseExpression()
            self.expect("]")
        elif(self.testExpression4()):
            self.parseExpression4()
            
        self.indentator.dedent()


    def testExpression5(self):
        next=self.show_next().kind
        testing_list=['new']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseExpression6(self):
        self.indentator.indent('Parsing Expression6')
        self.parseExpression()
        self.parseExpression7()
        self.indentator.dedent()


    def testExpression6(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression7(self):
        self.indentator.indent('Parsing Expression7')
        if(self.show_next().kind == "("):
            self.expect("(")
            if(self.testExpression()):
                self.parseExpression()
                
            self.expect(")")
            
        self.indentator.dedent()


    def testExpression7(self):
        next=self.show_next().kind
        testing_list=['(']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseBool(self):
        self.indentator.indent('Parsing Bool')
        if(self.show_next().kind == "true"):
            self.expect("true")
        elif(self.show_next().kind == "false"):
            self.expect("false")
            
        self.indentator.dedent()


    def testBool(self):
        next=self.show_next().kind
        testing_list=['true', 'false']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecial(self):
        self.indentator.indent('Parsing Special')
        self.expect("this")
        if(self.show_next().kind == "."):
            self.expect(".")
            
        if(self.testExpression6()):
            self.parseExpression6()
            
        self.indentator.dedent()


    def testSpecial(self):
        next=self.show_next().kind
        testing_list=['this']
        test=(next in testing_list)
        if (test): return(test)
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
        elif(self.show_next().kind == "a"):
            self.expect("a")
        elif(self.show_next().kind == "b"):
            self.expect("b")
        elif(self.show_next().kind == "c"):
            self.expect("c")
        elif(self.show_next().kind == "d"):
            self.expect("d")
        elif(self.show_next().kind == "e"):
            self.expect("e")
        elif(self.show_next().kind == "f"):
            self.expect("f")
        elif(self.show_next().kind == "g"):
            self.expect("g")
        elif(self.show_next().kind == "h"):
            self.expect("h")
        elif(self.show_next().kind == "i"):
            self.expect("i")
        elif(self.show_next().kind == "j"):
            self.expect("j")
        elif(self.show_next().kind == "k"):
            self.expect("k")
        elif(self.show_next().kind == "l"):
            self.expect("l")
        elif(self.show_next().kind == "m"):
            self.expect("m")
        elif(self.show_next().kind == "n"):
            self.expect("n")
        elif(self.show_next().kind == "o"):
            self.expect("o")
        elif(self.show_next().kind == "p"):
            self.expect("p")
        elif(self.show_next().kind == "q"):
            self.expect("q")
        elif(self.show_next().kind == "r"):
            self.expect("r")
        elif(self.show_next().kind == "s"):
            self.expect("s")
        elif(self.show_next().kind == "t"):
            self.expect("t")
        elif(self.show_next().kind == "u"):
            self.expect("u")
        elif(self.show_next().kind == "v"):
            self.expect("v")
        elif(self.show_next().kind == "w"):
            self.expect("w")
        elif(self.show_next().kind == "x"):
            self.expect("x")
        elif(self.show_next().kind == "y"):
            self.expect("y")
        elif(self.show_next().kind == "z"):
            self.expect("z")
            
        self.indentator.dedent()


    def testAlphabeticcharacter(self):
        next=self.show_next().kind
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecialcharacter(self):
        self.indentator.indent('Parsing Specialcharacter')
        self.expect("_")
        self.indentator.dedent()


    def testSpecialcharacter(self):
        next=self.show_next().kind
        testing_list=['_']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        self.expect(" ")
        while(self.testWhitespace()):
            self.parseWhitespace()
            
        self.indentator.dedent()


    def testWhitespace(self):
        next=self.show_next().kind
        testing_list=[' ']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        if(self.testAllcharacters()):
            self.parseAllcharacters()
        elif(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testWhitespace()):
            self.parseWhitespace()
        elif(self.testSpecialcharacter()):
            self.parseSpecialcharacter()
            
        while(self.testAllcharacters() or self.testIntegerliteral() or self.testWhitespace() or self.testSpecialcharacter()):
            if(self.testAllcharacters()):
                self.parseAllcharacters()
            elif(self.testIntegerliteral()):
                self.parseIntegerliteral()
            elif(self.testWhitespace()):
                self.parseWhitespace()
            elif(self.testSpecialcharacter()):
                self.parseSpecialcharacter()
                
            
        self.indentator.dedent()


    def testIdentifier(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testAllcharacters())
        test=(test or self.testIntegerliteral())
        test=(test or self.testWhitespace())
        test=(test or self.testSpecialcharacter())
        return(test)


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        self.parseAlphabeticcharacter()
        self.indentator.dedent()


    def testAllcharacters(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testAlphabeticcharacter())
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
        if (test): return(test)
        return(test)


    def parseIntegerliteral(self):
        self.indentator.indent('Parsing Integerliteral')
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
        self.indentator.dedent()


    def testIntegerliteral(self):
        next=self.show_next().kind
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDigit())
        return(test)


    def parseEof(self):
        self.indentator.indent('Parsing Eof')
        self.expect(".")
        self.indentator.dedent()


    def testEof(self):
        next=self.show_next().kind
        testing_list=['.']
        test=(next in testing_list)
        if (test): return(test)
        return(test)

    def parse(self, tokens, remove_comments_whitespace=False):
        '''
        Main function: launches the parsing operation
        ---
        Args:
        Returns
        '''
        self.tokens = tokens
        #print(self.tokens)
        if remove_comments_whitespace:
            self.tokens = self.remove_comments_whitespace()
        else:
            self.tokens = self.remove_comments()
        self.parseGoal()