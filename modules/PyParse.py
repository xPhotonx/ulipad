#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id: PyParse.py 475 2006-01-16 09:50:28Z limodou $


import tokenize # Python tokenizer
import token
import StringIO

# each Python class is represented by an instance of this class
class Class:
    '''Class to represent a Python class.'''
    def __init__(self, name, info, lineno):
        self.name = name
        self.methods = {}
        self.lineno = lineno
        self.info = info

    def addmethod(self, name, info, lineno):
        self.methods[name] = (info, lineno)

def parseFile(filename):
    text = open(filename).read()
    return parseString(text)

def parseString(string):
    # Initialize the dict for this module's contents
    dict = {'class':{}, 'function':{}, 'import':[]}

    stack = [] # stack of (class, indent) pairs

    f = StringIO.StringIO(string)

    g = tokenize.generate_tokens(f.readline)

    try:
        for tokentype, t, start, end, line in g:
            if tokentype == token.DEDENT:
                lineno, thisindent = start
                # close nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    del stack[-1]
            elif t == 'def':
                lineno, thisindent = start
                # close previous nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    del stack[-1]
                tokentype, meth_name, start, end, line = g.next()
                if tokentype != token.NAME:
                    continue # Syntax error
                info = meth_name
                while True: # get details
                    tokentype, t, start, end, line = g.next()
                    if t == ':':
                        break
                    if tokentype != tokenize.COMMENT:
                        if t == ',':
                            t = ', '
                        info += t
                if stack:
                    cur_class = stack[-1][0]
                    if isinstance(cur_class, Class):
                        # it's a method
                        cur_class.addmethod(meth_name, info, lineno)
                    # else it's a nested def
                else:
                    # it's a function
                    dict['function'][meth_name] = (info, lineno)
                stack.append((None, thisindent)) # Marker for nested fns
            elif t == 'class':
                lineno, thisindent = start
                # close previous nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    del stack[-1]
                tokentype, class_name, start, end, line = g.next()
                if tokentype != token.NAME:
                    continue # Syntax error
                info = class_name
                while True: # get details
                    tokentype, t, start, end, line = g.next()
                    if t == ':':
                        break
                    if tokentype != tokenize.COMMENT:
                        if t == ',':
                            t = ', '
                        info += t
                cur_class = Class(class_name, info, lineno)
                if not stack:
                    dict['class'][class_name] = cur_class
                stack.append((cur_class, thisindent))
            elif t == 'import' and start[1] == 0:
                info = t + ' '
                lineno, thisindent = start
                while True:
                    tokentype, t, start, end, line = g.next()
                    if tokentype == token.NEWLINE:
                        break
                    if t == ',':
                        t = ', '
                    info += t
                dict['import'].append((info, lineno))
            elif t == 'from' and start[1] == 0:
                info = t + ' '
                lineno, thisindent = start
                while True:
                    tokentype, t, start, end, line = g.next()
                    if tokentype == token.NEWLINE:
                        break
                    if t != ',':
                        t += ' '
                    info += t
                dict['import'].append((info, lineno))
    except:
        pass

    return dict

def main():
    # Main program for testing.
    import sys
    file = sys.argv[1]

    s = parseFile(file)
    print 'import ......'
    imports = s['import']
    for info, lineno in imports:
        print lineno, info
    print 'functions ......'
    functions = s['function'].values()
    for info, lineno in functions:
        print lineno, info
    print 'class ......'
    classes = s['class'].values()
    for c in classes:
        print c.info, c.lineno
        for info, lineno in c.methods.values():
            print '    ', lineno, info

if __name__ == "__main__":
    main()