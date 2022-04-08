# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:35:45 2019

@author: Quentin Ducasse & Kevin Bedin
"""

class Visitor(object):
    '''
    Main visitor class
    Templating the successive accept calls in order to be used by
    the subclasses lexerWriter and parserWriter
    '''
    def visit(self,grammar):
        grammar.accept(self,grammar)

    def visitGrammar(self,grammar):
        '''Visits grammar'''
        # Visit the syntax element
        syntax = grammar.syntax
        syntax.accept(self,syntax)

    def visitSyntax(self,syntax):
        '''Visits all syntax rules'''
        for syntaxRule in syntax.syntaxRules:
            syntaxRule.accept(self,syntaxRule)

    def visitSyntaxRule(self,syntaxRule):
        '''Visits one syntax rule'''
        # Visit identifier
        id   = syntaxRule.identifier
        # Visit all the definitions
        defs = syntaxRule.definitions
        id.accept(self,id)
        defs.accept(self,defs)

    def visitDefinitions(self,definitions):
        '''Visits all definitions'''
        for definition in definitions.definitions:
            definition.accept(self,definition)

    def visitDefinition(self,definition):
        '''Visit a definition'''
        # Visits all terms
        for term in definition.terms:
            term.accept(self,term)

    def visitTerm(self,term):
        '''Visit a term'''
        # Visits the factor
        term.factor.accept(self,term.factor)
        # Visits the exception
        exception = term.exception
        if exception != None:
            term.exception.accept(self,term.exception)

    def visitException(self,exception):
        '''Visit the exception'''
        exception.factor.accept(self,exception.factor)

    def visitFactor(self,factor):
        '''Visit a factor'''
        # Visits the primary
        factor.primary.accept(self,factor.primary)

    def visitPrimary(self,primary):
        '''Visit a primary'''
        if primary.optionalSeq != None:
            primary.optionalSeq.accept(self,primary.optionalSeq)
        elif primary.identifier != None:
            primary.identifier.accept(self,primary.identifier)
        elif primary.repeatedSeq != None:
            primary.repeatedSeq.accept(self,primary.repeatedSeq)
        elif primary.groupedSeq != None:
            primary.groupedSeq.accept(self,primary.groupedSeq)
        elif primary.specialSeq != None:
            primary.specialSeq.accept(self,primary.specialSeq)
        elif primary.terminalString != None:
            primary.terminalString.accept(self,primary.terminalString)
        elif primary.empty != None:
            primary.empty.accept(self,primary.empty)

    def visitOptionalSeq(self,optionalSeq):
        '''Visit an optional sequence'''
        optionalSeq.definitions.accept(self,optionalSeq.definitions)

    def visitRepeatedSeq(self,repeatedSeq):
        '''Visit a repeated sequence'''
        repeatedSeq.definitions.accept(self,repeatedSeq.definitions)

    def visitGroupedSeq(self,groupedSeq):
        '''Visit a grouped sequence'''
        groupedSeq.definitions.accept(self,groupedSeq.definitions)

    def visitSpecialSeq(self,specialSeq):
        pass

    def visitTerminalString(self,terminalString):
        pass

    def visitTerminalStringSQuote(self,terminalStringSQuote):
        pass

    def visitTerminalStringDQuote(self,terminalStringDQuote):
        pass

    def visitIdentifier(self,identifier):
        pass

    def visitEmpty(self,empty):
        pass

    def visitInteger(self,integer):
        pass
