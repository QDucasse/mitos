# -*- coding: utf-8 -*-
"""
Utilities, indentator, log decorator and colors
@author: Quentin Ducasse & Kevin Bedin
"""
import functools


class Indentator:
    """An indentator simplifying information display with automated tabulations."""
    INDENT = 2

    def __init__(self):
        self.indentation = 0
        self.verbose = False

    def indent(self):
        self.indentation += self.INDENT

    def dedent(self):
        self.indentation -= self.INDENT

    def prepare_string(self, text):
        output = ''
        if (self.indentation > 0):
            for i in range(1, self.indentation):
                output += ' '
        output += text
        return output

    def say(self, text):
        if self.verbose:
            print(self.prepare_string(text))


def loginfo(indentator):
    def decorator_loginfo(func):
        @functools.wraps(func)
        def wrapper_loginfo(*args, **kwargs):
            indentator.say("Parsing {}...".format(func.__name__.split("_")[1]))
            indentator.indent()
            value = func(*args, **kwargs)
            indentator.dedent()
            indentator.say("End of {} parsing".format(func.__name__.split("_")[1]))
            return value
        return wrapper_loginfo
    return decorator_loginfo


class Colors(object):
    '''
    Classic colors that can be used to display more pleasantly information
    in the terminal
    ex: Colors.OKGREEN + 'Text in Green!' +  Colors.ENDC
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
