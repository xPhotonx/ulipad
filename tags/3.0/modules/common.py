#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
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
#	$Id: common.py 93 2005-10-11 02:51:02Z limodou $

"""Used to define commonly functions.
"""
import locale
import types
import os
import os.path
import wx
import sys
import codecs
import GenericDispatch

defaultencoding = locale.getdefaultlocale()[1]
if not defaultencoding:
    defaultencoding = 'utf-8'
try:
    codecs.lookup(defaultencoding)
except:
    defaultencoding = 'utf-8'
    
defaultfilesystemencoding = sys.getfilesystemencoding()
if not defaultfilesystemencoding:
    defaultfilesystemencoding = 'ansii'
try:
    codecs.lookup(defaultfilesystemencoding)
except:
    defaultfilesystemencoding = 'ansii'

def unicode_abspath(path):
    """convert path to unicode
    """
    return decode_string(os.path.abspath(path), defaultfilesystemencoding)

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
    GenericDispatch.Dispatch(mainframe, mainframe.SetStatusText, message, 0)

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
        fname, ext = os.path.splitext(decode_string(filename))
        if ext.lower() == '.png':
            f = filename
        else:
            f = fname + '.png'
            if not os.path.exists(f):
                f = filename
        return wx.Image(f).ConvertToBitmap()
    else:
        return filename
    
