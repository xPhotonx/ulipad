import sys
import re
import inspect
import sets
import wx.py.introspect as intro
from modules.Debug import debug

INDENT = ' '*4
def pout(head, *args):
    if debug.is_debug():
        print head,
        for i in args:
            print i,
        print

getattributes = intro.getAttributeNames

namespace = {}

def get_calltip(win, word):
    if not hasattr(win, 'syntax_info') or not win.syntax_info:
        return []
    
    pout('-'*50)
    pout('get_calltip', word)
    
    flag, object = guessWordObject(win, word)

    pout(INDENT, 'ready to output:', flag, object)
    if object:
        if flag == 'obj':
            signature = getargspec(object)
            doc = object.__doc__
            return filter(None, [signature, doc])
        else:
            if object.type == 'function':
                return object.info
    pout(INDENT, 'return:', None)
    return None
    
def getWordObject(win, word=None, whole=None):
    if not word:
        word = getWord(win, whole=whole)
    try:
        return evaluate(win, word)
    except:
#        error.traceback()
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
#        error.traceback()
        pass
    try:
        return inspect.formatargspec(*inspect.getargspec(func))
    except:
#        error.traceback()
        pass
    try:
        return inspect.formatargvalues(*inspect.getargvalues(func))
    except:
#        error.traceback()
        return ''

def import_document(win):
    root = win.syntax_info
    lineno = win.GetCurrentLine() + 1
    result = root.get_imports(lineno)
    pout('import_document')
    for importline, line in result:
        pout('import', importline, line)
        if importline.startswith('from'):
            try:
                exec(importline) in namespace
            except:
                #error.traceback()
                pass
        elif importline.startswith('import'):
            try:
                exec(importline) in namespace
            except:
#                error.traceback()
                pass

def autoComplete(win, word=None):
    if not word:
        word = getWord(win)
    words = getAutoCompleteList(win, word)
    if words:
        return words
    else:
        if not word.startswith('self.'):
            words = getWords(win, word)
            return words
    
def getAutoCompleteList(win, command=''):
    if not hasattr(win, 'syntax_info') or not win.syntax_info:
        return []

    pout('-'*50)
    pout('getAutoCompleteList', command)

    v = guessWordObject(win, command)
    flag, object = v
    pout(INDENT, 'ready to output:', flag, object)
    if object:
        if flag == 'obj':
            return getattributes(object)
        else:
            if object.type == 'class':
                return getClassAttributes(win, object)
    pout(INDENT, 'return:', [])
    return []

def guessWordObject(win, command):
    root = win.syntax_info
    attributes = []
    # Get the proper chunk of code from the command.
    flag = None
    object = None
    while command.endswith('.'):
        command = command[:-1]
    
    lineno = win.GetCurrentLine() + 1
    attributes = command.split('.')
    if attributes[0] == 'self' and len(attributes) == 1:    #process self.
        cls = root.guess_class(lineno)
        if cls:
            return 'source', cls
    elif attributes[0] == 'self' and len(attributes) > 1:   #process self.a. then treat self.a as a var
        key = attributes[0] + '.' + attributes[1]
        del attributes[0]
        attributes[0] = key
    else:
        result = root.guess_type(lineno, command)
        if result:
            attributes = [command]
        
   
    #deal first word
    firstword = attributes[0]
    del attributes[0]
    pout(INDENT, 'attributes:', attributes, 'firstword:', firstword)
    result = root.guess_type(lineno, firstword)
    pout(INDENT, 'guess [%s] result:' % firstword, result)
    if result:
        t, v = result
        pout(INDENT, 'begin try_get_obj_type:', t, v, attributes)
        flag, object = try_get_obj_type(win, t, v, lineno)
        pout(INDENT, 'result:', flag, object, attributes)
        if flag == 'source' or attributes:
            #deal other rest
            flag, object = try_get_obj_attribute(win, flag, object, attributes)
            pout(INDENT, 'result:', flag, 'object=', object)
    else:
        if firstword.startswith('self.'):
            word = firstword.split('.', 1)[1]
            cls = root.guess_class(lineno)
            if cls:
                for b in cls.bases:
                    obj = getObject(win, b)
                    if obj:
                        if hasattr(obj, word):
                            object = getattr(obj, word)
                            flag = 'obj'
        else:
            flag = 'obj'
            object = getObject(win, firstword)

    return flag, object

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

