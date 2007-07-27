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
#   $Id: EditorFactory.py 1556 2006-10-08 01:59:35Z limodou $

import wx
import os
from modules import Mixin
from modules import makemenu
from MyUnicodeException import MyUnicodeException
from modules.Debug import error
from modules import common
from modules.wxctrl import FlatNotebook as FNB

class EditorFactory(FNB.StyledNotebook, Mixin.Mixin):

    __mixinname__ = 'editctrl'
    popmenulist = []
    imagelist = {}
    panellist = {}
    pageimagelist = {}

    def __init__(self, parent, mainframe):
        self.initmixin()

        self.parent = parent
        self.mainframe = mainframe
        self.pref = self.mainframe.pref
        self.app = self.mainframe.app
        self.mainframe.editctrl = self
        self.document = None
        self.lastfilename = None
        self.lastlanguagename = ''
        self.lastdocument = None

        if self.pref.notebook_direction == 0:
            style = 0
        else:
            style = FNB.FNB_BOTTOM
        FNB.StyledNotebook.__init__(self, parent, -1, size=(0, 0), style=style|FNB.FNB_TABS_BORDER_SIMPLE|FNB.FNB_X_ON_TAB|FNB.FNB_NO_X_BUTTON)
        self.id = self.GetId()


        #make popup menu
        #@add_menu menulist
        self.callplugin_once('add_menu', EditorFactory.popmenulist)
        #@add_menu_image_list imagelist
        self.callplugin_once('add_menu_image_list', EditorFactory.imagelist)
        #@add_panel_list panellist
        self.callplugin_once('add_panel_list', EditorFactory.panellist)

        self.popmenu = makemenu.makepopmenu(self, EditorFactory.popmenulist, EditorFactory.imagelist)
        self.SetRightClickMenu(self.popmenu)
#        wx.EVT_RIGHT_DOWN(self, self.OnPopUp)
##       wx.EVT_LEFT_UP(self, self.OnPageChanged)
#        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, self.id, self.OnChanged)
        FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED(self, self.id, self.OnChanged)
        FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING(self, self.id, self.OnClose)

        self.imageindex = {}
        pageimages = wx.ImageList(16, 16)
        for i, v in enumerate(self.pageimagelist.items()):
            name, imagefilename = v
            image = common.getpngimage(imagefilename)
            pageimages.Add(image)
            self.imageindex[name] = i
        self.pageimages = pageimages

#        self.AssignImageList(self.pageimages)
        self.SetImageList(self.pageimages)

#       self.callplugin('init', self)

#        self.list = []
        self.delete_must = False

#       self.openPage()


    def openPage(self):
        self.callplugin('init', self)

        if not self.execplugin('openpage', self):
            self.new()

        for file in self.mainframe.filenames:
            self.new(os.path.join(self.app.workpath, file))

    def changeDocument(self, document, delay=False):
        if not delay:
            #open delayed document
            if not document.opened:
                index = self.getIndex(document)
                try:
                    document.openfile(document.filename, document.locale, False)
                    #add restore session process
                    for v in self.pref.sessions:
                        if len(v) == 4:
                            filename, row, col, bookmarks = v
                            state = row
                        else:
                            filename, state, bookmarks = v
                        if filename == document.filename:
                            wx.CallAfter(setStatus, document, state, bookmarks)
                except MyUnicodeException, e:
                    error.traceback()
                    e.ShowMessage()
                    wx.CallAfter(self.closefile, document)
                    return
                except:
                    error.traceback()
                    filename = document.filename
                    wx.MessageDialog(self, tr("Can't open the file [%s]!") % common.uni_file(filename), tr("Open file..."), wx.OK).ShowModal()
                    wx.CallAfter(self.closefile, document)
                    return
            self._changeDocument(document)
            wx.CallAfter(self.document.SetFocus)
        return document
