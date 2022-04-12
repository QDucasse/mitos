# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""

class Visitor:
    """Placeholder example of a visitor, pretty print"""

    def visit(self, node):
        node.accept(self)

    def visit_grammar(self, grammar):
        """grammar = { rule };"""
        for rule in grammar.rules:
            self.visit(rule)

    def visit_rule(self, rule):
        """rule  = identifier, '=', definition, {'|', definition} ';';"""
        self.visit(rule.identifier)
        for definition in rule.definitions:
            self.visit(definition)

    def visit_definition(self, definition):
        """definition = term, {',', term};"""
        for term in definition.terms:
            self.visit(term)

    def visit_term(self, term):
        """term = factor, ['-', factor];"""
        self.visit(term.factor)
        if term.exception is not None:
            self.visit(term.exception)

    def visit_factor(self, factor):
        """factor = [integer, '*'], primary;"""
        if factor.integer is not None:
            self.visit(factor.integer)
        self.visit(factor.primary)

    def visit_primary(self, primary):
        """primary = option | repetition | group | special | string | identifier | empty;"""
        self.visit(primary.expression)

    def visit_option(self, option):
        """option = '[',  definition, {'|', definition}, ']';"""
        for definition in option.definitions:
            self.visit(definition)

    def visit_repetition(self, repetition):
        """repetition = '{',  definition, {'|', definition}, '}';"""
        for definition in repetition.definitions:
            self.visit(definition)

    def visit_group(self, group):
        """group = '(',  definition, {'|', definition}, ')';"""
        for definition in group.definitions:
            self.visit(definition)

    def visit_empty(self, empty):
        """empty = ;"""

    def visit_special(self, special):
        """special = REGEXED!"""

    def visit_identifier(self, identifier):
        """identifier = REGEXED!"""

    def visit_integer(self, integer):
        """integer = REGEXED!"""

    def visit_string(self, string):
        """string = REGEXED!"""
