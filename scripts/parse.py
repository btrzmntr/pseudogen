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
        .replace('=', '-EQUALS-') \
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
        return '(' + typename(node) + ' ' + str(node) + ')'

def main():
    for l in sys.stdin:
        l = l.strip()
        if not l:
            print()
            sys.stdout.flush()
            continue
        parse = sqlparse.parse(l)
        parse = parse[0]
        parse = parse.tokens
        dump = makestr(parse)
        dump = dump.replace("(Token  )","")
        dump = dump.replace("(Token    )","" )
        dump = dump.replace("="," -EQUALS- " )
        dump = dump.replace("_","")
        dump = dump.replace("*", "-ALL-")
        print(dump)
        sys.stdout.flush()

if __name__ == '__main__':
    main()

