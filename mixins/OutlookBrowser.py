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
#   $Id: OutlookBrowser.py 1472 2006-08-24 02:15:23Z limodou $

import wx
from modules import common
from modules import makemenu
from modules import Mixin

class OutlookBrowser(wx.Panel, Mixin.Mixin):

    __mixinname__ = 'outlookbrowser'

    popmenulist = []

    def __init__(self, parent, editor):
        self.initmixin()

        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.editor = editor
        
        self.activeflag = False

        psizer = wx.BoxSizer(wx.VERTICAL)
        psizer.Add(self, 1, wx.EXPAND)
        self.parent.SetSizer(psizer)
        self.parent.SetAutoLayout(True)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.imagelist = wx.ImageList(16, 16)

        #add share image list
        self.imagefilenames = {}
        self.imageids = {}
        self.callplugin('add_images', self.imagefilenames)
        for name, imagefile in self.imagefilenames.items():
            self.add_image(name, imagefile)

        style = wx.TR_SINGLE|wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_TWIST_BUTTONS
        if wx.Platform == '__WXMSW__':
            style = style | wx.TR_ROW_LINES
        elif wx.Platform == '__WXGTK__':
            style = style | wx.TR_NO_LINES

        self.tree = wx.TreeCtrl(self, -1, style = style)
        self.tree.SetImageList(self.imagelist)

        self.sizer.Add(self.tree, 1, wx.EXPAND)
        self.root = self.tree.AddRoot('OutlookBrowser')

        self.nodes = {}
        self.ID = 1

#        wx.EVT_TREE_SEL_CHANGING(self.tree, self.tree.GetId(), self.OnChanging)
        wx.EVT_TREE_SEL_CHANGED(self.tree, self.tree.GetId(), self.OnChanged)
#        wx.EVT_TREE_BEGIN_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnBeginChangeLabel)
#        wx.EVT_TREE_END_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnChangeLabel)
        wx.EVT_TREE_ITEM_ACTIVATED(self.tree, self.tree.GetId(), self.OnSelected)
#        wx.EVT_TREE_ITEM_RIGHT_CLICK(self.tree, self.tree.GetId(), self.OnRClick)
#        wx.EVT_RIGHT_UP(self.tree, self.OnRClick)
        wx.EVT_TREE_DELETE_ITEM(self.tree, self.tree.GetId(), self.OnDeleteItem)
