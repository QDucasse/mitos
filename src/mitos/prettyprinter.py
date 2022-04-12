# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""

from mitos.visitor import Visitor


class PrettyPrinter(Visitor):
    """Visitor example that displays the source program back"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_string = ""

    def pretty_print(self, ast):
        self.visit(ast)
        print(self.display_string)

    def visit_grammar(self, grammar):
        """grammar = { rule };"""
        for rule in grammar.rules:
            self.visit(rule)

    def visit_rule(self, rule):
        """rule  = identifier, '=', definition, {'|', definition} ';';"""
        self.visit(rule.identifier)
        self.display_string += " = "
        self.visit(rule.definitions[0])
        for definition in rule.definitions[1:]:
            self.display_string += " | "
            self.visit(definition)
        self.display_string += ";\n"

    def visit_definition(self, definition):
        """definition = term, {',', term};"""
        self.visit(definition.terms[0])
        for term in definition.terms[1:]:
            self.display_string += " , "
            self.visit(term)

    def visit_term(self, term):
        """term = factor, ['-', factor];"""
        self.visit(term.factor)
        if term.exception is not None:
            self.display_string += " - "
            self.visit(term.exception)

    def visit_factor(self, factor):
        """factor = [integer, '*'], primary;"""
        if factor.integer is not None:
            self.visit(factor.integer)
            self.display_string += " * "
        self.visit(factor.primary)

    def visit_primary(self, primary):
        """primary = option | repetition | group | special | string | identifier | empty;"""
        self.visit(primary.expression)

    def visit_option(self, option):
        """option = '[',  definition, {'|', definition}, ']';"""
        self.visit(option.definitions[0])
        for definition in option.definitions[1:]:
            self.display_string += " | "
            self.visit(definition)

    def visit_repetition(self, repetition):
        """repetition = '{',  definition, {'|', definition}, '}';"""
        self.visit(repetition.definitions[0])
        for definition in repetition.definitions[1:]:
            self.display_string += " | "
            self.visit(definition)

    def visit_group(self, group):
        """group = '(',  definition, {'|', definition}, ')';"""
        self.visit(group.definitions[0])
        for definition in group.definitions[1:]:
            self.display_string += " | "
            self.visit(definition)

    def visit_empty(self, empty):
        """empty = ;"""

    def visit_special(self, special):
        """special = REGEXED!"""
        self.display_string += special.sequence.value

    def visit_identifier(self, identifier):
        """identifier = REGEXED!"""
        self.display_string += identifier.identifier.value

    def visit_integer(self, integer):
        """integer = REGEXED!"""
        self.display_string += integer.integer.value

    def visit_string(self, string):
        """string = REGEXED!"""
        self.display_string += string.string.value
