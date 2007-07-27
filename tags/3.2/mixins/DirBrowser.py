#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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
#   $Id: DirBrowser.py 481 2006-01-17 05:54:13Z limodou $

import wx
import os
import copy
from modules import common
from modules import makemenu
from modules import Mixin
from modules.Debug import error


class DirBrowser(wx.Panel, Mixin.Mixin):

    __mixinname__ = 'dirbrowser'

    popmenulist = [ (None,
        [
            (100, 'IDPM_ADD', tr('Add Directory'), wx.ITEM_NORMAL, '', ''),
            (110, 'IDPM_CLOSE', tr('Close Directory'), wx.ITEM_NORMAL, 'OnCloseDirectory', ''),
            (115, 'IDPM_SETPROJ', tr('Set Project'), wx.ITEM_NORMAL, 'OnSetProject', ''),
            (116, 'IDPM_COMMANDLINE', tr('Open Command Window Here'), wx.ITEM_NORMAL, 'OnCommandWindow', ''),
            (120, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (125, 'IDPM_OPENDEFAULT', tr('Open with Default Editor'), wx.ITEM_NORMAL, 'OnOpenDefault', ''),
            (130, 'IDPM_ADDPATH', tr('Add Sub Directory'), wx.ITEM_NORMAL, 'OnAddSubDir', ''),
            (140, 'IDPM_ADDFILE', tr('Add File'), wx.ITEM_NORMAL, 'OnAddFile', ''),
            (150, 'IDPM_RENAME', tr('Rename'), wx.ITEM_NORMAL, 'OnRename', ''),
            (160, 'IDPM_DELETE', tr('Delete'), wx.ITEM_NORMAL, 'OnDelete', ''),
            (170, 'IDPM_REFRESH', tr('Refresh'), wx.ITEM_NORMAL, 'OnRefresh', ''),
            (180, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (190, 'IDPM_IGNORETHIS', tr('Ignore This'), wx.ITEM_NORMAL, 'OnIgnoreThis', ''),
            (200, 'IDPM_IGNORETHISTYPE', tr('Ignore This Type'), wx.ITEM_NORMAL, 'OnIgnoreThisType', ''),
        ]),
        ('IDPM_ADD',
        [
            (100, 'IDPM_ADD_NEWDIR', tr('Open new directory'), wx.ITEM_NORMAL, 'OnAddNewPath', ''),
            (110, 'IDPM_ADD_NEWEDITWORK', tr('Open NewEdit Work Path'), wx.ITEM_NORMAL, 'OnAddNewEditWorkPath', ''),
            (120, 'IDPM_ADD_NEWEDITUSER', tr('Open NewEdit User Path'), wx.ITEM_NORMAL, 'OnAddNewEditUserPath', ''),
            (130, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (140, 'IDPM_ADD_CLEAN', tr('Clean Recently Directoris'), wx.ITEM_NORMAL, 'OnCleanDirectories', ''),
            (150, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (160, 'IDPM_ADD_DIRS', tr('(empty)'), wx.ITEM_NORMAL, '', ''),
        ]),
    ]
    
    project_names = []

    def __init__(self, parent, mainframe, dirs=None):
        self.initmixin()
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.mainframe = mainframe
        self.pref = mainframe.pref

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        imagelist = mainframe.dirbrowser_imagelist
        self.dirbrowserimagelist = _imagel = wx.ImageList(16, 16)
        self.close_image = _imagel.Add(common.getpngimage(imagelist['close']))
        self.open_image = _imagel.Add(common.getpngimage(imagelist['open']))
        self.item_image = _imagel.Add(common.getpngimage(imagelist['item']))

        self.deal_file_images()

        self.tree = wx.TreeCtrl(self, -1, style = wx.TR_EDIT_LABELS|wx.TR_SINGLE|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS|wx.TR_ROW_LINES|wx.TR_HIDE_ROOT)
        self.tree.SetImageList(self.dirbrowserimagelist)

        self.sizer.Add(self.tree, 1, wx.EXPAND)
        self.root = self.tree.AddRoot('DirBrowser')

#        wx.EVT_TREE_SEL_CHANGED(self.tree, self.tree.GetId(), self.OnChanged)
        wx.EVT_TREE_BEGIN_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnBeginChangeLabel)
        wx.EVT_TREE_END_LABEL_EDIT(self.tree, self.tree.GetId(), self.OnChangeLabel)
        wx.EVT_TREE_ITEM_ACTIVATED(self.tree, self.tree.GetId(), self.OnSelected)
        wx.EVT_TREE_ITEM_RIGHT_CLICK(self.tree, self.tree.GetId(), self.OnRClick)
        wx.EVT_RIGHT_UP(self.tree, self.OnRClick)
        wx.EVT_TREE_DELETE_ITEM(self.tree, self.tree.GetId(), self.OnDeleteItem)
        wx.EVT_LEFT_DCLICK(self.tree, self.OnDoubleClick)
        wx.EVT_TREE_ITEM_EXPANDING(self.tree, self.tree.GetId(), self.OnExpanding)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

        self.nodes = {}
        self.ID = 1
        
        #@add_project
        self.callplugin_once('add_project', DirBrowser.project_names)

        pop_menus = copy.deepcopy(DirBrowser.popmenulist)
        self.popmenus = makemenu.makepopmenu(self, pop_menus)

        self.dirmenu_ids = [self.IDPM_ADD_DIRS]

        wx.EVT_UPDATE_UI(self, self.IDPM_CLOSE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_ADDFILE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_ADDPATH, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_DELETE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_REFRESH, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_RENAME, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_IGNORETHIS, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_IGNORETHISTYPE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_OPENDEFAULT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_SETPROJ, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_COMMANDLINE, self.OnUpdateUI)

        self.popmenus = None
        
        if dirs:
            for i in dirs:
                self.addpath(i)

        self.callplugin('init', self)

    def OnUpdateUI(self, event):
        eid = event.GetId()
        item = self.tree.GetSelection()
        if not item.IsOk():
            event.Enable(False)
            return
        if eid == self.IDPM_CLOSE:
            if self.is_first_node(item):
                event.Enable(True)
            else:
                event.Enable(False)
        elif eid in [self.IDPM_ADDFILE, self.IDPM_ADDPATH]:
            event.Enable(item.IsOk())
        elif eid in [self.IDPM_REFRESH, self.IDPM_COMMANDLINE]:
            filename = self.get_node_filename(item)
            if os.path.isdir(filename):
                event.Enable(True)
            else:
                event.Enable(False)
        elif eid in [self.IDPM_DELETE, self.IDPM_RENAME]:
            if self.is_first_node(item):
                event.Enable(False)
            else:
                event.Enable(True)
        elif eid == self.IDPM_IGNORETHIS:
            if self.is_first_node(item):
                event.Enable(False)
            else:
                event.Enable(True)
        elif eid == self.IDPM_IGNORETHISTYPE:
            filename = self.get_node_filename(item)
            if os.path.isdir(filename):
                event.Enable(False)
            else:
                event.Enable(True)
        elif eid == self.IDPM_OPENDEFAULT:
            filename = self.get_node_filename(item)
            if os.path.isdir(filename):
                event.Enable(False)
            else:
                event.Enable(True)
        elif eid == self.IDPM_SETPROJ:
            if self.project_names:
                filename = self.get_node_filename(item)
                if os.path.isdir(filename):
                    event.Enable(True)
                    return
            event.Enable(False)

    def create_recent_path_menu(self):
        menu = makemenu.findmenu(self.menuitems, 'IDPM_ADD')

        for id in self.dirmenu_ids:
            menu.Delete(id)

        self.dirmenu_ids = []
        if len(self.pref.recent_dir_paths) == 0:
            id = self.IDPM_ADD_DIRS
            menu.Append(id, tr('(empty)'))
            menu.Enable(id, False)
            self.dirmenu_ids = [id]
        else:
            for i, path in enumerate(self.pref.recent_dir_paths):
                id = wx.NewId()
                self.dirmenu_ids.append(id)
                menu.Append(id, "%d %s" % (i+1, path))
                wx.EVT_MENU(self, id, self.OnAddPath)

    def OnAddNewPath(self, event):
        dlg = wx.DirDialog(self, tr("Select directory:"), defaultPath=os.getcwd(), style=wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
            self.addpath(path)

    def OnAddPath(self, event):
        eid = event.GetId()
        index = self.dirmenu_ids.index(eid)
        self.addpath(self.pref.recent_dir_paths[index])

    def OnCleanDirectories(self, event):
        self.pref.recent_dir_paths = []
        self.pref.save()
        
    def addpath(self, path):
        dirs = self.getTopDirs()
        path = common.uni_file(path)
        if path not in dirs:
            if path in self.pref.recent_dir_paths:
                self.pref.recent_dir_paths.remove(path)
            self.pref.recent_dir_paths.insert(0, path)
            self.pref.recent_dir_paths = self.pref.recent_dir_paths[:self.pref.recent_dir_paths_num]
            self.pref.save()
            node = self.addnode(self.root, '', path, self.close_image, self.open_image, self.getid())
            self.addpathnodes(path, node)
        self.callplugin('after_addpath', self)

    def addpathnodes(self, path, node):
        try:
            files = os.listdir(path)
        except:
            error.traceback()
            return
        r = [(x, os.path.isdir(os.path.join(path, x))) for x in files if not self.validate(x)]
        if not r: return
        dirs = []
        files = []
        for x, dir in r:
            if dir:
                dirs.append((x, dir))
            else:
                files.append((x, dir))
        dirs.sort(lambda x, y: cmp(x[0].lower(), y[0].lower()))
        files.sort(lambda x, y: cmp(x[0].lower(), y[0].lower()))
        for x, dirflag in dirs:
            obj = self.addnode(node, path, x, self.close_image, self.open_image, self.getid())
            self.tree.SetItemHasChildren(obj, True)
        for x, dirflag in files:
            item_index = self.get_file_image(x)
            self.addnode(node, path, x, item_index, None, self.getid())
        wx.CallAfter(self.tree.Expand, node)
        wx.CallAfter(self.tree.SelectItem, node)

        #add check project plugin call point
        project_names = common.getCurrentPathProjectName(path)
        self.callplugin('project_begin', self, project_names, path)

    def get_file_image(self, filename):
        fname, ext = os.path.splitext(filename)
        if self.fileimages.has_key(ext):
            return self.fileimageindex[self.fileimages[ext]]
        else:
            return self.item_image

    def addnode(self, parent, path, name, imagenormal, imageexpand=None, data=None):
        obj = self.tree.AppendItem(parent, name)
        self.nodes[data] = (path, name, obj)
        self.tree.SetPyData(obj, data)
        self.tree.SetItemImage(obj, imagenormal, wx.TreeItemIcon_Normal)
        if imageexpand:
            self.tree.SetItemImage(obj, imageexpand, wx.TreeItemIcon_Expanded)
        return obj

    def validate(self, path):
        import fnmatch
        flag = False

        self.filter = ['.*', '*.pyc', '*.bak']
        configini = os.path.join(self.mainframe.userpath, 'config.ini')
        from modules import dict4ini
        ini = dict4ini.DictIni(configini)

        if ini.ignore.matches:
            self.filter = ini.ignore.matches
        ini.save()

        for p in self.filter:
            flag |= fnmatch.fnmatch(path, p)

        return flag

    def getid(self):
        _id = self.ID
        self.ID += 1
        return _id

    def OnChangeLabel(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        data = self.tree.GetPyData(item)
        path, name, obj = self.nodes[data]
        text = event.GetLabel()
        if text == '':
            event.Veto()
            return
        if name != text:
            f = os.path.join(path, name)
            if os.path.exists(os.path.join(path, text)):
                common.showerror(self, tr('Filename %s has exists!') % os.path.join(path, text))
                return
            if os.path.exists(f):
                try:
                    os.rename(f, os.path.join(path, text))
                except:
                    event.Veto()
                    error.traceback()
                    common.showerror(self, tr('Cannot change the filename %s to %s!') % (name, text))
                    return
            for d in self.mainframe.editctrl.getDocuments():
                if (os.path.exists(os.path.join(path, text)) and d.getFilename() == os.path.join(path, name)) or d.getFilename() == name:
                    d.setFilename(os.path.join(path, text))
                    self.mainframe.editctrl.showPageTitle(d)
                    if d is self.mainframe.document:
                        self.mainframe.editctrl.showTitle(d)
            self.nodes[data] = path, text, obj
            if self.isFile(item):
                item_index = self.get_file_image(text)
                self.tree.SetItemImage(item, item_index, wx.TreeItemIcon_Normal)
        wx.CallAfter(self.tree.SelectItem, item)

    def OnSelected(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)
        if self.isFile(item):
            wx.CallAfter(self.mainframe.editctrl.new, filename)

#    def OnChanged(self, event):
#        item = event.GetItem()
#        if not item.IsOk(): return
#        filename = self.get_node_filename(item)
#        if os.path.isdir(filename):
#            if self.tree.GetChildrenCount(item) == 0: #need expand
#                self.addpathnodes(filename, item)
#            else:
#                if not self.tree.IsExpanded(item):
#                    self.tree.Expand(item)

    def OnExpanding(self, event):
        item = event.GetItem()
        if self.tree.GetChildrenCount(item) == 0: #need expand
            self.addpathnodes(self.get_node_filename(item), item)
        else:
            event.Skip()
        
    def OnRClick(self, event):
        other_menus = []
        if self.popmenus:
            self.popmenus.Destroy()
            self.popmenus = None
        self.callplugin('other_popup_menu', self, self.getCurrentProjectName(), other_menus)
        import copy
        if other_menus:
            pop_menus = copy.deepcopy(DirBrowser.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(DirBrowser.popmenulist)
        self.popmenus = pop_menus = makemenu.makepopmenu(self, pop_menus)

        self.dirmenu_ids = [self.IDPM_ADD_DIRS]

        self.create_recent_path_menu()
        self.tree.PopupMenu(pop_menus, event.GetPosition())

    def OnCloseDirectory(self, event):
        item = self.tree.GetSelection()
        path = self.get_node_filename(item)
        if not item.IsOk(): return
        if self.is_first_node(item):
            self.tree.Delete(item)

        self.callplugin('after_closepath', self, path)
        #add check project plugin call point
        project_names = common.getCurrentPathProjectName(path)
        self.callplugin('project_end', self, project_names, path)

    def OnAddSubDir(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)

        foldername = 'NewFolder'
        if self.isFile(item):
            item = self.tree.GetItemParent(item)
            filename = self.get_node_filename(item)
        if os.path.exists(os.path.join(filename, foldername)):
            common.showerror(self, tr('Directory %s has exists!') % os.path.join(filename, foldername))
            return

        try:
            os.mkdir(os.path.join(filename, foldername))
        except:
            error.traceback()
            common.showerror(self, tr('Create directory %s error!') % os.path.join(filename, foldername))
            return
        node = self.addnode(item, filename, foldername, self.close_image, self.open_image, self.getid())
        self.tree.EditLabel(node)

    def OnAddFile(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)
        if self.isFile(item):
            item = self.tree.GetItemParent(item)
            filename = self.get_node_filename(item)
        document = self.mainframe.editctrl.new()
        node = self.addnode(item, filename, document.getShortFilename(), self.item_image, None, self.getid())
        wx.CallAfter(self.tree.Expand, item)
        wx.CallAfter(self.tree.EditLabel, node)

    def OnDeleteItem(self, event):
        item = event.GetItem()
        if item.IsOk():
            del self.nodes[self.tree.GetPyData(item)]
        event.Skip()

    def OnDelete(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        parent = self.tree.GetItemParent(item)
        filename = self.get_node_filename(item)
        dlg = wx.MessageDialog(self, tr('Do you want to delete %s ?') % filename, tr("Message"), wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            if os.path.exists(filename):
                if os.path.isdir(filename):
                    try:
                        os.rmdir(filename)
                    except:
                        error.traceback()
                        common.showerror(self, tr('Cannot delete directory %s!') % filename)
                        return
                else:
                    try:
                        os.remove(filename)
                    except:
                        error.traceback()
                        common.showerror(self, tr('Cannot delete file %s!') % filename)
                        return
            self.tree.Delete(item)
        if self.tree.GetChildrenCount(parent) == 0:
            self.tree.Collapse(parent)
            self.tree.SetItemImage(parent, self.close_image, wx.TreeItemIcon_Normal)
        dlg.Destroy()

    def OnRefresh(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        path = self.get_node_filename(item)
        self.tree.DeleteChildren(item)
        self.addpathnodes(path, item)

    def OnRename(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        self.tree.EditLabel(item)

    def OnBeginChangeLabel(self, event):
        item = event.GetItem()
        if not item.IsOk(): return
        if self.is_first_node(item):
            event.Veto()
            return
        else:
            event.Skip()

    def is_first_node(self, item):
        parent = self.tree.GetItemParent(item)
        return parent == self.root

    def get_node_filename(self, item):
        data = self.tree.GetPyData(item)
        path, name, obj = self.nodes[data]
        filename = os.path.join(path, name)
        return filename

    def deal_file_images(self):
        self.fileimages = {}
        self.fileimages['.py'] = 'file_py.gif'
        self.fileimages['.pyw'] = 'file_py.gif'
        self.fileimages['.txt'] = 'file_txt.gif'
        self.fileimages['.html'] = 'file_html.gif'
        self.fileimages['.htm'] = 'file_html.gif'
        self.fileimages['.ini'] = 'file_txt.gif'
        self.fileimages['.bat'] = 'file_txt.gif'
        self.fileimages['.xml'] = 'file_xml.gif'
        configini = os.path.join(self.mainframe.userpath, 'config.ini')
        from modules import dict4ini
        ini = dict4ini.DictIni(configini)
        self.fileimages.update(ini.fileimages)
        ini.fileimages = self.fileimages
        ini.save()

        self.fileimageindex = {}
        for image in self.fileimages.values():
            if not self.fileimageindex.has_key(image):
                obj = common.getpngimage(os.path.join(self.mainframe.userpath, 'images', image))
                self.fileimageindex[image] = self.dirbrowserimagelist.Add(obj)

    def OnIgnoreThis(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)
        if filename not in self.filter:
            self.filter.append(filename)
            configini = os.path.join(self.mainframe.userpath, 'config.ini')
            from modules import dict4ini
            ini = dict4ini.DictIni(configini)
            ini.ignore.matches = self.filter
            ini.save()
            self.tree.Delete(item)

    def OnIgnoreThisType(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)
        fname, ext = os.path.splitext(filename)
        if ext not in self.filter:
            self.filter.append(str('*' + ext))
            configini = os.path.join(self.mainframe.userpath, 'config.ini')
            from modules import dict4ini
            ini = dict4ini.DictIni(configini)
            ini.ignore.matches = self.filter
            ini.save()
            item = self.tree.GetItemParent(item)
            path = self.get_node_filename(item)
            self.tree.DeleteChildren(item)
            #self.addpathnodes(path, item)

    def getCurrentProjectName(self):
        item = self.tree.GetSelection()
        if not item.IsOk():
            projectname = ''
        else:
            projectname = common.getProjectName(self.get_node_filename(item))

        return projectname

    def getCurrentProjectHome(self):
        item = self.tree.GetSelection()
        if not item.IsOk():
            path = ''
        else:
            path = common.getProjectHome(self.get_node_filename(item))

        return path
    
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

    def getTopDirs(self):
        paths = []
        for item in self.getTopObjects():
            paths.append(self.get_node_filename(item))
        return paths

    def OnOpenDefault(self, event):
        item = self.tree.GetSelection()
        if item.IsOk():
            os.startfile(self.get_node_filename(item))
            
    def isFile(self, item):
        if not item.IsOk(): return False
        index = self.tree.GetItemImage(item)
        return index != self.open_image and index != self.close_image
    
    def OnAddNewEditWorkPath(self, event):
        from modules import Globals
        path = Globals.workpath
        self.addpath(path)
        
    def OnAddNewEditUserPath(self, event):
        from modules import Globals
        path = Globals.userpath
        self.addpath(path)
        
    def OnSetProject(self, event):
        item = self.tree.GetSelection()
        from modules import dict4ini
        filename = self.get_node_filename(item)
        proj_file = os.path.join(filename, '_project')
        name = []
        values = []
        if os.path.exists(proj_file):
            ini = dict4ini.DictIni(proj_file)
            name = ini.default.get('projectname', [])
            if name:
                if isinstance(name, list):
                    values = [{'name':x} for x in name]
                else:
                    values = [{'name':name}]
        dialog = [
                ('list', 'project_name', [], tr('Project Names'), {
                    'columns':[(tr('Project Name'), 60, 'right')],
                    'elements':[
                        ('single', 'name', self.project_names[0], tr('Name'), self.project_names),
                    ]
                }),
            ]
        from modules.EasyGuider import EasyDialog
        dlg = EasyDialog.EasyDialog(self, title=tr("Project Setting"), elements=dialog, values={'project_name':values})
        values = None
        if dlg.ShowModal() == wx.ID_OK:
            values = dlg.GetValue()
        dlg.Destroy()
        if values:
            filename = self.get_node_filename(item)
            proj_file = os.path.join(filename, '_project')
            ini = dict4ini.DictIni(proj_file)
            ini.default.projectname = [v['name'] for v in values['project_name']]
            ini.save()
            
            old_project_name = name
            new_project_name = ini.default.projectname
            #add check project plugin call point
            path = filename
            project_names = common.getCurrentPathProjectName(path)
            self.callplugin('project_end', self, list(set(old_project_name) - set(new_project_name)), path)
            self.callplugin('project_begin', self, list(set(new_project_name) - set(old_project_name)), path)
            
    def OnCommandWindow(self, event):
        item = self.tree.GetSelection()
        if not item.IsOk(): return
        filename = self.get_node_filename(item)
        if self.isFile(item):
            item = self.tree.GetItemParent(item)
            filename = self.get_node_filename(item)
        if wx.Platform == '__WXMSW__':
            cmdline = os.environ['ComSpec']
            os.spawnl(os.P_NOWAIT, cmdline, r"cmd.exe /k cd %s" % filename)
        else:
            common.showerror(self, tr('This features is only implemented in Windows Platform.\nIf you know how to implement in Linux please tell me.'))
