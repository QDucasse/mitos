# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""

import re


def empty_if_none(value):
    return value if value is not None else []


class BaseNode:
    def accept(self, visitor):
        """Meta-defining the accept method for the subclasses"""
        # Formatting the name
        class_name_camel_case = self.__class__.__name__[:-4]
        class_name_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name_camel_case).lower()
        method_name = getattr(visitor, "visit_" + class_name_snake_case)
        # Casting the visit<class_name> method on the visitor
        method_name(self)


class GrammarNode(BaseNode):
    """grammar = { rule };"""
    def __init__(self, rules=None):
        self.rules = empty_if_none(rules)


class RuleNode(BaseNode):
    """rule  = identifier, '=', definition, {'|', definition} ';';"""
    def __init__(self, identifier=None, definitions=None):
        self.identifier = identifier
        self.definitions = empty_if_none(definitions)


class DefinitionNode(BaseNode):
    """definition = term, {',', term};"""
    def __init__(self, terms=None):
        self.terms = empty_if_none(terms)


class TermNode(BaseNode):
    """term = factor, ['-', factor];"""
    def __init__(self, factor=None, exception=None):
        self.factor = factor
        self.exception = exception


class FactorNode(BaseNode):
    """factor = [integer, '*'], primary;"""
    def __init__(self, integer=None, primary=None):
        self.integer = integer
        self.primary = primary


class PrimaryNode(BaseNode):
    """primary = option | repetition | group | special | string | identifier | empty;"""
    def __init__(self, expression=None):
        self.expression = expression


class OptionNode(BaseNode):
    """option = '[',  definition, {'|', definition}, ']';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class RepetitionNode(BaseNode):
    """repetition = '{',  definition, {'|', definition}, '}';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class GroupNode(BaseNode):
    """group = '(',  definition, {'|', definition}, ')';"""
    def __init__(self, definitions=None):
        self.definitions = empty_if_none(definitions)


class EmptyNode(BaseNode):
    """empty = ;"""


class SpecialNode(BaseNode):
    """special = REGEXED!"""
    def __init__(self, sequence=None):
        self.sequence = sequence


class IdentifierNode(BaseNode):
    """identifier = REGEXED!"""
    def __init__(self, identifier=None):
        self.identifier = identifier


class IntegerNode(BaseNode):
    """integer = REGEXED!"""
    def __init__(self, integer=None):
        self.integer = integer


class StringNode(BaseNode):
    """string = REGEXED!"""
    def __init__(self, string=None):
        self.string = string
