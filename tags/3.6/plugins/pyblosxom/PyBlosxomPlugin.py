#       Programmer:     limodou
#       E-mail:         limodou@gmail.com
#
#       Copyleft 2006 limodou
#
#       Distributed under the terms of the GPL (GNU Public License)
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
#       $Id: PyBlosxomPlugin.py 42 2005-09-28 05:19:21Z limodou $

import wx
from modules import Entry
import xmlrpclib
from BlogManageWindow import *
from mixins.Editor import TextEditor

class PyBlosxomCategories(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title=tr("Edit Categories"), size=(300, 200))

        self.mainframe = parent.mainframe
        self.pref = parent.pref

        box = wx.BoxSizer(wx.VERTICAL)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS)
        box.Add(self.list, 1, wx.EXPAND)
        self.list.InsertColumn(0, tr("Category"), width=100)
        self.list.InsertColumn(1, tr("Path"), width=180)
        self.load()

        box1 = wx.wx.BoxSizer(wx.HORIZONTAL)

        #add button
        self.ID_ADD= wx.NewId()
        self.btnAdd = wx.Button(self, self.ID_ADD, tr('Add'), size=(40, -1))
        box1.Add(self.btnAdd, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        #edit button
        self.ID_EDIT= wx.NewId()
        self.btnEdit = wx.Button(self, self.ID_EDIT, tr('Edit'), size=(40, -1))
        box1.Add(self.btnEdit, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 6)

        #ok button
        self.btnOk = wx.Button(self, wx.ID_OK, tr('Ok'), size=(40, -1))
        box1.Add(self.btnOk, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        #close button
        self.btnClose = wx.Button(self, wx.ID_CANCEL, tr('Close'), size=(40, -1))
        box1.Add(self.btnClose, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        box.Add(box1, 0, wx.ALIGN_CENTER|wx.ALL, 2)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        wx.EVT_BUTTON(self.btnOk, wx.ID_OK, self.OnOk)
        wx.EVT_BUTTON(self.btnAdd, self.ID_ADD, self.OnAdd)
        wx.EVT_BUTTON(self.btnEdit, self.ID_EDIT, self.OnEdit)
        wx.EVT_UPDATE_UI(self.btnEdit, self.ID_EDIT, self.OnUpdateUI)

    def load(self):
        site = self.pref.blog_sites_info[self.pref.blog_sites[self.pref.last_blog_site]]
        for i, c in enumerate(site['categories']):
            self.list.InsertStringItem(i, c['description'])
            self.list.SetStringItem(i, 1, c['title'])

    def OnAdd(self, event):
        dlg = Entry.MyTextEntry(self, tr("Add Category Path"), tr("Input the path of the new category"), "")
        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            if dlg.GetValue():
                i = self.list.GetItemCount()
                self.list.InsertStringItem(i, tr('New Category'))
                self.list.SetStringItem(i, 1, dlg.GetValue())
                self.list.EditLabel(i)
        dlg.Destroy()

    def OnEdit(self, event):
        i = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        if i > -1:
            self.list.EditLabel(i)

    def OnUpdateUI(self, event):
        eid = event.GetId()
        if eid == self.ID_EDIT:
            index = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            event.Enable(index > -1)

    def OnOk(self, event):
        site = self.pref.blog_sites_info[self.pref.blog_sites[self.pref.last_blog_site]]
        categories = []
        setmessage(self.mainframe, tr('Updating categories...'))
        try:
            server = xmlrpclib.ServerProxy(site['url'])

            for i in range(self.list.GetItemCount()):
                description = self.list.GetItemText(i)
                path = self.list.GetItem(i, 1).GetText()
                result = server.newedit.editCategory(site['user'], site['password'], path, description)
                if result:
                    categories.append({'title':path, 'description':description})

            showmessage(self.mainframe, tr('Updating categories successfully!'))

        except Exception, msg:
            showerror(self.mainframe, msg)
        setmessage(self.mainframe, tr('Done'))

        #update pref
        for c in categories:
            title = c['title']
            description = c['description']

            for item in site['categories']:
                if item['title'] == title:
                    item['description'] = description
                    break
            else:
                site['categories'].append(c)

        self.pref.save()

        event.Skip()

class PyBlosxomEditFile(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title=tr("Edit Config Files"), size=(400, 200), style=wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE)

        self.mainframe = parent.mainframe
        self.pref = parent.pref

        box = wx.BoxSizer(wx.VERTICAL)

        self.editor = TextEditor(self, self.mainframe.editctrl, '', 'tmp')
        box.Add(self.editor, 1, wx.EXPAND)

        box1 = wx.wx.BoxSizer(wx.HORIZONTAL)

        #add button
        self.ID_GETFILELIST= wx.NewId()
        self.btnGetFileList = wx.Button(self, self.ID_GETFILELIST, tr('Get File List'), size=(100, -1))
        box1.Add(self.btnGetFileList, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        #edit button
        self.ID_SAVE= wx.NewId()
        self.btnSave = wx.Button(self, self.ID_SAVE, tr('Save'))
        box1.Add(self.btnSave, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 6)

        #close button
        self.btnClose = wx.Button(self, wx.ID_CANCEL, tr('Close'))
        box1.Add(self.btnClose, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        box.Add(box1, 0, wx.ALIGN_CENTER|wx.ALL, 2)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        wx.EVT_BUTTON(self.btnGetFileList, self.ID_GETFILELIST, self.OnGetFileList)
        wx.EVT_BUTTON(self.btnSave, self.ID_SAVE, self.OnSave)

        self.filename = ''

    def OnGetFileList(self, event):
        site = self.pref.blog_sites_info[self.pref.blog_sites[self.pref.last_blog_site]]
        try:
            server = xmlrpclib.ServerProxy(site['url'])
            result = server.newedit.getSysFileList(site['user'], site['password'])
            if result:
                dlg = wx.SingleChoiceDialog(self, tr('Choose a file you want to edit'), tr('File Choose'),
                        result, wx.CHOICEDLG_STYLE)
                ans = dlg.ShowModal()
                if ans == wx.ID_OK:
                    self.filename = dlg.GetStringSelection()
                    self.SetTitle(tr("Edit Config Files") + ' - [%s]' % self.filename)
                    dlg.Destroy()
                    self.getFile()
                else:
                    dlg.Destroy()
        except Exception, msg:
            showerror(self.mainframe, msg)

    def OnSave(self, event):
        setmessage(self.mainframe, tr("Saving..."))
        site = self.pref.blog_sites_info[self.pref.blog_sites[self.pref.last_blog_site]]
        try:
            server = xmlrpclib.ServerProxy(site['url'])
            result = server.newedit.putSysFile(site['user'], site['password'], self.filename, xmlrpclib.Binary(self.editor.GetText().encode('utf-8')))
            if result:
                showmessage(self.mainframe, tr("Saving successfully!"))
        except Exception, msg:
            showerror(self.mainframe, msg)
        setmessage(self.mainframe, tr("Done"))

    def getFile(self):
        setmessage(self.mainframe, tr("Getting file..."))
        site = self.pref.blog_sites_info[self.pref.blog_sites[self.pref.last_blog_site]]
        try:
            server = xmlrpclib.ServerProxy(site['url'])
            result = server.newedit.getSysFile(site['user'], site['password'], self.filename)
            if result:
                self.editor.SetText(unicode(str(result), 'utf-8'))
                self.editor.EmptyUndoBuffer()
                self.editor.SetSavePoint()
        except Exception, msg:
            showerror(self.mainframe, msg)
        setmessage(self.mainframe, tr("Done"))

def uploadFile(win):
    dlg = UploadFileEntry(win)
    ans = dlg.ShowModal()
    if ans == wx.ID_OK:
        filename, newfilename = dlg.GetValue()
        if not newfilename:
            newfilename = filename

        data = xmlrpclib.Binary(file(filename, 'rb').read())

        setmessage(win.mainframe, tr("Uploading..."))
        site = win.pref.blog_sites_info[win.pref.blog_sites[win.pref.last_blog_site]]
        try:
            server = xmlrpclib.ServerProxy(site['url'])
            result = server.newedit.putFile(site['user'], site['password'], newfilename, data)
            if result:
                showmessage(win.mainframe, tr("Uploading file successfully!"))
        except Exception, msg:
            showerror(win.mainframe, msg)
        setmessage(win.mainframe, tr("Done"))

class UploadFileEntry(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = tr('Upload file'))

        box = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, label=tr('Upload filename:'))
        box.Add(t, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self, -1, '', size=(200, 20))
        self.text.SetSelection(-1, -1)
        box1.Add(self.text, 1, wx.EXPAND|wx.ALL, 3)
        self.ID_BROWSER = wx.NewId()
        self.btnBrowser = wx.Button(self, self.ID_BROWSER, tr("Browser"), size=(50, -1))
        box1.Add(self.btnBrowser, 0, wx.ALL, 3)
        box.Add(box1, 1, wx.EXPAND, 5)

        t = wx.StaticText(self, -1, label=tr('New filename:'))
        box.Add(t, 0, wx.ALIGN_LEFT|wx.ALL, 3)
        self.txtNew = wx.TextCtrl(self, -1, '', size=(200, 20))
        box.Add(self.txtNew, 0, wx.ALIGN_LEFT|wx.ALL, 3)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        btnOK.SetDefault()
        box2.Add(btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)

        wx.EVT_BUTTON(self.btnBrowser, self.ID_BROWSER, self.OnBrowser)

        self.SetSizer(box)
        self.SetAutoLayout(True)
        box.Fit(self)

    def GetValue(self):
        return self.text.GetValue(), self.txtNew.GetValue()

    def OnBrowser(self, event):
        dlg = wx.FileDialog(self, tr("Select A File"), "", "", tr("All file (*.*)|*.*"), wx.OPEN|wx.HIDE_READONLY)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.text.SetValue(filename)
            if not self.txtNew.GetValue():
                self.txtNew.SetValue(os.path.basename(filename))

class PyBlosxomFileLists(wx.Dialog):
    def __init__(self, parent, filelists):
        wx.Dialog.__init__(self, parent, -1, title=tr("File Lists"), size=(400, 300), style=wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE)

        self.mainframe = parent.mainframe
        self.pref = parent.pref
        self.filelists = filelists

        box = wx.BoxSizer(wx.VERTICAL)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        box.Add(self.list, 1, wx.EXPAND)
        self.list.InsertColumn(0, tr("Filename"), width=120)
        self.list.InsertColumn(1, 'Url', width=260)
        self.load()

        box1 = wx.wx.BoxSizer(wx.HORIZONTAL)

        #ok button
        self.ID_COPY = wx.NewId()
        self.btnCopy = wx.Button(self, self.ID_COPY, tr('Copy Url'))
        box1.Add(self.btnCopy, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        #ok button
        self.btnOk = wx.Button(self, wx.ID_OK, tr('Close'))
        box1.Add(self.btnOk, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

        box.Add(box1, 0, wx.ALIGN_CENTER|wx.ALL, 2)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        wx.EVT_BUTTON(self.btnCopy, self.ID_COPY, self.OnCopy)
        wx.EVT_UPDATE_UI(self.btnCopy, self.ID_COPY, self.OnUpdateUI)
        wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.OnCopy)

    def load(self):
        for i, c in enumerate(self.filelists):
            self.list.InsertStringItem(i, c['filename'])
            self.list.SetStringItem(i, 1, c['url'])

    def OnCopy(self, event):
        index = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        text = wx.TextDataObject()
        text.SetText(self.list.GetItem(index, 1).GetText())
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(text)
        wx.TheClipboard.Close()
        setmessage(self.mainframe, tr('Copy finished'))

    def OnUpdateUI(self, event):
        eid = event.GetId()
        if eid == self.ID_COPY:
            index = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            event.Enable(index > -1)

def getFileLists(win):
    setmessage(win.mainframe, tr("Getting file lists..."))
    site = win.pref.blog_sites_info[win.pref.blog_sites[win.pref.last_blog_site]]
    try:
        server = xmlrpclib.ServerProxy(site['url'])
        result = server.newedit.getFileList(site['user'], site['password'])
        setmessage(win.mainframe, tr("Done"))
        if result:
            dlg = PyBlosxomFileLists(win, result)
            ans = dlg.ShowModal()
    except Exception, msg:
        showerror(win.mainframe, msg)