re_match = re.compile('^\s*from\s+')
def getObject(win, word):
    pout(INDENT, 'getObject:', word)
    object = None
    line = win.GetLine(win.GetCurrentLine())
    if re_match.match(line):
        if sys.modules.has_key(word):
            object = sys.modules[word]
        else:
            try:
                object = __import__(word, [], [], [''])
            except:
                pass
    else:
        try:
            object = eval(word, namespace)
        except:
            import_document(win)
            try:
                object = eval(word, namespace)
            except:
                pass
    pout(INDENT, 'getObject result [%s]:' % word, object)
    return object
    
def getClassAttributes(win, cls):
    s = sets.Set([])
    if cls:
        root = win.syntax_info
        s = sets.Set(cls.locals)
        for b in cls.bases:
            c = root.search_name(cls.lineno, b)
            if c:
                cls = root.guess_class(c[2])
                if cls:
                    s.update(cls.locals)
            else:
                obj = getObject(win, b)
                if obj:
                    s.update(getattributes(obj))
    return list(s)

def try_get_obj_type(win, t, v, lineno):
    pout(INDENT, "try_get_obj_type", t, v, lineno)
    root = win.syntax_info
    flag = 'obj'
    node = None
    if t in ('class', 'function'):
        node = v
        flag = 'source'
#        r = root.search_name(lineno, v)
#        if r:
#            cls = root.guess_class(r[2], v)
#            if cls:
#                node = cls
#                flag = 'source'
#    elif t == 'function':
#        r = root.search_name(lineno, v)
#        if r:
#            func = root.guess_function(r[2], v)
#            if func:
#                node = func
#                flag = 'source'
    elif t not in ('reference', 'import'):
        node = v
    else:
        node = getObject(win, v)
    return flag, node
    
def try_get_obj_attribute(win, flag, object, attributes):
    if not attributes:
        return flag, object
    root = win.syntax_info
    if object:
        if flag == 'obj':
            for o in attributes:
                if hasattr(object, o):
                    object = getattr(object, o)
                else:
                    object = None
                    break
        else:
            o = attributes[0]
            del attributes[0]
            r = object.get_local_name(o)
            if r:
                t, v, line = r
                if t == 'reference':
                    gt = root.guess_type(line, v)
                    if gt:
                        t, v = gt
                
                flag, object = try_get_obj_type(win, t, v, line)
                if attributes:
                    return try_get_obj_attribute(win, flag, object, attributes)
                else:
                    return flag, object
            else:
                for b in object.bases:
                    c = root.search_name(object.lineno, b)
                    if c:
                        cls = root.guess_class(c[2])
                        gr = cls.get_local_name(o)
                        if gr:
                           t, v, line = gr
                           if t == 'reference':
                               gt = root.guess_type(line, v)
                               if gt:
                                   t, v = gt
                           flag, object = try_get_obj_type(win, t, v, line)
                           if attributes:
                               return try_get_obj_attribute(win, flag, object, attributes)
                           else:
                               return flag, object
                    else:
                        flag = 'obj'
                        obj = getObject(win, b)
                        if hasattr(obj, o):
                            return flag, getattr(obj, o)
                
                object = None
    return flag, object

#getlocals
import __builtin__
import keyword
import types

def default_identifier(win):
    return keyword.kwlist + [x for x in dir(__builtin__) if isinstance(getattr(__builtin__, x), types.BuiltinFunctionType)] + ['None', 'as', 'True', 'False', 'self', 'file', 'str', 'int', 'unicode', 'list', 'dict', 'tuple', 'bool', 'float']

def get_locals(win, lineno, word):
    root = win.syntax_info
    if '.' in word:
        if word.endswith('.'):
            word = word[:-1]
            length = 0
        else:
            word, ext = word.rsplit('.', 1)
            length = len(ext)
        return length, getAutoCompleteList(win, word)
    else:
        r = root.get_locals(lineno)
        d = {}
        for i in r + default_identifier(win):
            if len(i) <= 1:
                continue
            k = i[0].upper()
            s = d.setdefault(k, [])
            if i not in s:
                s.append(i)
        for k, v in d.items():
            d[k].sort(lambda x, y:cmp(x.upper(), y.upper()))
            
        if len(word) > 0 and d.has_key(word[0].upper()):
            words = d.get(word[0].upper(), [])
            if words:
                for i in words:
                    if i.startswith(word):
                        return len(word), words
        
        return None, []