#           self.document.EnsureCaretVisible()

    def _changeDocument(self, document):
        self.mainframe.document = document
        self.document = document
        self.showTitle(self.document)
        if self.lastdocument != self.document or self.lastfilename != document.filename:
            if self.lastfilename is not None:
                self.callplugin('on_document_leave', self, self.lastfilename, self.lastlanguagename)
            self.callplugin('on_document_enter', self, document)
        if self.lastlanguagename != document.languagename:
            self.callplugin('on_document_lang_leave', self, self.lastfilename, self.lastlanguagename)
            self.callplugin('on_document_lang_enter', self, document)

        self.lastfilename = document.filename
        self.lastlanguagename = document.languagename
        self.lastdocument = document

    def getIndex(self, document):
        for i, d in enumerate(self.getDocuments()):
            if d == document:
                return i
        return -1

    def getDoc(self, index):
        return self.getDocuments()[index]
    
    def new(self, filename='', encoding='', delay=False, defaulttext='', language='', documenttype='texteditor'):
        if filename:
            for document in self.getDocuments():  #if the file has been opened
                if document.isMe(filename, documenttype):
                    self.switch(document, delay)
                    return document
            else:                   #the file hasn't been opened
                #if current page is empty and has not been modified
                if (self.document != None) and self.document.canopenfile(filename, documenttype):
                    #use current page , donot open a new page
                    try:
                        self.document.openfile(filename, encoding, delay, defaulttext)
                    except MyUnicodeException, e:
                        error.traceback()
                        e.ShowMessage()
                        return self.document
                    except:
                        error.traceback()
                        wx.MessageDialog(self, tr("Can't open the file [%s]!") % filename, tr("Open file..."), wx.OK).ShowModal()
                        return self.document

                    self.switch(self.document, delay)
                    return self.document
                else:
                    return self.newPage(filename, encoding, delay=delay, defaulttext=defaulttext, language=language, documenttype=documenttype)
        else:
            return self.newPage(filename, encoding, delay=delay, defaulttext=defaulttext, language=language, documenttype=documenttype)

    def newPage(self, filename, encoding=None, documenttype='texteditor', delay=False, defaulttext='', language='', **kwargs):
        try:
            panelclass = self.panellist[documenttype]
        except:
            error.traceback()
            return None

        panel = None
        try:
            panel = panelclass(self, filename, **kwargs)
            document = panel.document
            document.openfile(filename, encoding, delay, defaulttext, language)
        except MyUnicodeException, e:
            error.traceback()
            e.ShowMessage()
            if panel:
                panel.Destroy()
            return None
        except:
            error.traceback()
            if panel:
                panel.Destroy()
            wx.MessageDialog(self, tr("Can't open the file [%s]!") % filename, tr("Open file..."), wx.OK).ShowModal()
            return None

#        self.list.append(document)
        self.AddPage(panel, document.getShortFilename())
        self.SetSelection(self.getIndex(document))
        imageindex = self.imageindex.get(document.pageimagename, -1)
        if imageindex > -1:
            self.SetPageImage(self.GetPageCount() - 1, imageindex)
        self.switch(document, delay)
        return document

    def OnChanged(self, event):
#        document = self.list[event.GetSelection()]
        document = self.getDoc(event.GetSelection())
        self.changeDocument(document)
        event.Skip()

    def OnPopUp(self, event):
        self.PopupMenu(self.popmenu, event.GetPosition())

    def OnPopUpMenu(self, event):
        eid = event.GetId()
        if eid == self.ID_CLOSE:
            self.mainframe.OnFileClose(event)
        elif eid == self.ID_CLOSE_ALL:
            self.mainframe.OnFileCloseAll(event)
        elif eid == self.ID_SAVE:
            self.mainframe.OnFileSave(event)
        elif eid == self.IDPM_FILE_SAVE_ALL:
            self.mainframe.OnFileSaveAll(event)
        elif eid == self.ID_SAVEAS:
            self.mainframe.OnFileSaveAs(event)

    def switch(self, document, delay=False):
        try:
            index = self.getIndex(document)
        except:
            error.traceback()
            return
        if not delay:
            self.showPageTitle(document)
            if index != self.GetSelection():
                self.SetSelection(index)
            d = document
            if not document.opened:
                d = self.changeDocument(document, False)
            if d:
                self._changeDocument(document)

    def getDispTitle(self, ctrl):
        if ctrl.title:
            return ctrl.title

        if ctrl.isModified():
            pagetitle = ctrl.getFilename() + ' *'
        else:
            pagetitle = ctrl.getFilename()

        if isinstance(pagetitle, str):
            pagetitle = common.decode_string(pagetitle, common.defaultfilesystemencoding)

        return pagetitle

    def getDocuments(self):
        s = []
        for i in range(self.GetPageCount()):
            s.append(self.GetPage(i).document)
        return s

    def showPageTitle(self, ctrl):
        title = os.path.basename(ctrl.getShortFilename())
        if isinstance(title, str):
            title = common.decode_string(title, common.defaultfilesystemencoding)
        if ctrl.isModified():
            title = '* ' + title
        index = self.getIndex(ctrl)
        if title != self.GetPageText(index):
            wx.CallAfter(self.SetPageText, self.getIndex(ctrl), title)
#           self.Refresh()

    def showTitle(self, ctrl):
        title = u"%s - [%s]" % (self.app.appname, self.getDispTitle(ctrl))
        if title != self.mainframe.GetTitle():
            self.mainframe.SetTitle(title)

    def closefile(self, document):
        try:
            index = self.getIndex(document)
        except:
            return
#        self.list.pop(index)
        self.delete_must = True
        self.DeletePage(index)
        if index >= len(self.getDocuments()):
            index = len(self.getDocuments())-1
        if index >= 0:
            self.switch(self.getDoc(index))
        else:
            self.new()

    def savefile(self, document, filename, encoding):
        try:
            state = document.save_state()
            document.savefile(filename, encoding)
            self.switch(document)
            document.restore_state(state)
        except MyUnicodeException, e:
            error.traceback()
            e.ShowMessage()
            return False
        except:
            error.traceback()
            return False
        wx.SafeYield()        
        return True
    
    def OnClose(self, event):
        if not self.delete_must:
            event.Veto()
            wx.CallAfter(self.mainframe.CloseFile, self.document)
        else:
            self.delete_must = False
        
def setStatus(document, state, bookmarks):
    if isinstance(state, tuple):
        document.restore_state(state)
    else:
        document.GotoLine(state)
    for line in bookmarks:
        document.MarkerAdd(line, 0)
