#!/usr/bin/python3

import sqlparse
import ast
import sys
import re
import inspect
import logging

def typename(x):
    return type(x).__name__

def escape(text):
    text = text \
        .replace('"', '`') \
        .replace('\'', '`') \
        .replace(' ', '-SP-') \
        .replace('\t', '-TAB-') \
        .replace('\n', '-NL-') \
        .replace('(', '-LRB-') \
        .replace(')', '-RRB-') \
        .replace('|', '-BAR-') \
        .replace('<=', '-LOE-') \
        .replace('>=', '-GOE-') \
        .replace('=', '-EQUALS-') \
        .replace('<', '-LESS-') \
        .replace('>', '-GREATER-') \
        .replace('*', '-ALL-') 
    return repr(text)[1:-1] if text else '-NONE-'

def makestr(node):

    #if node is None or isinstance(node, ast.Pass):
    #    return ''

    if isinstance(node, ast.AST):
        n = 0
        nodename = typename(node)
        s = '(' + nodename
        for chname, chval in ast.iter_fields(node):
            chstr = makestr(chval)
            if chstr:
                s += ' (' + chname + ' ' + chstr + ')'
                n += 1
        if not n:
            s += ' -' + nodename + '-' # (Foo) -> (Foo -Foo-)
        s += ')'
        return s

    elif isinstance(node, list):
        n = 0
        s = '(list'
        for ch in node:
            chstr = makestr(ch)
            if chstr:
                s += ' ' + chstr
                n += 1
        s += ')'
        return s if n else ''

    elif isinstance(node, str):
        return '(str ' + escape(node) + ')'

    elif isinstance(node, bytes):
        return '(bytes ' + escape(str(node)) + ')'

    else:
        return '(' + typename(node) + ' ' + str(node) + ')' #eh aqui q entra

def main():
    for l in sys.stdin:
        l = l.lower()
        l = l.strip()
        l = l.replace(" int)"," integer)")
        l = l.replace(" int "," integer ")
        l = l.replace("varchar(10)", 'character') #teste varchar
        l = l.replace("(",'-LRB-') #teste corpus
        l = l.replace(")",'-RRB-') #teste corpus
        l = l.replace("_","")
        l = l.replace("@","")
        l = l.replace("'","")
        if not l:
            print()
            sys.stdout.flush()
            continue
        parse = sqlparse.parse(l)[0]
        #parse = parse[0] 
        #parse = parse.tokens
        parse = list(parse.flatten()) #teste flatten
        dump = makestr(parse)
        dump = dump.replace("(Token  )","")
        dump = dump.replace("(Token    )","" )
        dump = dump.replace(">="," -GOE- " )
        dump = dump.replace("<="," -LOE- " )
        dump = dump.replace("="," -EQUALS- " )
        dump = dump.replace("_","")
        dump = dump.replace("*", " -ALL- ")
        dump = dump.replace("<", " -LESS- " )
        dump = dump.replace(">", " -GREATER- ")
        dump = dump.replace("'", "")
        dump = dump.replace('"', "")
        dump = dump.replace("None", "")
        #dump = dump.replace("Where where", "Where")
        #dump = dump.replace("(Where fanatical -EQUALS- '1')", "(Token where) (Identifier fanatical) (Token -EQUALS-) (Identifier '1')")
        print(dump)
        #print(parse) #teste para avaliar o parse
        sys.stdout.flush()

if __name__ == '__main__':
    main()