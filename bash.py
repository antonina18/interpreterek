#!/usr/bin/env python3

tokens = (
    'ARG',
    'END',
    'SEMICOLON',
    'PIPE',
    'GT',
    'GTGT',
    'LT',
    'PATH',
)

t_SEMICOLON = r';'
t_PIPE = r'\|'
t_GTGT = r'>>'
t_GT = r'>'
t_LT = r'<'

#t_literals = ";"
t_ignore = " "

last_program = None

def p_program(t):
    "program : statements"
    global last_program
    last_program = t
    #print("PROGRAM", t[1])
    t[0] = t[1]


# def t_NAME(t):
#     r'[a-z]+'
#     return t

def t_ARG(t):
    r'[-a-zA-Z0-9_]+'
    return t

def t_PATH(t):
    r'[a-z]+'
    return t


def t_END(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex

import sys

sys.path.insert(0, "./")

import ast

lexer = lex.lex()

# FUNCTION NAME NAME END

def p_funcname2(p):
    'command : command ARG'
    p[0] = p[1].with_arg(p[2])

def p_funcname(p):
    'command : ARG'
    print("STATEMENT", p[1])
    p[0] = ast.Command(p[1], [])

def p_statement(p):
    'statement : command'
    p[0] = p[1]

def p_statement_pipe(p):
    'command : command PIPE command'
    p[0] = ast.Pipe(p[1], p[3])
    print("PIPE", p[1])


def p_statement_redirect_truncate(p):
    'command : command GT PATH'
    print("TRUNCATE")
    p[0] = ast.TruncateFile(p[1], p[3])

def p_separator(p):
    """
    separator : SEMICOLON
              | END
              | separator END
              | separator SEMICOLON
    """
    print("SEPARATOR", p[1])


def p_statements(p):
    """
    statements : statement
    """
    p[0] = [p[1]]

def p_statements_multiple(p):
    """
    statements : statements separator statement
    """
    p[0] = p[1] + [p[3]]


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p)
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc
yacc.yacc()


import sys

if len(sys.argv) < 2:
    print("USAGE: " + sys.argv[0] + " file.sh")
    sys.exit(1)

file = open(sys.argv[1])
code = file.read()

file.close()

lexer.input(code)

while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    # print(tok)

yacc.parse(code, debug = 0)

import subprocess

for statement in last_program[0]:
    statement.evaluate(sys.stdin, sys.stdout, sys.stderr).wait()
# program : statements
# statements: statement
#          |  statements statement
# statement:  FUNCTION name ';'

