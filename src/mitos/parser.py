# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import sys

from mitos.ast   import *
from mitos.utils import Indentator, Colors, loginfo


class Parser:
    """
    EBNF main parser class of the system.

    verbose: boolean - Run the parser in verbose mode to obtain outputs in the terminal.

    Note: The comments display extracts of the EBNF's EBNF grammar and those lines are followed by "//EBNF".
    You can refer to the full grammar in grammars/ebnf.ebnf
    """
    TERMINAL_STRING = [ 'SQUOTE','DQUOTE' ]
    INDENTATOR = Indentator()

    def __init__(self, verbose=True):
        self.lexems = []
        Parser.INDENTATOR.verbose = verbose

    def peek(self, n=1):
        """Return the next (or nth) token WITHOUT popping it from the lexems list"""
        try:
            return self.lexems[n-1]
        except IndexError:
            print('ERROR: no more lexems left!')
            sys.exit(1)

    def peek_next(self):
        """Peek next token without returning it"""
        return self.peek(1)

    def consume(self):
        """Pop the lexem out of the lexems list and return it"""
        return self.lexems.pop(0)

    def expect(self, tag):
        """Pop the next lexem and verify its tag"""
        lexem = self.peek()
        if lexem.tag == tag:
            return self.consume()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(lexem.position), tag, lexem.tag))
            sys.exit(1)

    def remove_comments(self):
        """Removes the comments from the token list by testing their tags."""
        self.lexems = [lexem for lexem in self.lexems if lexem.tag!="COMMENT"]

    # ======================== #
    #     PARSING FUNCTIONS    #
    # ======================== #

    def parse(self, lexems):
        """Main function: launches the parsing operation."""
        self.lexems = lexems
        self.remove_comments()
        grammar_node = self.parse_grammar()
        return grammar_node

    @loginfo(INDENTATOR)
    def parse_grammar(self):
        """grammar = { rule } ;"""
        # self.indentator.indent('Parsing Grammar...')
        grammar_node = GrammarNode()
        while (len(self.lexems)>0):
            rule_node = self.parse_rule()
            grammar_node.rules.append(rule_node)
        # self.indentator.dedent()
        return grammar_node

    @loginfo(INDENTATOR)
    def parse_rule(self):
        """rule  = identifier, '=', definition, {'|', definition} ';';"""
        # self.indentator.indent('Parsing Syntax...')
        # self.indentator.say(Colors.OKGREEN + 'New Syntax' +  Colors.ENDC)
        rule_node = RuleNode()
        rule_node.identifier = self.expect("IDENTIFIER")
        self.expect("ASSIGN")
        rule_node.definitions.append(self.parse_definition())
        while(self.peek_next().tag != "TERMINATOR"):
            self.expect("SEPARATOR")
            rule_node.definitions.append(self.parse_definition())
        self.expect("TERMINATOR")

        # self.indentator.say(Colors.OKGREEN + 'End Syntax' +  Colors.ENDC)
        # self.indentator.dedent()
        return rule_node

    @loginfo(INDENTATOR)
    def parse_definition(self):
        """"""
        while self.peek_next().tag != "TERMINATOR":
            self.consume()


    def parseTerm(self):
        '''
        Parses a term:
        Term = Factor, ['-', Exception];  //EBNF
        '''
        self.indentator.indent('Parsing Term...')
        self.indentator.say(Colors.OKGREEN + 'New Term' +  Colors.ENDC)
        term = Term()
        factor    = self.parseFactor()
        term.factor = factor
        exception = None
        if self.peek().tag == 'EXCEPT':
            self.expect('EXCEPT')
            exception = self.parseException()
            term.exception = exception
        self.indentator.say(Colors.OKGREEN + 'End Syntax with values: ' +  Colors.ENDC)
        self.indentator.dedent()
        return term

    def parseException(self):
        '''
        Parses an Exception:
        Exception = Factor;  //EBNF
        '''
        self.indentator.indent('Parsing Exception')
        self.indentator.say(Colors.OKGREEN + 'New Exception' +  Colors.ENDC)
        exception = Exception()
        factor = self.parseFactor()
        exception.factor = factor
        self.indentator.say(Colors.OKGREEN + 'End Exception with value: ' +  Colors.ENDC)
        self.indentator.dedent()
        return exception

    def parseFactor(self):
        '''
        Parses a factor:
        Factor = [Integer, '*'], Primary; //EBNF
        '''
        self.indentator.indent('Parsing Factor')
        self.indentator.say(Colors.OKGREEN + 'New Factor' +  Colors.ENDC)
        factor = Factor()
        integer = 0
        factor.integer = integer
        if self.peek().tag == 'DIGIT':
            integer = self.parseInteger()
            factor.integer = integer
            self.expect('REPETITION')
        primary = self.parsePrimary()
        factor.primary = primary
        self.indentator.say(Colors.OKGREEN + 'End Factor with values:' +  Colors.ENDC)
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
        self.indentator.indent('Parsing Primary...')
        self.indentator.say(Colors.OKGREEN + 'New Primary' +  Colors.ENDC)
        primary = Primary()
        # A primary can consist of different type of objects and is parsed accordingly
        if self.peek().tag == 'LBRACKET':
            optionalSeq = self.parseOptionalSeq()
            primary.optionalSeq = optionalSeq
        elif self.peek().tag == 'LBRACE':
            repeatedSeq = self.parseRepeatedSeq()
            primary.repeatedSeq = repeatedSeq
        elif self.peek().tag == 'LPAREN':
            groupedSeq = self.parseGroupedSeq()
            primary.groupedSeq = groupedSeq
        elif self.peek().tag == 'SPECIAL':
            specialSeq = self.parseSpecialSeq()
            primary.specialSeq = specialSeq
        elif self.peek().tag in Parser.TERMINAL_STRING:
            terminalString = self.parseTerminalString()
            primary.terminalString = terminalString
        elif self.peek().tag == 'IDENTIFIER':
            identifier = self.parseIdentifier()
            primary.identifier = identifier
        else:
            empty = self.parseEmpty()
            primary.empty = empty
        self.indentator.say(Colors.OKGREEN + 'End Primary' +  Colors.ENDC)
        self.indentator.dedent()
        return primary

    def parseOptionalSeq(self):
        '''
        Parses an optional sequence:
        OptionalSeq = '[', Definitions, ']';  //EBNF
        '''
        self.indentator.indent('Parsing Optional Sequence...')
        self.indentator.say(Colors.OKGREEN + 'New Optional Sequence' +  Colors.ENDC)
        optionalSeq = OptionalSeq()
        self.expect('LBRACKET')
        definitions = self.parseDefinitions()
        optionalSeq.definitions = definitions
        self.expect('RBRACKET')
        self.indentator.say(Colors.OKGREEN + 'End Optional Sequence')
        self.indentator.dedent()
        return optionalSeq

    def parseRepeatedSeq(self):
        '''
        Parses a repeated sequence:
        RepeatedSeq = '{', Definitions, '}';  //EBNF
        '''
        self.indentator.indent('Parsing Repeated Sequence...')
        self.indentator.say(Colors.OKGREEN + 'Repeated Sequence' +  Colors.ENDC)
        repeatedSeq = RepeatedSeq()
        self.expect('LBRACE')
        definitions = self.parseDefinitions()
        repeatedSeq.definitions = definitions
        self.expect('RBRACE')
        self.indentator.dedent()
        self.indentator.say(Colors.OKGREEN + 'End Repeated Sequence')
        return repeatedSeq

    def parseGroupedSeq(self):
        '''
        Parses a grouped sequence:
        GroupedSeq = '(', Definitions, ')';  //EBNF
        '''
        self.indentator.indent('Parsing Grouped Sequence...')
        self.indentator.say(Colors.OKGREEN + 'New Group Sequence' +  Colors.ENDC)
        groupedSeq = GroupedSeq()
        self.expect('LPAREN')
        definitions = self.parseDefinitions()
        groupedSeq.definitions = definitions
        self.expect('RPAREN')
        self.indentator.dedent()
        self.indentator.say(Colors.OKGREEN + 'End Grouped Sequence' +  Colors.ENDC)
        return groupedSeq

    def parseSpecialSeq(self):
        '''
        Parses a special sequence:
        SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
        '''
        self.indentator.indent('Parsing Special Sequence...')
        self.indentator.say(Colors.OKGREEN + 'New Special Sequence' +  Colors.ENDC)
        specialSeq = SpecialSeq()
        token = self.expect('SPECIAL')
        value = token.value
        specialSeq.value = value
        self.indentator.dedent()
        self.indentator.say(Colors.OKGREEN + 'End Special Sequence')
        return specialSeq

    def parseTerminalString(self):
        '''
        Parses a terminal string:
        TerminalString = "'", Character - "'", {Character - "'"}, "'"
                       | '"', Character - '"', {Character - '"'}, '"';  //EBNF
        '''
        self.indentator.indent('Parsing Terminal String...')
        self.indentator.say(Colors.OKGREEN + 'New Terminal String' +  Colors.ENDC)
        if self.peek().tag == 'SQUOTE':
            terminalString = TerminalStringSQuote()
            token = self.expect('SQUOTE')
            value = token.value
            terminalString.value = value
        elif self.peek().tag == 'DQUOTE':
            terminalString = TerminalStringDQuote()
            token = self.expect('DQUOTE')
            value = token.value
            terminalString.value = value
        self.indentator.say(Colors.OKGREEN + 'TERMINAL STRING ' + Colors.ENDC + Colors.OKBLUE + value)
        self.indentator.say(Colors.OKGREEN + 'End Terminal String')
        self.indentator.dedent()
        return terminalString

    def parseIdentifier(self):
        '''
        Parses an identifier:    (already done in the lexer)
        Identifier = Letter, {Letter | Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Identifier...')
        self.indentator.say(Colors.OKGREEN + 'New Identifier' +  Colors.ENDC)
        identifier = Identifier()
        token = self.expect('IDENTIFIER')
        value = token.value
        identifier.value = value
        self.indentator.say(Colors.OKGREEN + 'IDENTIFIER ' + Colors.ENDC + Colors.OKBLUE + value)
        self.indentator.say(Colors.OKGREEN + 'End Identifier' + Colors.ENDC)
        self.indentator.dedent()
        return identifier

    def parseEmpty(self):
        '''
        Parses an empty primary:
        Empty = ;  //EBNF
        '''
        self.indentator.indent('Parsing Empty...')
        self.indentator.say(Colors.OKGREEN + 'New Empty' +  Colors.ENDC)
        empty = Empty()
        self.indentator.dedent()
        self.indentator.say(Colors.OKGREEN + 'End Empty' +  Colors.ENDC)
        return empty

    def parseInteger(self):
        '''
        Parses an integer:   (already done in the lexer)
        Integer = Digit, {Digit};  //EBNF
        '''
        self.indentator.indent('Parsing Integer...')
        self.indentator.say(Colors.OKGREEN + 'New Integer' +  Colors.ENDC)
        integer = Integer()
        token = self.expect('INTEGER')
        value = token.value
        integer.value = value
        self.indentator.say(Colors.OKGREEN + 'INTEGER ' + Colors.ENDC + Colors.OKBLUE + value)
        self.indentator.say(Colors.OKGREEN + 'End Integer' +  Colors.ENDC)
        self.indentator.dedent()
        return integer
