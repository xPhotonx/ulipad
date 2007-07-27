__doc__ = 'Music List'

from modules import Mixin
import wx
from modules.Debug import error
import os
import codecs
import PyM3u
import locale
import threading
import time
class MusicListManage(wx.Panel):
    def __init__(self, parent, mainframe):
        self.parent = parent
        self.mainframe = mainframe
        self.defm3u='default.m3u'
        if not os.path.isfile(self.defm3u):
            fout=open(self.defm3u,'w')
            fout.write('#EXTM3U\n')
            fout.close()
        self.m3u=PyM3u.M3u(self.defm3u)
        self.mainframe.m3u=self.m3u
        self.m3u.Load()
        self.mainframe.selectedid=-1
        wx.Panel.__init__(self, parent, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
	
        self.m3u_filename = wx.StaticText(self, -1, '')
        self.playingname = wx.StaticText(self,-1,'')
        box.Add(self.m3u_filename, 0, wx.ALL|wx.EXPAND, 3)
        box.Add(self.playingname, 0, wx.ALL|wx.EXPAND, 3)

        #add button
        self.ID_ADD = wx.NewId()
        self.btnAdd = wx.Button(self, self.ID_ADD, tr('Add'), size=(40, 20))
        box1.Add(self.btnAdd, 0, wx.RIGHT, 2)

        self.ID_ADDDIR =wx.NewId()
        self.btnAddDir = wx.Button(self, self.ID_ADDDIR, tr('AddDir'), size=(60,20))
        box1.Add(self.btnAddDir, 0, wx.RIGHT, 2)

        self.ID_DEL = wx.NewId()
        self.btnDel = wx.Button(self, self.ID_DEL, tr('Delete'), size=(40, 20))
        box1.Add(self.btnDel, 0, wx.RIGHT, 2)

        self.ID_OPEN = wx.NewId()
        self.btnOpen = wx.Button(self, self.ID_OPEN, tr('OpenList'), size=(60, 20))
        box1.Add(self.btnOpen, 0, wx.RIGHT, 2)


        self.ID_SAVE = wx.NewId()
        self.btnSave = wx.Button(self, self.ID_SAVE, tr('SaveList'), size=(60, 20))
        box1.Add(self.btnSave, 0, wx.RIGHT, 2)

        box.Add(box1, 0, wx.ALL, 3)
            
    
        #create listctrl
        self.musiclist=wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
    
        self.musiclist.InsertColumn(0, tr("Id"))
        self.musiclist.InsertColumn(1, tr("Author - Title"))
        self.musiclist.InsertColumn(2, tr("Time(S)"))
        self.musiclist.InsertColumn(3, tr("Path"))
        
        self.musiclist.SetColumnWidth(0,30)
        self.musiclist.SetColumnWidth(1, 180)
        self.musiclist.SetColumnWidth(2, 55)
        self.musiclist.SetColumnWidth(3, 120)
        
        box.Add(self.musiclist, 1, wx.EXPAND)
        
        wx.EVT_BUTTON(self.btnAdd, self.ID_ADD, self.OnAdd)
        wx.EVT_BUTTON(self.btnAddDir, self.ID_ADDDIR, self.OnAddDir)
        wx.EVT_BUTTON(self.btnDel, self.ID_DEL, self.OnDel)
        wx.EVT_BUTTON(self.btnOpen, self.ID_OPEN, self.OnOpen)
        wx.EVT_BUTTON(self.btnSave, self.ID_SAVE, self.OnSave)
        wx.EVT_LIST_ITEM_ACTIVATED(self.musiclist,self.musiclist.GetId(),self.OnActivated)
        wx.EVT_LIST_ITEM_SELECTED(self.musiclist,self.musiclist.GetId(),self.OnSelected)
        
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.OnUpdateData()
        
    def encode(self,text):
        encoding = locale.getdefaultlocale()[1]
        return text.encode(encoding)
        
    def OnActivated(self,event):
        if self.mainframe.src:
            if self.mainframe.src.IsPlaying():
                self.mainframe.isloop=False
                self.mainframe.flag_pause=False
                self.mainframe.src.Stop()
                time.sleep(0.2)
        self.mainframe.selectedid=int(event.GetText())
        from PyMusic import playmusic
        self.mainframe.playing=self.m3u[self.mainframe.selectedid]
        encoding = locale.getdefaultlocale()[1]
        filename = self.mainframe.playing['Path'].encode(encoding)
        threading.Thread(target=playmusic, args=(self.mainframe,)).start()
        self.setplaying(self.mainframe.playing['Author-Title'])
        
    def OnSelected(self,event):
        self.mainframe.selectedid=int(event.GetText())
    def OnAdd(self, event):
        dialog = wx.FileDialog(self.mainframe,
                               "Add Media File To Music List",
                               "",
                               "",
                               "Media files(*.mp3;*.wma;*.asf;*.mid;*.wav)|*.mp3;*.wma;*.asf;*.mid;*.wav",
                               wx.OPEN|wx.MULTIPLE  )
        filenames=[]
        filename = ''
        if dialog.ShowModal() == wx.ID_OK:
            filenames = dialog.GetPaths()
        dialog.Destroy()
        record={}
        for filename in filenames:
#            filename = self.encode(filename)
            if filename.lower().endswith(".mp3"):
                from PyMp3Info import MP3FileInfo
                fi=MP3FileInfo(filename)
                if fi.parse():
                    record['Author-Title']=(fi['author'] and fi['author']+' - ' or '')+fi['title']
                else:
                    record['Author-Title']=os.path.split(filename)[-1]
            else:
                record['Author-Title']=os.path.split(filename)[-1]
            try:
                from pySonic import FileStream
                f=FileStream(self.encode(filename),0)
                record['Time']=str(int(f.Duration))
                del f
            except:
                error.traceback()
                dlg = wx.MessageDialog(self, tr('Can\'t add this file or this file isn\'t a media file!'),
                               tr('Error'),
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
                record={}
                continue
            record['Path']=filename
            self.m3u.Append(record)
            self.addrecord(record)
    def OnAddDir(self,event):
        dialog = wx.DirDialog(self.mainframe,
                               "Add Dir\All Media files to Music List",
                               ".",
                               0,
                               name="Add Dir"
                              )
        path=[]
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        path=self.encode(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename=os.path.join(root,file)
                if filename[-4:].lower() in ['.mp3','.wav','.mid','.wma','.asf']:
                    file = self.encode(filename)
                    record={}
                    if filename.lower().endswith(".mp3"):
                        from PyMp3Info import MP3FileInfo
                        fi=MP3FileInfo(filename)
                        if fi.parse():
                            record['Author-Title']=(fi['author'] and fi['author']+' - ' or '')+fi['title']
                        else:
                            record['Author-Title']=os.path.split(filename)[-1]
                    else:
                        record['Author-Title']=os.path.split(filename)[-1]
                    try:
                        from pySonic import FileStream
                        f=FileStream(filename,0)
                        record['Time']=str(int(f.Duration))
                        del f
                    except:
                        dlg = wx.MessageDialog(win, tr('Can\'t add this file or this file isn\'t a media file!'),
                                       tr('Error'),
                                       wx.OK | wx.ICON_ERROR
                                       )
                        dlg.ShowModal()
                        dlg.Destroy()
                        continue
                    record['Path']=filename
                    self.m3u.Append(record)
                    self.addrecord(record)
                    
    def OnDel(self, event):
        if self.mainframe.selectedid==-1:
            return
        self.m3u.Delete(self.mainframe.selectedid)
        self.delrecord(self.mainframe.selectedid)
        self.mainframe.selectedid=-1
    
    def OnSave(self, event):
        filepath=self.encode(self.m3u.filepath)
        filepath=os.path.split(filepath)
        dialog = wx.FileDialog(self.mainframe, "Save M3u File", filepath[0], filepath[1], "M3u files(*.m3u)|*.m3u", wx.SAVE|wx.OVERWRITE_PROMPT )
        filename = ''
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        if filename:
            self.m3u.SaveToFile(self.encode(filename))
		
    def OnOpen(self, event):
        if self.m3u.IsModify():
            dialog=wx.MessageDialog(self.mainframe,"Save the m3u file to file ?",'Save m3u file!',wx.YES_NO|wx.YES_DEFAULT)
            if dialog.ShowModal()==wx.ID_YES:
                self.OnSave()
            dialog.Destroy()
        dialog = wx.FileDialog(self.mainframe, "Open M3u File", "", "", "M3u files(*.m3u)|*.m3u", wx.OPEN )
        filename = ''
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        if filename:
            filename = self.encode(filename)
            self.m3u.ClearAll()
            self.m3u.Load(filename)
            self.OnUpdateData()
            
    def addrecord(self,record):
        lastid=self.musiclist.GetItemCount()
        self.musiclist.InsertStringItem(lastid,str(int(lastid)).rjust(3))
        self.musiclist.SetStringItem(lastid,1,record['Author-Title'])
        self.musiclist.SetStringItem(lastid,2,record['Time'])
        self.musiclist.SetStringItem(lastid,3,record['Path'])
        
    def delrecord(self,id):
        self.musiclist.DeleteItem(id)
        for i in range(self.musiclist.GetItemCount()):
            self.musiclist.SetStringItem(i,0,str(i).rjust(3))
    def setplaying(self,playing):
        self.playingname.SetLabel('Playing : %s'%playing)
    def OnUpdateData(self):
        self.m3u_filename.SetLabel('M3U File : '+self.m3u.GetFilePath())
        if self.mainframe.playing:
            self.setplaying(self.mainframe.playing['Author-Title'])
        else:
            self.setplaying('Playing : No Playing')
        self.musiclist.DeleteAllItems()
        for id in range(len(self.m3u.data)):
            self.musiclist.InsertStringItem(id,str(id).rjust(3))
            record=self.m3u.data[id]
            try:
                self.musiclist.SetStringItem(id,1,record['Author-Title'])
            except:
                self.musiclist.SetStringItem(id,1,os.path.split(record['Path'])[-1])
            self.musiclist.SetStringItem(id,2,record['Time'])
            try:
                self.musiclist.SetStringItem(id,3,record['Path'])
            except:
                self.musiclist.SetStringItem(id,3,'?'*len(record['Path']))
