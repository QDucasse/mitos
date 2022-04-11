# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""


def empty_if_none(value):
    return value if value is not None else []


class GrammarNode:
    """grammar = { rule };"""
    def __init__(self, rules=None):
        self.rules = empty_if_none(rules)

    def accept(self, visitor):
        self.visitor.visit_grammar(self)


class RuleNode:
    """rule = identifier , "=" , expression , ";" ;"""
    def __init__(self, identifier=None, definitions=None):
        self.identifier = identifier
        self.definitions = empty_if_none(definitions)


class DefinitionNode:
    """definition = term, {',', term};"""
    def __init__(self, terms=None):
        self.terms = empty_if_none(terms)


class TermNode:
    """term = factor, ['-', exception];"""
    def __init__(self, factor=None, exception=None):
        self.factor = factor
        self.exception = exception


class FactorNode:
    """factor = [integer, '*'], primary;"""
    def __init(self, integer=None, primary=None):
        self.integer = integer
        self.primary = primary


class PrimaryNode:
    """primary = option | repetition | group | special | string | identifier | empty;"""
    def __init__(self, expression=None):
        self.expression = expression


class OptionNode:
    """option = '[',  definition, {'|', definition}, ']';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class RepetitionNode:
    """repetition = '{',  definition, {'|', definition}, '}';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class GroupNode:
    """group = '(',  definition, {'|', definition}, ')';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class EmptyNode:
    """empty = ;"""


class SpecialNode:
    """special = REGEXED!"""
    def __init__(self, sequence=None):
        self.sequence = sequence


class IdentifierNode:
    """identifier = REGEXED!"""
    def __init__(self, identifier=None):
        self.identifier = identifier


class IntegerNode:
    """integer = REGEXED!"""
    def __init__(self, integer=None):
        self.integer = integer


class StringNode:
    """string = REGEXED!"""
    def __init__(self, string=None):
        self.string = string
