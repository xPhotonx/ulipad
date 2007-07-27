#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   UliPad is free software; you can redistribute it and/or modify
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
#   $Id: PyParse.py 1616 2006-10-17 02:31:15Z limodou $


import tokenize # Python tokenizer
import token
import StringIO
import sets

class Node:
    def __init__(self, parent=None, name='', type='', info='', lineno=-1, span=[]):
        self.parent = parent
        self.name = name
        self.type = type
        self.lineno = lineno
        self.info = info
        if span:
            self.span = span
        else:
            self.span = [lineno]
        self.items = {}
        self.orders = []
        self.lines = []

    def set_lines(self, lines):
        self.lines = lines

    def __setitem__(self, name, value):
        self.items[name] = value
        self.orders.append(name)

    def __getitem__(self, name):
        try:
            return self.items[name]
        except:
            raise KeyError, name

    def items(self):
        for key in self.orders:
            yield key, self.items[key]

    def keys(self):
        return self.items.keys()

    def values(self):
        for key in self.orders:
            yield self.items[key]

    def get_text(self):
        obj = self
        while obj.parent:
            obj = obj.parent
        lines = obj.lines
        if len(self.span) == 1:
            return lines[self.span[0]-1]
        else:
            return '\n'.join(lines[self.span[0]-1:self.span[1]-1])

    def is_in(self, lineno):
        if len(self.span) == 2:
            return self.span[0] < lineno < self.span[1]
        else:
            return self.lineno == lineno

    def guess(self, lineno):
        node = []
        if self.is_in(lineno):
            node.append(self)
        for obj in self.values():
            if hasattr(obj, 'guess') and callable(obj.guess):
                node.extend(obj.guess(lineno))
        return node

    def __str__(self):
        s = []
        s.append("[name=%s,type=%s,span=%r,info=%s]" % (self.name, self.type, self.span, self.info))
#        for obj in self.values():
#            s.append(str(obj))
#        return '\n'.join(s)
        return ''.join(s)

def parseFile(filename):
    text = open(filename).read()
    return parseString(text)

def parseString(buf):
    stack = [] # stack of (class, indent) pairs

    f = StringIO.StringIO(buf)

    g = tokenize.generate_tokens(f.readline)

    root = Node()
    root.set_lines(buf.splitlines())
    func_nodes = root['function'] = Node(root)
    class_nodes = root['class'] = Node(root)
    import_nodes = root['import'] = Node(root)
    root['idens'] = {}
    idens = []

    last_node = None

    flag = False

    def close_span(stack, lineno):
        if stack:
            last_node = stack.pop(-1)[0]
            if last_node.type in ('class', 'function'):
                last_node.span.append(lineno)
    try:
        for tokentype, t, start, end, line in g:
            try:
                if tokentype == token.DEDENT:
                    lineno, thisindent = start
                    # close nested classes and defs
                    while stack and stack[-1][1] >= thisindent:
                        close_span(stack, lineno)
                elif t == 'def':
                    lineno, thisindent = start
                    # close previous nested classes and defs
                    while stack and stack[-1][1] >= thisindent:
                        close_span(stack, lineno)
                    tokentype, meth_name, start, end, line = g.next()
                    if tokentype != token.NAME:
                        continue # Syntax error
                    info = meth_name
                    put_list(idens, info)
                    while True: # get details
                        tokentype, t, start, end, line = g.next()
                        if t == ':':
                            break
                        if tokentype != tokenize.COMMENT:
                            if t == ',':
                                t = ', '
                            put_list(idens, t, [', '])
                            info += t
                    if stack:
                        obj = stack[-1][0]
                        if obj.type == 'class' or obj.type == 'function':
                            # it's a method
                            node = obj[meth_name] = Node(obj, meth_name, 'function', info, lineno)
                            stack.append((node, thisindent)) # Marker for nested fns
                        # else it's a nested def
                    else:
                        # it's a function
                        node = func_nodes[meth_name] = Node(func_nodes, meth_name, 'function', info, lineno)
                        stack.append((node, thisindent)) # Marker for nested fns
                elif t == 'class':
                    lineno, thisindent = start
                    # close previous nested classes and defs
                    while stack and stack[-1][1] >= thisindent:
                        close_span(stack, lineno)
                    tokentype, class_name, start, end, line = g.next()
                    if tokentype != token.NAME:
                        continue # Syntax error
                    info = class_name
                    put_list(idens, info)
                    while True: # get details
                        tokentype, t, start, end, line = g.next()
                        if t == ':':
                            break
                        if tokentype != tokenize.COMMENT:
                            if t == ',':
                                t = ', '
                            put_list(idens, t, [', '])
                            info += t
                    if stack:
                        obj = stack[-1][0]
                        if obj.type == 'class' or obj.type == 'function':
                            # it's a method
                            node = obj[class_name] = Node(obj, class_name, 'class', info, lineno)
                            stack.append((node, thisindent)) # Marker for nested fns
                    else:
                        node = class_nodes[class_name] = Node(class_nodes, class_name, 'class', info, lineno)
                        stack.append((node, thisindent))
                elif t == 'import' and start[1] == 0:
                    info = t + ' '
                    lineno, thisindent = start
                    while True:
                        tokentype, t, start, end, line = g.next()
                        if tokentype == token.NEWLINE or tokentype == tokenize.COMMENT:
                            break
                        if t == ',':
                            t = ', '
                        if t == 'as':
                            t = ' as '
                        put_list(idens, t, [', ', ' as'])
                        info += t
                    node = import_nodes[info] = Node(import_nodes, info, 'import', info, lineno)
                elif t == 'from' and start[1] == 0:
                    info = t + ' '
                    lineno, thisindent = start
                    while True:
                        tokentype, t, start, end, line = g.next()
                        if tokentype == token.NEWLINE or tokentype == tokenize.COMMENT:
                            break
                        if t == 'import':
                            t = ' import '
                        if t == ',':
                            t = ', '
                        put_list(idens, t, [' import ', ', '])
                        info += t
                    node = import_nodes[info] = Node(import_nodes, info, 'import', info, lineno)
                elif tokentype == token.NAME:
                    put_list(idens, t)
            except:
        #        raise
                pass
    except:
#        import traceback
#        traceback.print_exc()
        return root
    root['idens'] = idens
    return root

def put_list(alist, v, not_include=None):
    if not not_include or not v in not_include:
        if len(v) > 1 and not v in alist:
            alist.append(v)
def main():
    # Main program for testing.
    import sys
    file = sys.argv[1]

    s = parseFile(file)
    print 'import ......'
    imports = s['import']
    for value in imports.values():
        print value.lineno, value.info
    print 'functions ......'
    functions = s['function']
    for value in functions.values():
        print value.lineno, value.info, value.span
#        print value.get_text()
    print 'class ......'
    classes = s['class']
    for c in classes.values():
        print c.info, c.lineno
        for value in c.values():
            print ' '*4, value.lineno, value.info, value.span
#            print value.get_text()
    print 'identifers ......'
    for k, v in s['idens'].items():
        print '------', k
        print ' '.join(v)
    
    print 'guess ......'
    for i in s.guess(25):
        print i
    for i in s.guess(87):
        print i

if __name__ == "__main__":
    main()
