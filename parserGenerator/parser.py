import sys
from ast    import *
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
        grammar = self.parseGrammar()
        return grammar

    def parseGrammar(self):
        '''
        Root of the program, beginning of the parsing
        '''
        self.indentator.indent('Parsing Grammar')
        grammar = Grammar()
        syntax  = self.parseSyntax()
        grammar.syntax = syntax
        self.indentator.dedent()
        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')
        return grammar

    def parseSyntax(self):
        '''
        Parses a syntax:
        Syntax = SyntaxRule, {SyntaxRule};
        '''
        self.indentator.indent('Parsing Syntax')
        syntax = Syntax()
        while (len(self.tokens)>0):
            syntaxRule = self.parseSyntaxRule()
            syntax.addRule(syntaxRule)
        self.indentator.dedent()
        return syntax

    def parseSyntaxRule(self):
        '''
        Parses a syntax rule:
        SyntaxRule = Identifier, '=', Definitions, ';';  //EBNF
        '''
        self.indentator.indent('Parsing Syntax Rule')
        syntaxRule = SyntaxRule()
        identifier  = self.parseIdentifier()
        syntaxRule.identifier = identifier
        self.expect('ASSIGN')
        definitions = self.parseDefinitions()
        syntaxRule.definitions = definitions
        self.expect('TERMINATOR')
        self.indentator.dedent()
        return syntaxRule

    def parseDefinitions(self):
        '''
        Parses definitions:
        Definitions = Definition, {'|', Definition};  //EBNF
        '''
        self.indentator.indent('Parsing Definitions')
        definitions = Definitions()
        self.parseDefinition()
        while(self.show_next().kind == 'SEPARATOR'):
            self.expect('SEPARATOR')
            definition = self.parseDefinition()
            definitions.addDefinition(definition)
        self.indentator.dedent()
        return definitions

    def parseDefinition(self):
        '''
        Parses a definition:
        Definition = Term, {',', Term};  //EBNF
        '''
        self.indentator.indent('Parsing Definition')
        definition = Definition()
        mainTerm = self.parseTerm()
        definition.addTerm(mainTerm)
        while(self.show_next().kind == 'CONCATENATION'):
            self.expect('CONCATENATION')
            otherTerm=self.parseTerm()
            definition.addTerm(otherTerm)
        self.indentator.dedent()
        return definition

    def parseTerm(self):
        '''
        Parses a term:
        Term = Factor, ['-', Exception];  //EBNF
        '''
        self.indentator.indent('Parsing Term')
        term = Term()
        factor    = self.parseFactor()
        term.factor = factor
        exception = None
        if self.show_next().kind == 'EXCEPT':
            self.expect('EXCEPT')
            exception = self.parseException()
            term.exception = exception
        self.indentator.dedent()
        return term

    def parseException(self):
        '''
        Parses an Exception:
        Exception = Factor;  //EBNF
        '''
        self.indentator.indent('Parsing Exception')
        exception = Exception()
        factor = self.parseFactor()
        exception.factor = factor
        self.indentator.dedent()
        return exception

    def parseFactor(self):
        '''
        Parses a factor:
        Factor = [Integer, '*'], Primary; //EBNF
        '''
        self.indentator.indent('Parsing Factor')
        factor = Factor()
        integer = 0
        factor.integer = integer
        if self.show_next().kind == 'DIGIT':
            integer = self.parseInteger()
            factor.integer = integer
            self.expect('REPETITION')
        primary = self.parsePrimary()
        factor.primary = primary
        self.indentator.dedent()
        return factor

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
        primary = Primary()
        if self.show_next().kind   == 'LBRACKET':
            optionalSeq = self.parseOptionalSeq()
            primary.optionalSeq = optionalSeq
        elif self.show_next().kind == 'LBRACE':
            repeatedSeq = self.parseRepeatedSeq()
            primary.repeatedSeq = repeatedSeq
        elif self.show_next().kind == 'LPAREN':
            groupedSeq = self.parseGroupedSeq()
            primary.groupedSeq = groupedSeq
        elif self.show_next().kind == 'SPECIAL':
            specialSeq = self.parseSpecialSeq()
            primary.specialSeq = specialSeq
        elif self.show_next().kind in Parser.TERMINAL_STRING:
            terminalString = self.parseTerminalString()
            primary.terminalString = terminalString
        elif self.show_next().kind == 'IDENTIFIER':
            identifier = self.parseIdentifier()
            primary.identifier = identifier
        else:
            empty = self.parseEmpty()
            primary.empty = empty
        self.indentator.dedent()
        return primary

    def parseOptionalSeq(self):
        '''
        Parses an optional sequence:
        OptionalSeq = '[', Definitions, ']';  //EBNF
        '''
        self.indentator.indent('Parsing Optional Sequence')
        optionalSeq = OptionalSeq()
        self.expect('LBRACKET')
        definitions = self.parseDefinitions()
        optionalSeq.definitions = definitions
        self.expect('RBRACKET')
        self.indentator.dedent()
        return optionalSeq

    def parseRepeatedSeq(self):
        '''
        Parses a repeated sequence:
        RepeatedSeq = '{', Definitions, '}';  //EBNF
        '''
        self.indentator.indent('Parsing Repeated Sequence')
        repeatedSeq = RepeatedSeq()
        self.expect('LBRACE')
        definitions = self.parseDefinitions()
        repeatedSeq.definitions = definitions
        self.expect('RBRACE')
        self.indentator.dedent()
        return repeatedSeq

    def parseGroupedSeq(self):
        '''
        Parses a grouped sequence:
        GroupedSeq = '(', Definitions, ')';  //EBNF
        '''
        self.indentator.indent('Parsing Grouped Sequence')
        groupedSeq = GroupedSeq()
        self.expect('LPAREN')
        definitions = self.parseDefinitions()
        groupedSeq.definitions = definitions
        self.expect('RPAREN')
        self.indentator.dedent()
        return groupedSeq

    def parseSpecialSeq(self):
        '''
        Parses a special sequence:
        SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
        '''
        self.indentator.indent('Parsing Special Sequence')
        specialSeq = SpecialSeq()
        token = self.expect('SPECIAL')
        value = token.value
        specialSeq.value = value
        self.indentator.dedent()
        return specialSeq

    def parseTerminalString(self):
        '''
        Parses a terminal string:
        TerminalString = "'", Character - "'", {Character - "'"}, "'"
                       | '"', Character - '"', {Character - '"'}, '"';  //EBNF
        '''
        self.indentator.indent('Parsing Terminal String')
        terminalString = TerminalStringFQuote()
        if self.show_next().kind == 'FQUOTE':
            token = self.expect('FQUOTE')
            value = token.value
            terminalString.value = value
        elif self.show_next().kind == 'SQUOTE':
            token = self.expect('SQUOTE')
            value = token.value
            terminalString.value = value
        self.indentator.dedent()
        return terminalString

    def parseIdentifier(self):
        '''
        Parses an identifier:    (already done in the lexer)
        Identifier = Letter, {Letter | Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Identifier')
        identifier = Identifier()
        token = self.expect('IDENTIFIER')
        value = token.value
        identifier.value = value
        self.indentator.dedent()
        return identifier

    def parseEmpty(self):
        '''
        Parses an empty primary:
        Empty = ;  //EBNF
        '''
        self.indentator.indent('Parsing Empty')
        empty = Empty()
        self.indentator.dedent()
        return empty

    def parseInteger(self):
        '''
        Parses an integer:   (already done in the lexer)
        Integer = Digit, {Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Integer')
        integer = Integer()
        token = self.expect('INTEGER')
        value = token.value
        integer.value = value
        self.indentator.dedent()
        return integer
