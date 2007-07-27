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
#   $Id$

import wx
import os.path
import copy
from modules import common
from modules import makemenu
from modules import Mixin
from modules.Debug import error
from elementtree.ElementTree import ElementTree, Element, SubElement
from elementtree.SimpleXMLWriter import XMLWriter

class OutlineWindow(wx.Panel, Mixin.Mixin):

    __mixinname__ = 'outline'

    popmenulist = [ (None,
        [
            (100, 'IDPM_CUT', tr('Cut')+'\tCtrl+X', wx.ITEM_NORMAL, 'OnOutlineCut', ''),
            (110, 'IDPM_COPY', tr('Copy')+'\tCtrl+C', wx.ITEM_NORMAL, 'OnOutlineCopy', ''),
            (120, 'IDPM_PASTE', tr('Paste')+'\tCtrl+V', wx.ITEM_NORMAL, 'OnOutlinePaste', ''),
            (130, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (140, 'IDPM_NEW', tr('New Outline'), wx.ITEM_NORMAL, 'OnNewOutline', ''),
            (150, 'IDPM_OPEN', tr('Open Outline'), wx.ITEM_NORMAL, 'OnOpenOutline', ''),
            (160, 'IDPM_RECENT', tr('Recently Outlines'), wx.ITEM_NORMAL, '', ''),
            (170, 'IDPM_SAVE', tr('Save Outline'), wx.ITEM_NORMAL, 'OnSaveOutline', ''),
            (180, 'IDPM_SAVEAS', tr('Save Outline As...'), wx.ITEM_NORMAL, 'OnSaveAsOutline', ''),
            (190, 'IDPM_CLOSE', tr('Close Outline'), wx.ITEM_NORMAL, 'OnCloseOutline', ''),
            (200, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (210, 'IDPM_NEW_FOLDER', tr('New Folder'), wx.ITEM_NORMAL, 'OnNewFolder', ''),
            (220, 'IDPM_NEW_NODE', tr('New Node'), wx.ITEM_NORMAL, 'OnNewNode', ''),
        ]),
        ('IDPM_RECENT',
        [
            (160, 'IDPM_RECENT_OUTLINES', tr('(empty)'), wx.ITEM_NORMAL, '', ''),
        ]),
    ]

    def __init__(self, parent, mainframe):
        self.initmixin()
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.mainframe = mainframe
        self.pref = mainframe.pref

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.outlineimagelist = imagelist = wx.ImageList(16, 16)

        #add share image list
        self.imagefiles = {}
        self.imageids = {}
        self.callplugin('add_images', self.imagefiles)
        for name, imagefile in self.imagefiles.items():
            self.add_image(name, imagefile)
        
        style = wx.TR_EDIT_LABELS|wx.TR_SINGLE|wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_TWIST_BUTTONS
        if wx.Platform == '__WXMSW__':
            style = style | wx.TR_ROW_LINES
        elif wx.Platform == '__WXGTK__':
            style = style | wx.TR_NO_LINES
        self.tree = wx.TreeCtrl(self, -1, style = style)
        self.tree.SetImageList(self.outlineimagelist)

        self.sizer.Add(self.tree, 1, wx.EXPAND)
        self.root = self.tree.AddRoot('Outline')

        self.nodes = {}
        self.ID = 1
        self.cache = None

#        wx.EVT_TREE_SEL_CHANGING(self.tree, self.tree.GetId(), self.OnChanging)
        wx.EVT_TREE_SEL_CHANGED(self.tree, self.tree.GetId(), self.OnChanged)
        wx.EVT_TREE_BEGIN_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnBeginChangeLabel)
        wx.EVT_TREE_END_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnChangeLabel)
        wx.EVT_TREE_ITEM_ACTIVATED(self.tree, self.tree.GetId(), self.OnSelected)
        wx.EVT_TREE_ITEM_RIGHT_CLICK(self.tree, self.tree.GetId(), self.OnRClick)
        wx.EVT_RIGHT_UP(self.tree, self.OnRClick)
        wx.EVT_TREE_DELETE_ITEM(self.tree, self.tree.GetId(), self.OnDeleteItem)
        wx.EVT_LEFT_DCLICK(self.tree, self.OnDoubleClick)
        wx.EVT_TREE_ITEM_EXPANDING(self.tree, self.tree.GetId(), self.OnExpanding)
        wx.EVT_KEY_DOWN(self.tree, self.OnKeyDown)
        wx.EVT_CHAR(self.tree, self.OnChar)

        pop_menus = copy.deepcopy(OutlineWindow.popmenulist)
        self.popmenus = makemenu.makepopmenu(self, pop_menus)
        self.recentmenu_ids = [self.IDPM_RECENT_OUTLINES]

        wx.EVT_UPDATE_UI(self, self.IDPM_CUT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_COPY, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_PASTE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_SAVE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_SAVEAS, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_CLOSE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_NEW_FOLDER, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_NEW_NODE, self.OnUpdateUI)

        #add init process
        self.callplugin('init', self)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

        self.popmenus = None

    def OnUpdateUI(self, event):
        eid = event.GetId()
        item = self.tree.GetSelection()
        if not self.is_ok(item):
            event.Enable(self.is_ok(item))
            return
        if eid in [self.IDPM_CUT, self.IDPM_COPY]:
            event.Enable(self.is_ok(item))
        elif eid == self.IDPM_PASTE:
            event.Enable(bool(self.cache))
        elif eid in [self.IDPM_CLOSE, self.IDPM_SAVE]:
            if self.is_first_node(item):
                event.Enable(True)
            else:
                event.Enable(False)
        elif eid in [self.IDPM_NEW_FOLDER, self.IDPM_NEW_NODE]:
            event.Enable(self.is_folder(item))
        self.callplugin('on_update_ui', self, event)

    def addnode(self, parent, caption, imagenormal, imageexpand=None, _id=None, data=None):
        obj = self.tree.AppendItem(parent, caption)
        if not _id:
            _id = self.getid()
        self.nodes[_id] = data
        self.tree.SetPyData(obj, _id)
        self.tree.SetItemImage(obj, imagenormal, wx.TreeItemIcon_Normal)
        if imageexpand:
            self.tree.SetItemImage(obj, imageexpand, wx.TreeItemIcon_Expanded)
        return obj

    def get_cur_node(self):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        _id = self.tree.GetPyData(item)
        return item, self.nodes.get(_id, None)

    def get_node(self, item):
        if not item.IsOk(): return
        _id = self.tree.GetPyData(item)
        return self.nodes.get(_id, None)

    def getid(self):
        _id = self.ID
        self.ID += 1
        return _id

    def OnCloseWin(self):
        for klass in self.processors.values():
            if hasattr(klass, 'OnSharewinClose'):
                klass.OnSharewinClose()

    def OnChangeLabel(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        text = event.GetLabel()
        if text:
            self.update_node(item, text)
        
    def OnSelected(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        self.callplugin('on_selected', self, item)

    def OnExpanding(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
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
            pop_menus = copy.deepcopy(OutlineWindow.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(OutlineWindow.popmenulist)
        self.popmenus = pop_menus = makemenu.makepopmenu(self, pop_menus)
        self.recentmenu_ids = [self.IDPM_RECENT_OUTLINES]
        self.create_recent_outline_menu()
        self.tree.PopupMenu(pop_menus)
  
    def OnDeleteItem(self, event):
        item = event.GetItem()
        if item.IsOk():
            del self.nodes[self.tree.GetPyData(item)]
        event.Skip()

    def OnBeginChangeLabel(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        if self.is_first_node(item):
            event.Veto()
            return
        else:
            event.Skip()

    def is_ok(self, item):
        return item.IsOk() and item != self.root

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
        self.tree.SelectItem(item)
        self.tree.EditLabel(item)

    def OnDelete(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        self.tree.Delete(item)

    def OnChanged(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
#        self.mainframe.createOutlineEditWindow()
#        self.mainframe.panel.showPage('Outline Edit')
#        page = self.mainframe.panel.getPage('Outline Edit')
#        e = self.get_node_data(item)['element']
#        if e.text is not None:
#            page.SetValue(e.text)
        document = self.mainframe.editctrl.new('outline://edit', documenttype='outlineedit')
        e = self.get_node_data(item)['element']
        document.outline = self
        document.outline_node = item
        document.setTitle(e.attrib.get('caption', tr('(NoTitle)')))
            
        if e.text is not None:
            document.SetText(e.text)
        else:
            document.SetText('')
        document.SetSavePoint()
        self.callplugin('on_changed', self, item)

    def OnChanging(self, event):
        item = event.GetOldItem()
        if not item.IsOk(): return
        if not self.execplugin('on_changing', self, item):
            event.Skip()

    def get_image_id(self, name):
        return self.imageids.get(name, -1)

    def add_image(self, name, imagefile):
        if not self.imagefiles.has_key(name):
            self.imagefiles[name] = imagefile
        if not self.imageids.has_key(name):
            image = common.getpngimage(imagefile)
            self.imageids[name] = self.outlineimagelist.Add(image)

    def OnOutlineCut(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        self.cache = 'cut', item
      
    def OnOutlineCopy(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        self.cache = 'copy', item
      
    def OnOutlinePaste(self, event):
        action, item = self.cache
        dstobj = self.tree.GetSelection()
        if not self.is_ok(dstobj): return
  
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        ctrl = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()
        if key == ord('X') and ctrl:
            wx.CallAfter(self.OnOutlineCut, None)
        elif key == ord('C') and ctrl:
            wx.CallAfter(self.OnOutlineCopy, None)
        elif key == ord('V') and ctrl:
            wx.CallAfter(self.OnOutlinePaste, None)
        event.Skip()
      
    def OnChar(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        key = event.GetKeyCode()
        ctrl = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()
        if key == wx.WXK_DELETE:
            wx.CallAfter(self.OnDelete, None)
        elif key == wx.WXK_INSERT and not ctrl: #insert a folder
            node = self.addnode(item, 'NewItem', self.get_image_id('close'), self.get_image_id('open'), self.getid())
            self.EditLabel(node)
  
    def OnNewOutline(self, event):
        dlg = wx.FileDialog(self, tr("New Outline File"), self.pref.last_dir, '', 'Outline File(*.otl)|*.otl|All Files(*.*)|*.*', wx.SAVE|wx.OVERWRITE_PROMPT)
        dlg.SetFilterIndex(0)
        filename = None
        if (dlg.ShowModal() == wx.ID_OK):
            filename = dlg.GetPath()
        dlg.Destroy()
        f = file(filename, 'wb')
        w = XMLWriter(f)
        w.start('xml')
        w.start('outline')
        w.start('properties')
        w.end('properties')
        w.start('folder')
        w.end('folder')
        w.end('outline')
        w.end('xml')
        f.close()
        self.addoutline(filename)
    
    def create_recent_outline_menu(self):
        menu = makemenu.findmenu(self.menuitems, 'IDPM_RECENT')
        for id in self.recentmenu_ids:
            menu.Delete(id)
            self.recentmenu_ids = []
        if len(self.pref.recent_outlines) == 0:
            id = self.IDPM_RECENT_OUTLINES
            menu.Append(id, tr('(empty)'))
            menu.Enable(id, False)
            self.recentmenu_ids = [id]
        else:
            for i, path in enumerate(self.pref.recent_outlines):
                id = wx.NewId()
                self.recentmenu_ids.append(id)
                menu.Append(id, "%d %s" % (i+1, path))
                wx.EVT_MENU(self, id, self.OnRecentOutline)
  
    def getTopOutlines(self):
        files = []
        for item in self.getTopObjects():
            files.append(self.tree.GetItemText(item))
        return files

    def addoutline(self, filename):
        files = self.getTopOutlines()
        filename = common.uni_file(filename)
        if filename not in files:
            if filename in self.pref.recent_outlines:
                self.pref.recent_outlines.remove(filename)
            self.pref.recent_outlines.insert(0, filename)
            self.pref.recent_outlines = self.pref.recent_outlines[:self.pref.recent_outlines_num]
            self.pref.save()
            
            self.tree.Freeze()
            node = self.add_new_folder(self.root, filename, data={'type':'root', 'filename':filename})
            self.read_outline_file(filename, node)
            self.tree.Thaw()
            
        self.callplugin('after_addoutlinefile', self)
    
    def read_outline_file(self, filename, node):
        try:
            e = ElementTree(file=filename)
            data = self.get_node_data(node)
            data['etree'] = e
            data['element'] = e.find('outline/folder')
            title = e.find('outline/properties/title')
            if title and title.text:
                self.tree.SetItemText(node, title.text)
            nodes = e.find('outline/folder')
            
            def add_nodes(root, nodes):
                for n in nodes:
                    if n.tag == 'node':
                        obj = self.add_new_node(root, n.attrib['caption'], data={'element':n})
                    elif n.tag == 'folder':
                        obj = self.add_new_folder(root, n.attrib['caption'], data={'element':n})
                        add_nodes(obj, n.getchildren())
                self.tree.Expand(root)
                        
            add_nodes(node, nodes)
            wx.CallAfter(self.tree.SelectItem, node)
            
            return True
        except:
            error.traceback()
            common.showerror(self, tr("There are some errors as openning the Outline file"))
            return False
            
    def OnRecentOutline(self, event):
        eid = event.GetId()
        index = self.recentmenu_ids.index(eid)
        self.addoutline(self.pref.recent_outlines[index])
        
    def OnNewFolder(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
    
        parent_element = self.get_node_data(item)['element']
        new_element = SubElement(parent_element, 'folder', {'caption':'NewFolder'})
        
        node = self.add_new_folder(item, 'NewFolder', data={'element':new_element})
        
        wx.CallAfter(self.tree.Expand, item)
        wx.CallAfter(self.EditLabel, node)
        
    def OnNewNode(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
    
        parent_element = self.get_node_data(item)['element']
        new_element = SubElement(parent_element, 'node', {'caption':'NewItem'})
        
        node = self.add_new_node(item, 'NewItem', data={'element':new_element})
        
        wx.CallAfter(self.tree.Expand, item)
        wx.CallAfter(self.EditLabel, node)
        
    def update_node(self, node, newcaption=None, newcontent=None):
        element = self.get_node_data(node)['element']
        if newcaption is not None and self.tree.GetItemText(node) != newcaption:
            element.attrib['caption'] = newcaption
            self.set_modify(node)
        if newcontent is not None and element.text != newcontent:
            element.text = newcontent
            self.set_modify(node)
            
    def add_new_folder(self, parent, caption, data=None):
        if not data:
            data={'type':'folder'}
        if not data.has_key('type'):
            data['type'] = 'folder'
        return self.addnode(parent, caption, self.get_image_id('close'), self.get_image_id('open'), data=data)
    
    def add_new_node(self, parent, caption, data=None):
        if not data:
            data={'type':'node'}
        if not data.has_key('type'):
            data['type'] = 'node'
        return self.addnode(parent, caption, self.get_image_id('item'), data=data)
    
    def get_root_node(self, node):
        if self.is_root(node):
            return node
        while not self.is_root(node):
            node = self.tree.GetItemParent(node)
        return node
        
    def get_node_data(self, node):
        _id = self.tree.GetPyData(node)
        return self.nodes[_id]
    
    def set_modify(self, node, flag=True):
        root = self.get_root_node(node)
        self.get_node_data(root)['modified'] = flag
        
    def get_modify(self, node):
        root = self.get_root_node(node)
        data = self.get_node_data(root)
        return data.has_key('modified') and data['modified']
        
    def OnSaveOutline(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        self.save_outline(item)
            
    def save_outline(self, node):
        root = self.get_root_node(node)
        data = self.get_node_data(root)
        try:
            f = file(data['filename'], 'wb')
            data['etree'].write(f)
            f.close()
            self.set_modify(root, False)
        except:
            error.traceback()
            common.showerror(self, tr("There is something wrong as saving the outline file."))
        
        
    def OnCloseOutline(self, event):
        item = self.tree.GetSelection()
        if not self.is_ok(item): return
        
        if self.get_modify(item):
            dlg = wx.MessageDialog(self, tr('The outline has been modified, do you want to save it ?'), tr("Message"), wx.YES_NO | wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_YES:
                self.save_outline(item)
            dlg.Destroy()
        
        self.tree.Freeze()    
        self.tree.Delete(item)
        self.tree.Thaw()
        
    def is_folder(self, node):
        data = self.get_node_data(node)
        return data['type'] == 'folder'
    
    def is_node(self, node):
        data = self.get_node_data(node)
        return data['type'] == 'node'
      
    def is_root(self, node):
        data = self.get_node_data(node)
        return data['type'] == 'root'
        