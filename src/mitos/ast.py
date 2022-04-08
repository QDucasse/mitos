# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""

class GrammarNode:
    """grammar = { rule };"""
    def __init__(self,rules=None):
        self.rules = rules if rules is not None else []

    def accept(self, visitor):
        self.visitor.visit_grammar(self)

class RuleNode:
    """rule = identifier , "=" , expression , ";" ;"""
    def __init__(self, identifier=None, definitions=None):
        self.identifier = identifier
        self.definitions = definitions if definitions is not None else []





class ExpressionNode:
    """
    expression = identifier
         | terminal
         | "-", expression
         | "[" , expression , "]"
         | "{" , expression , "}"
         | "(" , expression , ")"
         | expression , "|" , expression
         | expression , "," , expression ;
    """
    def __init__(self,identifier=None,definitions=None):
        self.identifier  = identifier
        self.definitions = definitions

class Definitions:
    ##### TODO : SAME AS SYNTAX RULE, NO NEED FOR DEFINITIONS
    ############# OR NEED FOR SYNTAX RULES
    '''
    A set of definitions
    Definitions = Definition, {'|', Definition};  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

    def addDefinition(self,definition):
        self.definitions.append(definition)

class Definition:
    '''
    A definition (a set of terms)
    Definition = Term, {',', Term};  //EBNF
    '''
    def __init__(self,terms=[]):
        self.terms = []

    def addTerm(self,term):
        self.terms.append(term)

class Term:
    '''
    A term (Factor & Exception)
    Term = Factor, ['-', Exception];  //EBNF
    '''
    def __init__(self,factor=None,exception=None):
        self.factor    = factor
        self.exception = exception

class Exception:
    '''
    An exception
    Exception = Factor;  //EBNF
    '''
    def __init__(self,factor=None):
        self.factor = factor

class Factor:
    '''
    A factor
    Factor = [Integer, '*'], Primary; //EBNF
    '''
    def __init__(self,integer=0,primary=None):
        self.integer = integer
        self.primary = primary

class Primary:
    '''
    A primary corresponding to either of those sequence:
    Primary = OptionalSeq
            | RepeatedSeq
            | GroupedSeq
            | SpecialSeq
            | TerminalString
            | Identifier
            | Empty;            //EBNF
    '''
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

class OptionalSeq:
    '''
    An optional sequence:
    OptionalSeq = '[', Definitions, ']';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class RepeatedSeq:
    '''
    A repeated sequence:
    RepeatedSeq = '{', Definitions, '}';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class GroupedSeq:
    '''
    A grouped sequence
    GroupedSeq = '(', Definitions, ')';  //EBNF
    '''
    def __init__(self,definitions=[]):
        self.definitions = definitions

class SpecialSeq:
    '''
    A special Sequence
    SpecialSeq = '?', {Character - '?'}, '?';  //EBNF
    '''
    def __init__(self,value=''):
        self.value = value

class TerminalString:
    def __init__(self,value=''):
        self.value = value

class TerminalStringSQuote(TerminalString):
    '''
    A terminal string with simple quotes
    TerminalString = "'", Character - "'", {Character - "'"}, "'" //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\''

class TerminalStringDQuote(TerminalString):
    '''
    A terminal string with double quotes
    TerminalString = '"', Character - '"', {Character - '"'}, '"' //EBNF
    '''
    def __init__(self,value=''):
        super().__init__(value)
        self.separator = '\"'

class Identifier:
    '''
    An identifier
    Identifier = Letter, {Letter | Digit};  //EBNF
    --> Simplified with a value only here
    '''
    def __init__(self,value=''):
        self.value = value

class Empty:
    '''
    An empty primary
    Empty = ;  //EBNF
    '''
    def __init__(self):
        pass

class Integer:
    '''
    An integer
    Integer = Digit, {Digit};  //EBNF
     --> Simplified with a value only here
    '''
    def __init__(self,value=0):
        self.value = value
