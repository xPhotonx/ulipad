#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
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
#   $Id$

from modules import Mixin
import wx
from mixins import DocumentBase
from mixins.Editor import TextEditor
from modules import common

class OutlinePage(wx.Panel, DocumentBase.DocumentBase, Mixin.Mixin):

    __mixinname__ = 'outlinepage'

    def __init__(self, parent, mainframe, filename, documenttype, **kwargs):
        self.initmixin()

        wx.Panel.__init__(self, parent, -1)
        DocumentBase.DocumentBase.__init__(self, parent, filename, documenttype, **kwargs)
        self.mainframe = mainframe
        self.pref = mainframe.pref

        box = wx.BoxSizer(wx.VERTICAL)

        #editor
        self.editor = TextEditor(self, self.mainframe.editctrl, 'outline://edit', self.documenttype)

        box.Add(self.editor, 1, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        self.opened = True
        
        self.editor.canopenfile = common.curry(canopenfile, self)
        self.editor.openfile = common.curry(openfile, self)
        self.editor.savefile = common.curry(savefile, self)
        self.editor.needcheckfile = False
        self.editor.cansavefileflag = False
        self.edirot.title = 'Outline'

def canopenfile(self, filename, documenttype='outline'):
    return False

def openfile(self, filename='', encoding='', delay=None, *args, **kwargs):
    self.title = tr('New Post')

def savefile(self, filename, encoding):
    self.callplugin('savefile', self, self.editor)
    
