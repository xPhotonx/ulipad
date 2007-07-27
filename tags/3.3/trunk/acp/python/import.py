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
