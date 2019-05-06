from visitor import Visitor

class Node():
    def accept(self, visitor, args):
        className  = self.__class__.__name__
        methodName = getattr(visitor, "visit" + className)
        visitor.nomMethode(self, args)


class Grammar(Node):
    def __init__(self,syntax=[]):
        self.syntax = syntax

class Syntax(Node):
    def __init__(self,syntaxRules=[]):
        self.syntaxRules = syntaxRules

class SyntaxRule(Node):
    def __init__(self,identifier=None,definitions=[]):
        self.identifier  = identifier
        self.definitions = definitions

class Definitions(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

class Definition(Node):
    def __init__(self,terms=[]):
        self.terms = []

class Term(Node):
    def __init__(self,factor=None,exception=None):
        self.factor    = factor
        self.exception = exception

class Exception(Node):
    def __init__(self,factor=None):
        self.factor = factor

class Factor(Node):
    def __init__(self,integer=0,primary=None):
        self.integer = integer
        self.primary = primary

class Primary(Node):
    def __init__(self,optionalSeq    = None,
                      repeatedSeq    = None,
                      groupedSeq     = None,
                      specialSeq     = None,
                      terminalString = None,
                      identifier     = None,
                      empty          = None):
        self.optionalSeq    = optionalSeq
        self.repeatedSeq    = repeatedSeq
        self.groupedSeq     = groupedSeq
        self.specialSeq     = specialSeq
        self.terminalString = terminalString
        self.identifier     = identifier
        self.empty          = empty

class OptionalSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

class RepeatedSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

class GroupedSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

class SpecialSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

class TerminalString(Node):
    def __init__(self,value=''):
        self.value = value

class Identifier(Node):
    def __init__(self,value=''):
        self.value = value

class Empty(Node):
    def __init__(self):
        
class Integer(Node):
    def __init__(self,value=0):
        self.value = value
