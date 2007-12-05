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
#   $Id$
#   Update:
#   2008/08/25
#       * Support Chinese filename, and auto adaptate the utf-8 encoding and local
#         locale
#       * When exporting, can test if the direction directory is already existed
#       * Add refreshing current folder functionality after the svn command finished
#   2008/08/27
#       * Add show unversioned files checkbox
#       * Add select / deselect all checkbox, support 3Dstates

import wx
import os
from modules import Globals
from modules import Casing
from modules import common
from modules import meide as ui
from modules.Debug import error
from modules import CheckList

#export functions
################################################################
def do(dirwin, command, *args):
    callbacks = {
        'update': dirwin.OnRefresh,
        'commit':dirwin.OnRefresh,
        'add':dirwin.OnRefresh,
        'rename':dirwin.OnRefresh,
        'delete':dirwin.OnRefresh,
        'revert':dirwin.OnRefresh,
        'status':dirwin.OnRefresh,
    }

    proxy = Command(dirwin, *args)
    func = getattr(proxy, command, None)
    if func:
        func(callbacks.get(command, None))
    else:
        common.showerror(tr("Don't support [%s] command!") % command)

class Command(object):
    def __init__(self, dirwin, *args):
        try:
            import pysvn
            client = pysvn.Client()
        except:
            common.showerror(dirwin, tr('You should install pysvn module first.\nYou can get it from http://pysvn.tigris.org/'))
            return
        
        self.svn = pysvn
        self.dirwin = dirwin
        self.args = args
        self.pref = Globals.pref
        self.path = args[0]
        self.result = None
        
    def export(self, callback=None):
        dirwin = self.dirwin
        url = self.path
        path = get_path(dirwin.pref.version_control_export_path)
        self.pref.version_control_export_path = path
        self.pref.save()
        if not path:
            return
        export_path = os.path.join(path, os.path.basename(url))
        if os.path.exists(export_path):
            dlg = wx.MessageDialog(dirwin, tr("The directory is existed, do you want to overwrite it?"), 
                tr("Export"), wx.YES_NO|wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            dlg.Destroy()
            if answer != wx.ID_YES:
                return
            force = True
        else:
            force = False
            
        def f():
            client = self.svn.Client()
            client.export(url, export_path, force)
        wrap_run(f, callback)
            
    def checkout(self, callback=None):
        dlg = CheckoutDialog()
        value = None
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()
        dlg.Destroy()
        if not value: return
    
        if value['revision']:
            r = value['revision']
        else:
            r = self.svn.Revision(self.svn.opt_revision_kind.head )
    
        self.result = ResultDialog()
        self.result.Show()
        
        def f():
            client = self.svn.Client()
            client.callback_notify  = self.cbk_update
            client.checkout(value['url'], value['dir'], revision=r)
            self.result.finish()
        wrap_run(f, callback)
            
    def list(self, callback=None):
        def f():
            client = self.svn.Client()
            r = client.list(self.path)
            s = []
            fmt = "%(path)-60s %(last_author)-20s %(size)-10s"
            s.append(fmt % {'path':'Filename', 'last_author':'Last Author', 'size':'Size'})
            for node, flag in r:
                t = fmt % node
                s.append(t)
            wx.CallAfter(show_in_message_win, '\n'.join(s))
        wrap_run(f, callback)
        
    def status(self, callback=None):
        def f():
            client = self.svn.Client()
            r = client.status(self.path, ignore=True)
            s = []
            fmt = "%(path)-60s %(text_status)-20s"
            s.append(fmt % {'path':'Filename', 'text_status':'Status'})
            for node in r:
                t = fmt % node
                s.append(t)
            wx.CallAfter(show_in_message_win, '\n'.join(s))
        wrap_run(f, callback)
        
    def log(self, callback):
        def f():
            import time
            
            client = self.svn.Client()
            r = client.log(self.path)
            s = []
            fmt = ("%(message)s\n" + '-'*70 + 
                "\nr%(revision)d | %(author)s | %(date)s\n")
            for node in r:
                node['revision'] = node['revision'].number
                node['date'] = time.strftime("%Y-%m-%d %H:%M:%S", 
                    time.localtime(node['date']))
                if not node['author']:
                    node['author'] = tr('<No Author>')
                t = fmt % node
                s.append(t)
            wx.CallAfter(show_in_message_win, '\n'.join(s))
        wrap_run(f, callback)
        
    def diff(self, callback):
        def f():
            client = self.svn.Client()
            r = client.diff(wx.StandardPaths.Get().GetTempDir(), self.path)
            wx.CallAfter(show_in_message_win, r)
        wrap_run(f, callback)
        
    def add(self, callback):
        dlg = AddDialog(Globals.mainframe, tr('Add'), self.path)
        values = []
        if dlg.ShowModal() == wx.ID_OK:
            values = dlg.GetValue()
        dlg.Destroy()
        
        if values:
            self.result = ResultDialog()
            self.result.Show()
            
            def f():
                client = self.svn.Client()
                client.callback_notify  = self.cbk_notify
                r = client.add(values, False)
                self.result.finish()
            wrap_run(f, callback)
            
    def revert(self, callback):
        dlg = RevertDialog(tr('Revert'), self.path)
        values = []
        if dlg.ShowModal() == wx.ID_OK:
            values = dlg.GetValue()
        dlg.Destroy()
        
        if values:
            self.result = ResultDialog()
            self.result.Show()
            
            def f():
                client = self.svn.Client()
                client.callback_notify  = self.cbk_notify
                r = client.revert(values, False)
                self.result.finish()
            wrap_run(f, callback)
            
    def rename(self, callback):
        dir = os.path.dirname(self.path)
        dlg = wx.TextEntryDialog(Globals.mainframe, tr('New name'),
            tr('Rename'), os.path.basename(self.path))
        newname = ''
        if dlg.ShowModal() == wx.ID_OK:
            newname = os.path.join(dir, dlg.GetValue())
        dlg.Destroy()
        if newname:
            def f():
                client = self.svn.Client()
                r = client.move(self.path, os.path.join(dir, newname))
            wrap_run(f, callback)
            
    def delete(self, callback):
        def f():
            client = self.svn.Client()
            r = client.remove(self.path)
        wrap_run(f, callback)
        
    def update(self, callback):
        self.result = ResultDialog()
        self.result.Show()
        
        def f():
            client = self.svn.Client()
            client.callback_notify  = self.cbk_update
            r = client.update(self.path)
            self.result.finish()
        wrap_run(f, callback)
    
    def commit(self, callback):
        dlg = CommitDialog(tr('Commit'), self.path)
        values = None
        if dlg.ShowModal() == wx.ID_OK:
            values =  dlg.GetValue()
        dlg.Destroy()
        
        if values['add_files'] + values['files']:
            self.result = ResultDialog()
            self.result.Show()
            
            def f():
                client = self.svn.Client()
                client.callback_notify  = self.cbk_notify
                if values['add_files']:
                    r = client.add(values['add_files'], False)
                r = client.checkin(values['add_files'] + values['files'], values['message'])
                self.result.finish()
            wrap_run(f, callback)
        
    def cbk_update(self, event):
        print event
        if event['error']:
            self.result.add([tr('error'), event['error']])
        else:
            action = str(event['action'])
            if action.startswith('update_'):
                action = action[7:]
            if action == 'update':
                return
            elif action == 'completed':
                action = 'completed'
                path = 'At version %d' % event['revision'].number
            else:
                path = event['path']
            self.result.add([action, path])
            
    def cbk_notify(self, event):
        print event
        if event['error']:
            self.result.add([tr('error'), event['error']])
        else:
            self.result.add([str(event['action']), event['path']])
        
#common functions
################################################################
def show_in_message_win(text, clear=True, goto_end=False):
    win = Globals.mainframe
    win.createMessageWindow()
    win.panel.showPage(tr('Message'))
    if clear:
        win.messagewindow.SetText('')
    win.messagewindow.AddText(text)
    if goto_end:
        win.messagewindow.GotoPos(win.messagewindow.GetTextLength())
    else:
        win.messagewindow.GotoPos(0)
    
def wrap_run(func, callback=None, begin_msg=tr('Processing...'), end_msg='', finish_msg='Finished!'):
    def f():
        common.setmessage(begin_msg)
        try:
            try:
                func()
                if callback:
                    callback()
            except Exception, e:
                error.traceback()
                common.showerror(str(e))
        finally:
            common.setmessage(end_msg)
    Casing.Casing(f).start_thread()
    
def get_entries(path):
    import pysvn
    client = pysvn.Client()
    entries = {}
    for line in client.status(path, False, ignore=True):
        entries[os.path.basename(line['path'])] = str(line['text_status'])
    return entries

#dialogs
################################################################
def get_path(path=''):
    if not path:
        path = os.getcwd()
    dlg = wx.DirDialog(Globals.mainframe, tr("Select directory:"), defaultPath=path, style=wx.DD_NEW_DIR_BUTTON)
    if dlg.ShowModal() == wx.ID_OK:
        dir = dlg.GetPath()
        dlg.Destroy()
        return dir
    
def is_versioned(path):
    try:
        import pysvn
    except:
        return False
    client = pysvn.Client()
    r = client.status(path, False)
    if len(r) > 0:
        return r[0]['is_versioned']
    else:
        return False

class CheckoutDialog(wx.Dialog):
    def __init__(self, title=tr('Checkout'), size=(450, -1)):
        wx.Dialog.__init__(self, Globals.mainframe, -1, title=title, size=size)
        
        self.pref = Globals.pref
        self.sizer = sizer = ui.VBox(namebinding='widget').create(self).auto_layout()
        box = sizer.add(ui.VGroup(tr('Repository')))
        box.add(ui.Label(tr('URL of repository:')))
        box.add(ui.ComboBox('', self.pref.svn_urls), name='url')
        box.add(ui.Label(tr('Checkout Directory')))
        box.add(ui.Dir(self.pref.svn_checkout_folder), name='dir')
        
        box = sizer.add(ui.VGroup(tr('Revision')))
        box1 = box.add(ui.HBox)
        box1.add(ui.Check(False, tr('Revision'), name='chk_revision')).bind('check', self.OnCheck)
        box1.add(ui.Text('', size=(80, -1)), name='revision').get_widget().Disable()
        
        sizer.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        sizer.bind('btnOk', 'click', self.OnOk)
        self.btnOk.SetDefault()
        
        sizer.auto_fit(1)
        
    def OnCheck(self, event):
        self.revision.Enable()
        
    def GetValue(self):
        return self.sizer.GetValue()
    
    def OnOk(self, event):
        url = self.url.GetValue()
        if url:
            try:
                self.pref.svn_urls.remove(url)
            except:
                pass
            self.pref.svn_urls.insert(0, url)
            del self.pref.svn_urls[30:]
            self.pref.save()
        path = self.dir.GetValue()
        if path:
            self.pref.svn_checkout_folder = path
            self.pref.save()
        event.Skip()

class AddDialog(wx.Dialog):
    def __init__(self, parent, title, path):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(400, 300))
        self.path = path
        
        self.sizer = box = ui.VBox(namebinding='widget').create(self).auto_layout()
        self.list = CheckList.CheckList(self, columns=[
                (tr("File"), 380, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.add(self.list, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        self.list.on_check = self.OnCheck
        
        #add selection switch checkbox
        box.add(ui.Check3D(2, tr('Select / deselect All')), name='select').bind('check', self.OnSelect)
        
        box.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        self.btnOk.SetDefault()
        
        self.init()

    def init(self):
        def f():
            from SvnSettings import get_global_ignore
            ignore = [x[1:] for x in get_global_ignore().split()]
            
            import pysvn
            client = pysvn.Client()
            r = client.status(self.path)
            files = {}
            for node in r:
                files[node['path']] = node['is_versioned']
            if os.path.isfile(self.path) and not files.get(self.path, False):
                self.path = os.path.dirname(self.path)
                wx.CallAfter(self.list.addline, [os.path.basename(self.path)], flag=True)
            else:
                if not files.get(self.path, False):
                    wx.CallAfter(self.list.addline, ['.'], flag=True)
                _len = len(self.path)
                for curpath, dirs, fs in os.walk(self.path):
                    if '.svn' in curpath:
                        continue
                    for fname in fs:
                        ext = os.path.splitext(fname)[1]
                        if ext in ignore:
                            continue
                        filename = os.path.join(curpath, fname)
                        if not files.get(filename, False):
                              wx.CallAfter(self.list.addline, [filename[_len+1:]], flag=True)

        wrap_run(f)
        
    def GetValue(self):
        files = []
        for i in range(self.list.GetItemCount()):
            if not self.list.getFlag(i):
                continue
            f = self.list.getCell(i, 0)
            if f == '.':
                f = self.path
            else:
                f = os.path.join(self.path, f)
            files.append(f)
        return files
    
    def check_state(self):
        count = {True:0, False:0}
        for i in range(self.list.GetItemCount()):
            count[self.list.getFlag(i)] += 1
        if count[True] > 0 and count[False] > 0:
            self.select.Set3StateValue(wx.CHK_UNDETERMINED)
        elif count[True] > 0 and count[False] == 0:
            self.select.Set3StateValue(wx.CHK_CHECKED)
        else:
            self.select.Set3StateValue(wx.CHK_UNCHECKED)
    
    def OnCheck(self, index, f):
        self.check_state()
    
    def OnSelect(self, event):
        value = event.GetEventObject().Get3StateValue()
        if value == wx.CHK_UNCHECKED:
            self.list.checkAll(False)
        elif value == wx.CHK_CHECKED:
            self.list.checkAll(True)

class RevertDialog(AddDialog):
    def __init__(self, title, path):
        wx.Dialog.__init__(self, Globals.mainframe, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(450, 300))
        self.path = path
        
        self.sizer = box = ui.VBox(namebinding='widget').create(self).auto_layout()
        self.list = CheckList.CheckList(self, columns=[
                (tr("File"), 300, 'left'),
                (tr("Text Status"), 100, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.add(self.list, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        self.list.on_check = self.OnCheck
        
        #add selection switch checkbox
        box.add(ui.Check3D(2, tr('Select / deselect All')), name='select').bind('check', self.OnSelect)
        
        box.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        self.btnOk.SetDefault()
        
        self.init()
        
    def init(self):
        def f():
            import pysvn
            client = pysvn.Client()
            r = client.status(self.path)
            if os.path.isfile(self.path):
                self.path = os.path.dirname(self.path)
            _len = len(self.path)
            for node in r:
                status = str(node['text_status'])
                if  status in ('modified', 'added', 'deleted'):
                    fname = node['path'][_len+1:]
                    if not fname:
                        fname = '.'
                    wx.CallAfter(self.list.addline, [fname, status], flag=True)
    
        wrap_run(f)
        
class CommitDialog(AddDialog):
    def __init__(self, title, path):
        wx.Dialog.__init__(self, Globals.mainframe, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(600, 500))
        self.pref = Globals.pref
        self.path = path
        self.fileinfos = {}
        self.filelist = []
        
        self.sizer = box = ui.VBox(namebinding='widget').create(self).auto_layout()
        
        box1 = box.add(ui.VGroup(tr("Message")))
        box1.add(ui.Button(tr("Recent Messages"))).bind('click', self.OnHisMsg)
        box1.add(ui.MultiText, name='message')

        #add filenames list
        self.list = CheckList.CheckList(self, columns=[
                (tr("File"), 390, 'left'),
                (tr("Extension"), 70, 'left'),
                (tr("Status"), 100, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.add(self.list, proportion=2, flag=wx.EXPAND|wx.ALL, border=5)
        self.list.on_check = self.OnCheck
        
        box.add(
            ui.Check(True, tr('Show unversioned files')), 
            name='chkShowUnVersion').bind('check', self.OnShowUnVersion)
        box.add(
            ui.Check3D(False, tr('Select / deselect All')),
            name='select').bind('check', self.OnSelect)
        
        box.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        self.btnOk.SetDefault()
        
        box.auto_fit(0)
        
        wx.CallAfter(self.init)

    def GetValue(self):
        add_files = []
        files = []
        for i in range(self.list.GetItemCount()):
            if not self.list.getFlag(i):
                continue
            filename, flag = self.fileinfos[self.list.GetItemData(i)]
            if flag:
                files.append(filename)
            else:
                add_files.append(filename)

        #save log
        self.pref.svn_log_history.insert(0, self.message.GetValue())
        del Globals.pref.svn_log_history[30:]
        self.pref.save()
        return {'add_files':add_files, 'files':files, 
            'message':self.message.GetValue()}
    
    def init(self):
        self.filelist = []
        def f():
            import pysvn
            client = pysvn.Client()
            r = client.status(self.path, ignore=True)
            if os.path.isfile(self.path):
                self.path = os.path.dirname(self.path)
            _len = len(self.path)
            for node in r:
                status = str(node['text_status'])
                fname = node['path'][_len+1:]
                if not fname:
                    fname = '.'
                if status != 'normal':
                    self.filelist.append((node['is_versioned'], fname, node['path'],
                        status))
                
            if not self.filelist:
                wx.CallAfter(common.showmessage, tr("No files need to process."))
                return
            
            self.load_data(self.chkShowUnVersion.GetValue())
            
        wrap_run(f)
        
    def load_data(self, unversioned=True):
        color = {
            'added':'#007F05',
            'modified':wx.BLACK,
            'deleted':wx.RED,
        }
        
        self.list.DeleteAllItems()
        self.fileinfos = {}
        
        i = 0
        for flag, fname, filename, f in self.filelist:
            ext = os.path.splitext(fname)[1]
            if flag == False:
                if unversioned:
                    index = self.list.addline([fname, ext, f], False)
                    item = self.list.GetItem(index)
                    item.SetTextColour('#999999')
                    self.list.SetItem(item)
                    self.fileinfos[self.list.GetItemData(index)] = (filename, False)
            else:
                index = self.list.insertline(i, [fname, ext, f], True)
                item = self.list.GetItem(index)
                item.SetTextColour(color.get(f, wx.BLACK))
                self.list.SetItem(item)
                self.fileinfos[self.list.GetItemData(index)] = (filename, True)
                i += 1
        self.check_state()
        
    def OnHisMsg(self, event):
        dlg = wx.SingleChoiceDialog(
                self, tr('Select one log'), tr('Log History'),
                Globals.pref.svn_log_history, 
                wx.CHOICEDLG_STYLE
                )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue(dlg.GetStringSelection())
        dlg.Destroy()
        
    def OnShowUnVersion(self, event):
        wx.CallAfter(self.load_data, event.IsChecked())
            
class ResultDialog(wx.Dialog):
    def __init__(self, title=tr('Result')):
        wx.Dialog.__init__(self, Globals.mainframe, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(600, 300))
        
        self.sizer = box = ui.VBox(namebinding='widget').create(self).auto_layout()
        self.list = CheckList.List(self, columns=[
                (tr("Action"), 120, 'left'),
                (tr("Path"), 400, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.add(self.list, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        box.add(ui.Label, name='message')
        box.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        box.auto_fit(0)
        self.btnOk.Disable()
        self.btnCancel.Enable()
        
    def update_message(self, message):
        wx.CallAfter(self.message.SetLabel, message)
        
    def add(self, data):
        wx.CallAfter(self.list.addline, data)
        
    def finish(self):
        self.btnCancel.Disable()
        self.btnOk.Enable()
