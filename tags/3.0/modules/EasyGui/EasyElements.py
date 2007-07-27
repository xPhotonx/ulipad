#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2005 limodou
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

import wx
from EasyUtils import *
import EasyBasicElements
from EasyGlobal import element_classes

class EasyElements(object):
    def __init__(self, elements, values={}, factor=1):
        self.elements = elements
        self.items = {}
        self.values = values
        self.factor = factor
        
    def addItems(self, sizer):
        number = len(self.elements)
        if not number:
            return
        if self.values:
            elements = self.getNewElements(self.values)
        else:
            elements = self.elements
            
        self.gbs = wx.GridBagSizer(2, 2)
        
        for i, item in enumerate(elements):
            kind, name, value, message, extern = item
            self.addItem(i, kind, name, value, message, extern)

        sizer.Add(self.gbs, self.factor, wx.EXPAND|wx.ALL, 2)
        self.gbs.AddGrowableCol(1)

    def getNewElements(self, values):
        new_elements = []
        for i, e in enumerate(self.elements):
            value = values.get(e[1], None)
            if value is not None:
                e = list(e)
                e[2] = value
                new_elements.append(tuple(e))
            else:
                new_elements.append(e)
        return new_elements

    def addItem(self, i, kind, name, value, message, extern):
        flag = wx.LEFT|wx.RIGHT
        try:
            klass = element_classes[kind]
        except:
            raise EasyException, "Cann't support this type [%s]" % kind
        obj = klass(self, value, message, extern)
        self.items[name] = obj
            
        if not obj.isLarge():
            self.gbs.Add(wx.StaticText(self, -1, message), (i, 0), flag=wx.ALIGN_CENTER_VERTICAL, border=2)
            self.gbs.Add(obj.getContainer(), (i, 1), flag=obj.getAlignFlag(flag), border=2)
        else:
            self.gbs.Add(obj.getContainer(), (i, 0), (1, 2), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=2)
            self.gbs.AddGrowableRow(i)

    def getValues(self):
        values = {}
        for key, obj in self.items.items():
            values[key] = obj.getValue()
        return values