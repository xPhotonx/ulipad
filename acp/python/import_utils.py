import os
import sys
import re
import inspect
import sets
from modules.Debug import error
from modules import common

namespace = {}

def getWordObject(win, word=None, whole=None):
    if not word:
        word = getWord(win, whole=whole)
    try:
        return evaluate(win, word)
    except:
        error.traceback()
        return None

def getWord(win, whole=None):
    pos=win.GetCurrentPos()
    line = win.GetCurrentLine()
    linePos=win.PositionFromLine(line)
    txt = win.GetLine(line)
    start=win.WordStartPosition(pos,1)
    i = start - 1
    while i >= 0:
        if win.getChar(i) in win.mainframe.getWordChars() + '.':
            start -= 1
            i -= 1
        else:
            break
    if whole:
        end=win.WordEndPosition(pos,1)
    else:
        end=pos
    return txt[start-linePos:end-linePos]


def evaluate(win, word):
    try:
        obj = eval(word, namespace)
        return obj
    except:
        import_document(win)
        try:
            obj = eval(word, namespace)
            return obj
        except:
            return None

def getargspec(func):
    """Get argument specifications"""
    try:
        func=func.im_func
    except:
        error.traceback()
        pass
    try:
        return inspect.formatargspec(*inspect.getargspec(func))
    except:
        error.traceback()
        pass
    try:
        return inspect.formatargvalues(*inspect.getargvalues(func))
    except:
        error.traceback()
        return ''

def import_document(win):
    dir = common.encode_string(os.path.dirname(win.filename))
    if dir not in sys.path:
        sys.path.insert(0, dir)
    r = re.compile(r'^\s*from\s+.*$|^\s*import\s+.*$', re.M)
    result = r.findall(win.GetText())
    result = [s.strip() for s in result]
    for line in result:
        if line.startswith('from'):
            try:
                exec(line) in namespace
            except:
                error.traceback()
        elif line.startswith('import'):
            try:
                exec(line) in namespace
            except:
                error.traceback()

def autoComplete(win, word=None):
    import wx.py.introspect as intro

    if not word:
        word = getWord(win)

    words = getAutoCompleteList(intro, win, word)
    if words:
        return words
    else:
        words = getWords(win, word)
        return words
    
re_match = re.compile('^\s*from\s+')
def getAutoCompleteList(modules, win, command='', includeMagic=1,
                        includeSingle=1, includeDouble=1):
    """Return list of auto-completion options for command.

    The list of options will be based on the locals namespace."""
    attributes = []
    # Get the proper chunk of code from the command.
    object = None
    if command.endswith('.'):
        root = command[:-1]
    else:
        root = command
    line = win.GetLine(win.GetCurrentLine())
    if re_match.match(line):
        if sys.modules.has_key(root):
            object = sys.modules[root]
        else:
            try:
                object = __import__(root, [], [], [''])
            except:
                error.error("Can't load the module " + root)
                error.traceback()
                pass
    else:
        try:
            object = eval(root, namespace)
        except:
            error.traceback()
            import_document(win)
            try:
                object = eval(root, namespace)
            except:
                error.traceback()
                pass
    if object:
        attributes = modules.getAttributeNames(object, includeMagic,
                                       includeSingle, includeDouble)
    return attributes

def getWords(win, word=None, whole=None):
    if not word:
        word = getWord(whole=whole)
    if not word:
        return []
    else:
        word = word.replace('.', r'\.')
        words = list(sets.Set([x for x in re.findall(r"\b" + word + r"(\w+)\b", win.GetText())]))
        words.sort(lambda x, y:cmp(x.upper(), y.upper()))
        return words
