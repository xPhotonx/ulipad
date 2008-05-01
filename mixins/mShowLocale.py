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
#   $Id: mShowLocale.py 1566 2006-10-09 04:44:08Z limodou $

__doc__ = 'show document locale in statusbar'

from modules import Mixin

def on_document_enter(win, document):
    if document.edittype == 'edit':
        win.mainframe.SetStatusText(win.document.locale, 'coding')
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def fileopentext(win, stext):
    win.mainframe.SetStatusText(win.locale, 'coding')
Mixin.setPlugin('editor', 'openfiletext', fileopentext)

def savefiletext(win, stext):
    win.mainframe.SetStatusText(win.locale, 'coding')
Mixin.setPlugin('editor', 'savefiletext', savefiletext)

def afteropenfile(win, filename):
    win.mainframe.SetStatusText(win.locale, 'coding')
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)
