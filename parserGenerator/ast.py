from visitor import Visitor

class Node():
    def accept(self, visitor, args):
        className  = self.__class__.__name__
        methodName = getattr(visitor, "visit" + className)
        visitor.nomMethode(self, args)


class Grammar(Node):
    def __init__(self,syntax=[]):
        self.syntax = syntax

    def __repr__(self):
        string = "Grammar - "
        string += str(self.syntax)
        return string

class Syntax(Node):
    def __init__(self,syntaxRules=[]):
        self.syntaxRules = syntaxRules

    def __repr__(self):
        string = "Syntax - "
        for syntaxRule in self.syntaxRules:
            string += str(syntaxRule)
        return string


class SyntaxRule(Node):
    def __init__(self,identifier=None,definitions=[]):
        self.identifier  = identifier
        self.definitions = definitions

    def __repr__(self):
        string = "Syntax Rule - {0}".format(self.identifier)
        for definition in self.definitions.definitions:
            string += str(definition) + '\n'
        return string

class Definitions(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Definitions - "
        for definition in self.definitions:
            string += str(definition)
        return string

class Definition(Node):
    def __init__(self,terms=[]):
        self.terms = []

    def __repr__(self):
        string = "Definition - "
        for term in self.terms:
            string += str(term)
        return string


class Term(Node):
    def __init__(self,factor=None,exception=None):
        self.factor    = factor
        self.exception = exception

    def __repr__(self):
        string = "Term - {0}".format(self.factor)
        if self.exception != None:
            string += '- {0}'.format(self.exception)
        return string

class Exception(Node):
    def __init__(self,factor=None):
        self.factor = factor

    def __repr__(self):
        return "Exception - {0}".format(self.factor)

class Factor(Node):
    def __init__(self,integer=0,primary=None):
        self.integer = integer
        self.primary = primary

    def __repr__(self):
        string = "Factor - "
        if self.integer != 0:
            string += str(integer) + "* "
        string += str(self.primary)
        return string

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

    def __repr__(self):
        pass
        # For arguments, if not none --> print

class OptionalSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Optional Sequence - [ "
        for definition in definitions:
            string += str(definition)
        string += "]"
        return string

class RepeatedSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Repeated Sequence - { "
        for definition in definitions:
            string += str(definition)
        string += "}"
        return string

class GroupedSeq(Node):
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def __repr__(self):
        string = "Grouped Sequence - ( "
        for definition in definitions:
            string += str(definition)
        string += ")"
        return string

class SpecialSeq(Node):
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Special Sequence - ? {0} ?".format(self.value)

class TerminalString(Node):
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Terminal String - {0}".format(self.value)

class TerminalStringSQuote(TerminalString):
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\"'

    def __repr__(self):
        return "Terminal String (S Quote) - {0}{1}{0}".format(self.separator,self.value)


class TerminalStringFQuote(TerminalString):
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\''

    def __repr__(self):
        return "Terminal String (F Quote) - {0}{1}{0}".format(self.separator,self.value)

class Identifier(Node):
    def __init__(self,value=''):
        self.value = value

    def __repr__(self):
        return "Identifier - {0} ".format(self.value)

class Empty(Node):
    def __init__(self):
        pass

    def __repr__(self):
        return "Empty Primary"

class Integer(Node):
    def __init__(self,value=0):
        self.value = value

    def __repr__(self):
        return "Integer - {0}".format(self.value)
