# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


import sys

from mitos.ast import DefinitionNode
from mitos.ast import EmptyNode
from mitos.ast import FactorNode
from mitos.ast import GrammarNode
from mitos.ast import GroupNode
from mitos.ast import IdentifierNode
from mitos.ast import IntegerNode
from mitos.ast import OptionNode
from mitos.ast import PrimaryNode
from mitos.ast import RepetitionNode
from mitos.ast import RuleNode
from mitos.ast import SpecialNode
from mitos.ast import StringNode
from mitos.ast import TermNode
from mitos.utils import Indentator
from mitos.utils import loginfo


class Parser:
    """
    EBNF main parser class of the system.

    verbose: boolean - Run the parser in verbose mode to obtain outputs in the terminal.

    Note: The comments display extracts of the EBNF's EBNF grammar and those lines are followed by "//EBNF".
    You can refer to the full grammar in grammars/ebnf.ebnf
    """
    TERMINAL_STRING = ['SQUOTE', 'DQUOTE']
    INDENTATOR = Indentator()

    def __init__(self, verbose=False):
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

    def next_tag_equals(self, tag):
        """Check if the next token has the given tag WITHOUT popping it"""
        return self.peek_next().tag == tag

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
        self.lexems = [lexem for lexem in self.lexems if lexem.tag != "COMMENT"]

    # ======================== #
    #     PARSING FUNCTIONS    #
    # ======================== #

    def parse(self, lexems):
        """Entry point function: launches the parsing operation."""
        self.lexems = lexems
        self.remove_comments()
        grammar_node = self.parse_grammar()
        return grammar_node

    @loginfo(INDENTATOR)
    def parse_grammar(self):
        """grammar = { rule } ;"""
        grammar_node = GrammarNode()
        while (len(self.lexems) > 0):
            rule_node = self.parse_rule()
            grammar_node.rules.append(rule_node)
        print("Parser: analysis successful!")
        return grammar_node

    @loginfo(INDENTATOR)
    def parse_rule(self):
        """rule  = identifier, '=', definition, {'|', definition} ';';"""
        rule_node = RuleNode()
        rule_node.identifier = self.parse_identifier()
        self.expect("ASSIGN")
        rule_node.definitions.append(self.parse_definition())
        while not self.next_tag_equals("TERMINATOR"):
            self.expect("SEPARATOR")
            rule_node.definitions.append(self.parse_definition())
        self.expect("TERMINATOR")
        return rule_node

    @loginfo(INDENTATOR)
    def parse_definition(self):
        """definition = term, {',', term};"""
        definition_node = DefinitionNode()
        definition_node.terms.append(self.parse_term())
        while self.next_tag_equals("CONCATENATION"):
            self.consume()  # Remove the ','
            definition_node.terms.append(self.parse_term())
        return definition_node

    @loginfo(INDENTATOR)
    def parse_term(self):
        """term = factor, ['-', exception];"""
        term_node = TermNode()
        term_node.factor = self.parse_factor()
        if self.next_tag_equals("EXCEPT"):
            term_node.exception = self.parse_factor()
        return term_node

    @loginfo(INDENTATOR)
    def parse_factor(self):
        """factor = [integer, '*'], primary;"""
        factor_node = FactorNode()
        if self.next_tag_equals("INTEGER"):
            factor_node.integer = self.expect("INTEGER")
            self.expect("REPETITION")
        factor_node.primary = self.parse_primary()
        return factor_node

    @loginfo(INDENTATOR)
    def parse_primary(self):
        """primary = option | repetition | group | special | string | identifier | empty;"""
        primary_node = PrimaryNode()
        option_dictionary = {
            # Group nodes
            "LBRACKET":   self.parse_option,
            "LPAREN":     self.parse_group,
            "LBRACE":     self.parse_repetition,
            # Special sequences nodes
            "SPECIAL":    self.parse_special,
            "STRING":     self.parse_string,
            "INTEGER":    self.parse_integer,
            "IDENTIFIER": self.parse_identifier,
            # Empry node
            "TERMINATOR": self.parse_empty,
        }
        # Run the next token's tag into the option dictionary and apply its method
        primary_node.expression = option_dictionary[self.peek_next().tag]()
        return primary_node

    @loginfo(INDENTATOR)
    def parse_option(self):
        """option = '[',  definition, {'|', definition}, ']';"""
        option_node = OptionNode()
        self.expect("LBRACKET")
        option_node.definitions.append(self.parse_definition())
        while not self.next_tag_equals("RBRACKET"):
            self.expect("SEPARATOR")
            option_node.definitions.append(self.parse_definition())
        self.expect("RBRACKET")
        return option_node

    @loginfo(INDENTATOR)
    def parse_group(self):
        """group = '(',  definition, {'|', definition}, ')';"""
        group_node = GroupNode()
        self.expect("LPAREN")
        group_node.definitions.append(self.parse_definition())
        while not self.next_tag_equals("RPAREN"):
            self.expect("SEPARATOR")
            group_node.definitions.append(self.parse_definition())
        self.expect("RPAREN")
        return group_node

    @loginfo(INDENTATOR)
    def parse_repetition(self):
        """repetition = '{',  definition, {'|', definition}, '}';"""
        repetition_node = RepetitionNode()
        self.expect("LBRACE")
        repetition_node.definitions.append(self.parse_definition())
        while not self.next_tag_equals("RBRACE"):
            self.expect("SEPARATOR")
            repetition_node.definitions.append(self.parse_definition())
        self.expect("RBRACE")
        return repetition_node

    @loginfo(INDENTATOR)
    def parse_special(self):
        """special = REGEXED!"""
        special_node = SpecialNode()
        special_node.sequence = self.expect("SPECIAL")
        return special_node

    @loginfo(INDENTATOR)
    def parse_string(self):
        """string = REGEXED!"""
        string_node = StringNode()
        string_node.string = self.expect("STRING")
        return string_node

    @loginfo(INDENTATOR)
    def parse_identifier(self):
        """identifier = REGEXED!"""
        identifier_node = IdentifierNode()
        identifier_node.identifier = self.expect("IDENTIFIER")
        return identifier_node

    @loginfo(INDENTATOR)
    def parse_integer(self):
        """integer = REGEXED!"""
        integer_node = IntegerNode()
        integer_node.integer = self.expect("INTEGER")
        return integer_node

    @loginfo(INDENTATOR)
    def parse_empty(self):
        """empty = ;"""
        empty_node = EmptyNode()
        return empty_node
