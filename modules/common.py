#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
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
#   $Id: common.py 1599 2006-10-12 09:04:00Z limodou $

"""Used to define commonly functions.
"""
import locale
import types
import os
import wx
import sys
import codecs
import Globals
import time

try:
    defaultencoding = locale.getdefaultlocale()[1]
except:
    defaultencoding = None

if not defaultencoding:
    defaultencoding = 'utf-8'
try:
    codecs.lookup(defaultencoding)
except:
    defaultencoding = 'utf-8'

try:
    defaultfilesystemencoding = sys.getfilesystemencoding()
except:
    defaultfilesystemencoding = None

if not defaultfilesystemencoding:
    defaultfilesystemencoding = 'ascii'
try:
    codecs.lookup(defaultfilesystemencoding)
except:
    defaultfilesystemencoding = 'ascii'

def unicode_abspath(path):
    """convert path to unicode
    """
    return decode_string(os.path.abspath(path), defaultfilesystemencoding)

def uni_join_path(*path):
    return decode_string(os.path.join(*path), defaultfilesystemencoding)

def uni_work_file(filename):
    return uni_join_path(Globals.workpath, filename)

def decode_string(string, encoding=None):
    """convert string to unicode

    If the second parameter encoding is omit, the default locale will be used.
    """
    if not encoding:
        encoding = defaultencoding
    if not isinstance(string, types.UnicodeType):
        return unicode(string, encoding)
    else:
        return string

def encode_string(string, encoding=None):
    """convert unicode to string

    If the second parameter encoding is omit, the default locale will be used.
    """
    if not encoding:
        encoding = defaultencoding
    if isinstance(string, types.UnicodeType):
        return string.encode(encoding)
    else:
        return string

def get_app_filename(mainframe, filename):
    """concatenate app.workpath and filename
    """
    return decode_string(os.path.join(mainframe.app.workpath, filename), defaultfilesystemencoding)

