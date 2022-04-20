# -*- coding: utf-8 -*-
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m mitos` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``mitos.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``mitos.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
@author: Quentin Ducasse
"""


import sys

from mitos.compiler import Compiler


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Launches the compilation passes on an EBNF grammar
    """
    if len(argv) != 2:
        print("Error: Please provide a file to process.")
        sys.exit(1)
    file_name = argv[1]
    try:
        with open(file_name, 'r') as file:
            file_data = file.readlines()
    except FileNotFoundError:
        print('Error: test file {} does not exist'.format(file_name))
        sys.exit()

    # The compiler will:
    #  - lex the raw data through the lexer and generate lexems
    #  - parse the lexems through the parser and generate an AST
    #  - visit the AST and pretty print the source code back

    compiler = Compiler()
    res = compiler.compile(file_data)
    print(res)
