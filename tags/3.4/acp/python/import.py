from modules.Debug import error
import sys
import re

re_as = re.compile('\s+as(\s+|$)')
re_match = re.compile('import\s*$|,\s*$')
def fromimport(win, matchobj):
    n = {}
    try:
        b = re_as.search(matchobj.group())
        if b:
            return 'blank', ''
        b = re_match.search(matchobj.group())
        if not b:
            return 'blank', ''
        module = matchobj.groups()[0]
        if sys.modules.has_key(module):
            keys = dir(sys.modules[module])
        else:
            exec('import ' + module) in n
            keys = dir(sys.modules[module])
        return 'append', keys
    except:
        error.error('Execute code error: import ' + matchobj.groups()[0])
        error.traceback()
        return 'blank', ''

import __builtin__
import keyword
import types

def default_identifier(win):
    return keyword.kwlist + [x for x in dir(__builtin__) if isinstance(getattr(__builtin__, x), types.BuiltinFunctionType)] + ['None', 'as', 'True', 'False', 'self']

import import_utils
def calltip(win, word):
    obj = import_utils.getWordObject(win, word)
    if obj:
        signature = import_utils.getargspec(obj)
        doc = obj.__doc__
        return filter(None, [signature, doc])

def autodot(win, word):
    return import_utils.autoComplete(win, word)

def analysis(win):
    from modules import PyParse
    root = PyParse.parseString(win.getRawText())
    win.syntax_info = root
    