def showerror(win, errmsg):
    """show error message dialog

    win is parent window
    """
    if not isinstance(errmsg, types.StringTypes):
        errmsg = str(errmsg)
    wx.MessageDialog(win, errmsg, tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()

def showmessage(win, message):
    """show message dialog

    win is parent window
    """
    if not isinstance(message, types.StringTypes):
        message = str(message)
    wx.MessageDialog(win, message, tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()

def setmessage(mainframe, message):
    """show message in main frame statusbar

    mainframe is main frame
    """
#    GenericDispatch.Dispatch(mainframe, mainframe.SetStatusText, message, 0)
    wx.CallAfter(mainframe.SetStatusText, message, 0)

def getHomeDir():
    ''' Try to find user's home directory, otherwise return current directory.'''
    try:
        path1=os.path.expanduser("~")
    except:
        path1=""
    try:
        path2=os.environ["HOME"]
    except:
        path2=""
    try:
        path3=os.environ["USERPROFILE"]
    except:
        path3=""

    if os.path.exists(path1): return path1
    if os.path.exists(path2): return path2
    if os.path.exists(path3): return path3
    return os.getcwd()

def uni_prt(a, encoding=None):
    s = []
    if not encoding:
        encoding = defaultencoding
    if isinstance(a, (list, tuple)):
        if isinstance(a, list):
            s.append('[')
        else:
            s.append('(')
        for i, k in enumerate(a):
            s.append(uni_prt(k, encoding))
            if i<len(a)-1:
                s.append(', ')
        if isinstance(a, list):
            s.append(']')
        else:
            s.append(')')
    elif isinstance(a, dict):
        for i, k in enumerate(a.items()):
            key, value = k
            s.append('{%s: %s}' % (uni_prt(key, encoding), uni_prt(value, encoding)))
            if i<len(a.items())-1:
                s.append(', ')
    elif isinstance(a, str):
        s.append("%s" %a)
    elif isinstance(a, unicode):
        s.append("%s" % a.encode(encoding))
    else:
        s.append(str(a))
    return ''.join(s)

def getpngimage(filename):
    if isinstance(filename, (str, unicode)):
        if not os.path.exists(filename) and not os.path.isabs(filename):
            filename = os.path.join(Globals.workpath, filename)
        fname, ext = os.path.splitext(decode_string(filename))
        if ext.lower() == '.ico':
            icon = wx.Icon(filename, wx.BITMAP_TYPE_ICO, 16, 16)
            bitmap = wx.EmptyBitmap(16, 16)
            bitmap.CopyFromIcon(icon)
            return bitmap
        if ext.lower() == '.png':
            f = filename
        else:
            f = fname + '.png'
            if not os.path.exists(f):
                f = filename
        image = wx.Image(f)
        if image.Ok():
            return image.ConvertToBitmap()
        else:
            return filename
    else:
        return filename

def getProjectName(filename):
    path = getProjectHome(filename)
    #found _project
    from modules import dict4ini
    ini = dict4ini.DictIni(os.path.join(path, '_project'))
    name = ini.default.get('projectname', [])
    if not isinstance(name, list):
        name = [name]
    return name

def getCurrentPathProjectName(filename):
    path = getCurrentPathProjectHome(filename)
    #found _project
    from modules import dict4ini
    ini = dict4ini.DictIni(os.path.join(path, '_project'))
    name = ini.default.get('projectname', [])
    if not isinstance(name, list):
        name = [name]
    return name

def getCurrentPathProjectHome(filename):
    if not filename:
        return ''
    if os.path.isfile(filename):
        path = os.path.dirname(os.path.abspath(filename))
    else:
        path = filename
    if not os.path.exists(os.path.join(path, '_project')):
        path = ''
    return path

def getProjectHome(filename):
    if not filename:
        return ''
    if os.path.isfile(filename):
        path = os.path.dirname(os.path.abspath(filename))
    else:
        path = filename
    while not os.path.exists(os.path.join(path, '_project')):
        newpath = os.path.dirname(path)
        if newpath == path: #not parent path, so not found _project
            return ''
        path = newpath
    return path

def getProjectFile(filename):
    if not filename:
        return ''
    if os.path.isfile(filename):
        path = os.path.dirname(os.path.abspath(filename))
    else:
        path = filename
    while not os.path.exists(os.path.join(path, '_project')):
        newpath = os.path.dirname(path)
        if newpath == path: #not parent path, so not found _project
            return ''
        path = newpath
    return os.path.join(path, '_project')

def getConfigPathFile(f):
    filename = os.path.join(Globals.workpath, f)
    if os.path.exists(filename):
        return filename
    filename = os.path.join(Globals.confpath, f)
    if os.path.exists(filename):
        return filename
    return ''

def uni_file(filename):
    if isinstance(filename, str):
        return decode_string(filename, defaultfilesystemencoding)
    else:
        return filename

def normal_file(filename):
    if isinstance(filename, unicode):
        return encode_string(filename, defaultfilesystemencoding)
    else:
        return filename

def print_time(name, debug):
    if debug:
        print name, time.strftime("%H:%M:%S")


def getCurrentDir(filename):
    if os.path.isfile(filename):
        dir = os.path.dirname(filename)
    else:
        dir = filename
    return dir

def show_in_message_window(text):
    win = Globals.mainframe
    win.createMessageWindow()
    win.panel.showPage(tr('Message'))
    win.messagewindow.SetText(text)

def note(text):
    Globals.mainframe.statusbar.note(text)

def warn(text):
    Globals.mainframe.statusbar.warn(text)

def curry(*args, **kwargs):
    def _curried(*moreargs, **morekwargs):
        return args[0](*(args[1:]+moreargs), **dict(kwargs.items() + morekwargs.items()))
    return _curried

def set_acp_highlight(ini, suffix, acps, highlight):
    if acps:
        s = ini.acp.get(suffix, [])
        if not isinstance(s, list):
            s = [s]
        if not isinstance(acps, list):
            acps = [acps]
        for i in acps:
            if not i in s:
                s.append(i)
        ini.acp[suffix] = s
    if highlight:
        ini.highlight[suffix] = highlight
    
def remove_acp_highlight(ini, suffix, acps, highlight):
    if acps:
        s = ini.acp.get(suffix, [])
        if not isinstance(s, list):
            s = [s]
        if not isinstance(acps, list):
            acps = [acps]
        for i in acps:
            if i in s:
                s.remove(i)
        if not s:
            del ini.acp[suffix]
        else:
            ini.acp[suffix] = s
    if highlight:
        del ini.highlight[suffix]