#        wx.EVT_LEFT_DCLICK(self.tree, self.OnDoubleClick)
#        wx.EVT_TREE_ITEM_EXPANDING(self.tree, self.tree.GetId(), self.OnExpanding)
        wx.EVT_LEFT_DOWN(self, self.OnLeftDown)

        #add init process
        self.callplugin('init', self)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

        self.popmenus = None

    def OnUpdateUI(self, event):
        self.callplugin('on_update_ui', self, event)

    def show(self):
        self.activeflag = True
        self.tree.Freeze()
        self.tree.DeleteChildren(self.root)

        #call plugin
        self.callplugin('parsetext', self, self.editor)
        self.tree.Thaw()
        self.activeflag = False

    def addnode(self, parent, caption, imagenormal, imageexpand=None, data=None):
        if not parent:
            parent = self.root
        obj = self.tree.AppendItem(parent, caption)
        _id = self.getid()
        self.tree.SetPyData(obj, _id)
        self.nodes[_id] = data
        if imagenormal > -1:
            self.tree.SetItemImage(obj, imagenormal, wx.TreeItemIcon_Normal)
        if imageexpand > -1:
            self.tree.SetItemImage(obj, imageexpand, wx.TreeItemIcon_Expanded)
        if parent!= self.root and not self.tree.IsExpanded(parent):
            self.tree.Expand(parent)
        return _id, obj

    def get_cur_node(self):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        _id = self.tree.GetPyData(item)
        return item, self.nodes.get(_id, None)

    def get_node(self, item):
        if not self.is_ok(item): return
        _id = self.tree.GetPyData(item)
        return self.nodes.get(_id, None)

    def getid(self):
        _id = self.ID
        self.ID += 1
        return _id

    def OnCloseWin(self):
        for klass in self.processors.values():
            if hasattr(klass, 'OnOutlookBrowserClose'):
                klass.OnOutlookBrowserClose()

    def OnChangeLabel(self, event):
        item = event.GetItem()
        if not self.is_ok(item): return
        if not self.execplugin('on_change_label', self, item, event.GetLabel()):
            event.Veto()

    def OnSelected(self, event):
        item = event.GetItem()
        if not self.is_ok(item): return
        self.callplugin('on_selected', self, item)

    def OnExpanding(self, event):
        item = event.GetItem()
        if not self.is_ok(item): return
        if not self.execplugin('on_expanding', self, item):
            event.Skip()

    def OnRClick(self, event):
        other_menus = []
        if self.popmenus:
            self.popmenus.Destroy()
            self.popmenus = None
        self.callplugin('other_popup_menu', self, other_menus)
        import copy
        if other_menus:
            pop_menus = copy.deepcopy(OutlookBrowser.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(OutlookBrowser.popmenulist)
        self.popmenus = pop_menus = makemenu.makepopmenu(self, pop_menus)

        self.tree.PopupMenu(pop_menus, event.GetPosition())

    def OnDeleteItem(self, event):
        item = event.GetItem()
        if self.is_ok(item):
            try:
                del self.nodes[self.tree.GetPyData(item)]
            except:
                pass
        event.Skip()

    def OnBeginChangeLabel(self, event):
        item = event.GetItem()
        if not self.is_ok(item): return
        if not self.execplugin('on_begin_change_label', self, item):
            event.Veto()
            return
        else:
            event.Skip()

    def is_first_node(self, item):
        parent = self.tree.GetItemParent(item)
        return parent == self.root

    def OnDoubleClick(self, event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if flags in (wx.TREE_HITTEST_NOWHERE, wx.TREE_HITTEST_ONITEMRIGHT,
            wx.TREE_HITTEST_ONITEMLOWERPART, wx.TREE_HITTEST_ONITEMUPPERPART):
            for item in self.getTopObjects():
                self.tree.Collapse(item)
        else:
            if self.tree.GetChildrenCount(item) == 0:
                if not self.callplugin('on_expanding', self, item):
                    event.Skip()
            else:
                event.Skip()

    def OnLeftDown(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if self.is_ok(item):
            if item == self.GetSelection():
                self.SelectItem(self.GetSelection(), False)
                wx.CallAfter(self.SelectItem, item, True)
                return
        event.Skip()

    def getTopObjects(self):
        objs = []
        child, cookie = self.tree.GetFirstChild(self.root)
        while child.IsOk():
            objs.append(child)
            child, cookie = self.tree.GetNextChild(self.root, cookie)
        return objs

    def OnMenu(self, event):
        self.callplugin('on_menu', self, event.GetId())

    def EditLabel(self, item):
        wx.CallAfter(self.tree.EditLabel, item)

    def OnChanged(self, event):
        item = event.GetItem()
        lineno = self.get_node(item)
        if self.editor and not self.activeflag:
            wx.CallAfter(self.editor.goto, lineno)

    def OnChanging(self, event):
        item = event.GetOldItem()
        if not self.is_ok(item): return
        if not self.execplugin('on_changing', self, item):
            event.Skip()

    def reset_cur_item(self):
        item = self.tree.GetSelection()
        if self.is_ok(item):
            self.tree.Freeze()
            self.tree.CollapseAndReset(item)
            self.tree.Thaw()
            self.execplugin('on_expanding', self, item)

    def get_image_id(self, name):
        return self.imageids.get(name, -1)

    def add_image(self, name, imagefile):
        if not self.imagefilenames.has_key(name):
            self.imagefilenames[name] = imagefile
        if not self.imageids.has_key(name):
            image = common.getpngimage(imagefile)
            self.imageids[name] = self.imagelist.Add(image)

    def is_ok(self, item):
        return item.IsOk() and item != self.root
