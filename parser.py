import sys
from indent import Indent
from colors import Colors


class Parser:

    TERMINAL_STRING = [ 'SQUOTE','FQUOTE' ]

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
        self.parseGrammar()

    def parseGrammar(self):
        '''
        Root of the program, beginning of the parsing
        '''
        self.indentator.indent('Parsing Grammar')
        self.parseSyntax()
        self.indentator.dedent()
        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

    def parseSyntax(self):
        '''
        Parses a syntax:
        Syntax = SyntaxRule, {SyntaxRule};
        '''
        self.indentator.indent('Parsing Syntax')
        while (len(self.tokens)>0):
            self.parseSyntaxRule()
        self.indentator.dedent()

    def parseSyntaxRule(self):
        '''
        Parses a syntax rule:
        SyntaxRule = Identifier, '=', Definitions, ';';  //EBNF
        '''
        self.indentator.indent('Parsing Syntax Rule')
        self.parseIdentifier()
        self.expect('ASSIGN')
        self.parseDefinitions()
        self.expect('TERMINATOR')
        self.indentator.dedent()

    def parseDefinitions(self):
        '''
        Parses definitions:
        Definitions = Definition, {'|', Definition};  //EBNF
        '''
        self.indentator.indent('Parsing Definitions')
        self.parseDefinition()
        while(self.show_next().kind == 'SEPARATOR'):
            self.expect('SEPARATOR')
            self.parseDefinition()
        self.indentator.dedent()

    def parseDefinition(self):
        '''
        Parses a definition:
        Definition = Term, {',', Term};  //EBNF
        '''
        self.indentator.indent('Parsing Definition')
        self.parseTerm()
        while(self.show_next().kind == 'CONCATENATION'):
            self.expect('CONCATENATION')
            self.parseTerm()
        self.indentator.dedent()

    def parseTerm(self):
        '''
        Parses a term:
        Term = Factor, ['-', Exception];  //EBNF
        '''
        self.indentator.indent('Parsing Term')
        self.parseFactor()
        if self.show_next().kind == 'EXCEPT':
            self.expect('EXCEPT')
            self.parseException()
        self.indentator.dedent()

    def parseException(self):
        '''
        Parses an Exception:
        Exception = Factor;  //EBNF
        '''
        self.indentator.indent('Parsing Exception')
        self.parseFactor()
        self.indentator.dedent()

    def parseFactor(self):
        '''
        Parses a factor:
        Factor = [Integer, '*'], Primary; //EBNF
        '''
        self.indentator.indent('Parsing Factor')
        if self.show_next().kind == 'DIGIT':
            self.parseInteger()
            self.expect('REPETITION')
        self.parsePrimary()
        self.indentator.dedent()

    def parsePrimary(self):
        '''
        Parses a primary:
        Primary = OptionalSeq
                | RepeatedSeq
                | GroupedSeq
                | SpecialSeq
                | TerminalString
                | Identifier
                | Empty;            //EBNF
        '''
        self.indentator.indent('Parsing Primary')
        if self.show_next().kind   == 'LBRACKET':
            self.parseOptionalSeq()
        elif self.show_next().kind == 'LBRACE':
            self.parseRepeatedSeq()
        elif self.show_next().kind == 'LPAREN':
            self.parseGroupedSeq()
        elif self.show_next().kind == 'SPECIAL':
            self.parseSpecial()
        elif self.show_next().kind in Parser.TERMINAL_STRING:
            self.parseTerminalString()
        elif self.show_next().kind == 'IDENTIFIER':
            self.parseIdentifier()
        else:
            self.parseEmpty()
        self.indentator.dedent()

    def parseOptionalSeq(self):
        '''
        Parses an optional sequence:
        OptionalSeq = '[', Definitions, ']';  //EBNF
        '''
        self.indentator.indent('Parsing Optional Sequence')
        self.expect('LBRACKET')
        self.parseDefinitions()
        self.expect('RBRACKET')
        self.indentator.dedent()

    def parseRepeatedSeq(self):
        '''
        Parses a repeated sequence:
        RepeatedSeq = '{', Definitions, '}';  //EBNF
        '''
        self.indentator.indent('Parsing Repeated Sequence')
        self.expect('LBRACE')
        self.parseDefinitions()
        self.expect('RBRACE')
        self.indentator.dedent()

    def parseGroupedSeq(self):
        '''
        Parses a grouped sequence:
        GroupedSeq = '(', Definitions, ')';  //EBNF
        '''
        self.indentator.indent('Parsing Grouped Sequence')
        self.expect('LPAREN')
        self.parseDefinitions()
        self.expect('RPAREN')
        self.indentator.dedent()

    def parseSpecialSeq(self):
        '''
        Parses a special sequence:
        SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
        '''
        self.indentator.indent('Parsing Special Sequence')
        self.expect('SPECIAL')
        self.indentator.dedent()

    def parseTerminalString(self):
        '''
        Parses a terminal string:
        TerminalString = "'", Character - "'", {Character - "'"}, "'"
                       | '"', Character - '"', {Character - '"'}, '"';  //EBNF
        '''
        self.indentator.indent('Parsing Terminal String')
        if self.show_next().kind == 'FQUOTE':
            self.expect('FQUOTE')
        elif self.show_next().kind == 'SQUOTE':
            self.expect('SQUOTE')
        self.indentator.dedent()

    def parseIdentifier(self):
        '''
        Parses an identifier:    (already done in the lexer)
        Identifier = Letter, {Letter | Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Identifier')
        self.expect('IDENTIFIER')
        self.indentator.dedent()

    def parseEmpty(self):
        '''
        Parses an empty primary:
        Empty = ;  //EBNF
        '''
        self.indentator.indent('Parsing Empty')
        self.indentator.dedent()

    def parseInteger(self):
        '''
        Parses an integer:   (already done in the lexer)
        Integer = Digit, {Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Integer')
        self.expect('INTEGER')
        self.indentator.dedent()
