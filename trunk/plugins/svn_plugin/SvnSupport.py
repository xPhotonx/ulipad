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

from modules import common
import wx
import os
import re
from modules import Globals
from modules import Casing

#commands definition
################################################################
status = {
    '?': tr('non-versioned'),
    'M': tr('modified'),
    'A': tr('added'),
    'D': tr('deleted'),
    ' ': tr('normal'),
    '!': tr('missing'),
    'I': tr('ignored'),
    'C': tr('conflict'),
}

#export functions
################################################################
def do(dirwin, command, *args):
    commands = {
        'update': ('update', dirwin.OnRefresh),
        'checkout':('checkout', None),
        'commit':('commit', dirwin.OnRefresh),
        'list':('list', None),
        'log':('log', None),
        'add':('add', dirwin.OnRefresh),
        'rename':('rename', dirwin.OnRefresh),
        'delete':('delete', dirwin.OnRefresh),
        'revert':('revert', dirwin.OnRefresh),
        'diff':('diff', None),
        'export':('export', None),
        'status':('status', dirwin.OnRefresh),
    }

    m = dirwin.mainframe
    vc_exe = m.pref.svn_exe
    if not vc_exe:
        common.showerror(dirwin, tr('You should set the version control settings\nfirst in Preference Dialog.'))
        return
    
    if not commands.get(command, None):
        common.showerror(dirwin, tr('Unsupported command [%s]') % command)
        return
    
    #when the commands are finished, it should automatically refresh
    callback = None
    if command == 'export':
        path = get_path(dirwin.pref.version_control_export_path)
        dirwin.pref.version_control_export_path = path
        dirwin.pref.save()
        if not path:
            return
        export_path = os.path.join(path, os.path.basename(args[0]))
        if os.path.exists(export_path):
            dlg = wx.MessageDialog(dirwin, tr("The directory is existed, do you want to overwrite it?"), 
                tr("Export"), wx.YES_NO|wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            dlg.Destroy()
            if answer != wx.ID_YES:
                return
            force = '--force'
        else:
            force = ''
            
        args = args + (force, export_path)
    elif command == 'checkout':
        args = check_dialog(dirwin)
        if args:
            args, path = args
            def f():
                dirwin.addpath(os.path.normcase(path))
            callback = f
    elif command == 'commit':
        args = commit_dialog(dirwin, args[0])
        if not args: return
    elif command == 'revert':
        args = revert_dialog(dirwin, args[0])
    elif command == 'rename':
        newname = rename_dialog(dirwin, args[0])
        args = [args[0], newname]
    if not args: return

    command_name, call_func = commands.get(command)
    if callback:
        call_func = callback
    cmd = u'"%s" %s %s' % (vc_exe, command_name, u' '.join(args))
    run_command(cmd, call_func)

#common functions
################################################################
def convert_text(text):
    re_string = re.compile(r'\?\\(\d{3})', re.S|re.M|re.I)
    def do_sub(m):
        return chr(int(m.group(1)))
    if re_string.search(text):
        text = unicode(re.sub(re_string,do_sub, text), 'utf-8')
    else:
        text = common.decode_string(text)
    return text
    
def svn_input_decorator(func):
    def _func(win, text):
        text = convert_text(text)
        return func(win, text)
    return _func
    
def run_command(cmd, callback=None):
    from modules.Debug import error
    def f():
        try:
            Globals.mainframe.RunCommand(cmd, redirect=True, hide=True, 
                input_decorator=svn_input_decorator, callback=callback)
        except:
            error.traceback()
    wx.CallAfter(f)
        
def pipe_command(cmd, callback):
    def _run(cmd):
        o = os.popen(cmd)
        text = convert_text(o.read())
        if callback:
            callback(text)
    d = Casing.Casing(_run, cmd)
    d.start_thread()
  
def get_entries(path):
    cmd = '"%s" status -Nv %s' % (Globals.mainframe.pref.svn_exe, path)
    o = os.popen(cmd)
    text = convert_text(o.read())
    entries = {}
    for line in text.splitlines():
        f = line[0]
        line = line.strip()
        filename = line.split()[-1]
        if filename in ('.', '..'):
            continue
        entries[os.path.basename(filename)] = f
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
    
def rename_dialog(dirwin, path):
    dlg = wx.TextEntryDialog(dirwin, tr('New name'),
        tr('Rename'), path)
    if dlg.ShowModal() == wx.ID_OK:
        newname = dlg.GetValue()
        dlg.Destroy()
        return newname
    
    
def check_dialog(dirwin):
    dialog = [
            ('string', 'url', '', tr('URL of repository:'), None),
            ('dir', 'dir', dirwin.pref.version_control_checkout_path, tr('Checkout Directory'), None),
            (False, 'string', 'revision', '', tr('Revision'), None),
        ]
    from modules.EasyGuider import EasyDialog
    dlg = EasyDialog.EasyDialog(Globals.mainframe, title=tr("Checkout"), elements=dialog)
    values = None
    if dlg.ShowModal() == wx.ID_OK:
        values = dlg.GetValue()
        dirwin.pref.version_control_checkout_path = values['dir']
        dirwin.pref.save()
        if values.get('revision', ''):
            r = '-r ' + values['revision']
        else:
            r = ''
        args = [r, values['url'], values['dir']]
        dlg.Destroy()
        return args, values['dir']
    dlg.Destroy()
    
def commit_dialog(dirwin, path):
    dlg = CommitDialog(dirwin, tr('Commit'), path)
    if dlg.ShowModal() == wx.ID_OK:
        dlg.Destroy()
        return dlg.GetValue()
    dlg.Destroy()
  
def revert_dialog(dirwin, path):
    dlg = RevertDialog(dirwin, tr('Revert'), path)
    if dlg.ShowModal() == wx.ID_OK:
        dlg.Destroy()
        return dlg.GetValue()
    dlg.Destroy()

from modules import CheckList
class CommitDialog(wx.Dialog):
    filetype = 'all'
    def __init__(self, parent, title, files):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(600, -1))
        self.parent = parent
        self.files = files
        self.fileinfos = {}
        self.filelist = []
        box = wx.BoxSizer(wx.VERTICAL)
        
        #add message label and recent messages button
        title = wx.StaticBox(self, -1, tr("Message"))
        box1 = wx.StaticBoxSizer(title, wx.VERTICAL)
        self.ID_HISMSG = wx.NewId()
        self.btnHisMsg = wx.Button(self, self.ID_HISMSG, tr("Recent Messages"))
        box1.Add(self.btnHisMsg, 0, wx.LEFT, 5)
        #add message input box
        self.text = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
        box1.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)
        box.Add(box1, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)

        #add filenames list
        self.filenames = CheckList.CheckList(self, columns=[
                (tr("File"), 390, 'left'),
                (tr("Extension"), 70, 'left'),
                (tr("Status"), 100, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.Add(self.filenames, 2, wx.ALL|wx.EXPAND, 5)
        self.filenames.on_check = self.OnCheck
        
        #add selection switch checkbox
        self.chkShowUnVertion = wx.CheckBox(self, -1, tr('Show unversioned files'))
        if self.filetype == 'all':
            self.chkShowUnVertion.SetValue(True)
        box.Add(self.chkShowUnVertion, 0, wx.LEFT, 5)
        self.chkSelect = wx.CheckBox(self, -1, tr('Select / deselect All'), 
            style=wx.CHK_3STATE)
        box.Add(self.chkSelect, 0, wx.LEFT, 5)
        
        #add ok and cancel buttons
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnOK.SetDefault()
        box2.Add(self.btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        wx.EVT_BUTTON(self.btnHisMsg, self.ID_HISMSG, self.OnHisMsg)
        wx.EVT_CHECKBOX(self.chkShowUnVertion, self.chkShowUnVertion.GetId(), self.OnShowUnVersion)
        wx.EVT_CHECKBOX(self.chkSelect, self.chkSelect.GetId(), self.OnSelect)

        self.SetSizer(box)
        self.SetAutoLayout(True)
        
        wx.CallAfter(self.init)

    def GetValue(self):
        add_files = []
        files = []
        for i in range(self.filenames.GetItemCount()):
            if not self.filenames.getFlag(i):
                continue
            filename, flag = self.fileinfos[self.filenames.GetItemData(i)]
            if flag:
                files.append(filename)
            else:
                add_files.append(filename)
        if add_files:
            vc_exe = Globals.mainframe.pref.svn_exe
            cmd_add = u'"%s" add %s' % (vc_exe, u' '.join(add_files))
            run_command(cmd_add)
            
        #save log
        Globals.pref.svn_log_history.insert(0, self.text.GetValue())
        del Globals.pref.svn_log_history[30:]
        Globals.pref.save()
        return ['-m "%s"' % self.text.GetValue()] + add_files + files
    
    def init(self):
        self.filelist = []
        def _callback(text):
            try:
                self.filenames.Freeze()
                path = os.path.dirname(self.files)
                length = len(path)
                for line in text.splitlines():
                    wx.SafeYield()
                    line = line.strip()
                    if not line: continue
                    filename = line[7:]
                    ext = os.path.splitext(filename)[1]
                    if line[0] == '?':
                        if self.filetype == 'all':
                            self.filelist.append((False, filename[length+1:], filename, line[0]))
                    else:
                        self.filelist.append((True, filename[length+1:], filename, line[0]))
                if not self.filelist:
                    common.showmessage(self, tr("No files need to process."))
                    return
                
                self.load_data(self.filetype == 'all')
            finally:
                self.filenames.Thaw()
                
        cmd = '"%s" status %s' % (self.parent.pref.svn_exe, self.files)
        pipe_command(cmd, _callback)
        
    def check_state(self):
        count = {True:0, False:0}
        for i in range(self.filenames.GetItemCount()):
            count[self.filenames.getFlag(i)] += 1
        if count[True] > 0 and count[False] > 0:
            self.chkSelect.Set3StateValue(wx.CHK_UNDETERMINED)
        elif count[True] > 0 and count[False] == 0:
            self.chkSelect.Set3StateValue(wx.CHK_CHECKED)
        else:
            self.chkSelect.Set3StateValue(wx.CHK_UNCHECKED)
        
    def load_data(self, unversioned=True):
        color = {
            'A':'#007F05',
            'M':wx.BLACK,
            'D':wx.RED,
        }
        try:
            self.filenames.Freeze()
            self.filenames.DeleteAllItems()
            self.fileinfos = {}
            
            i = 0
            for flag, fname, filename, f in self.filelist:
                wx.SafeYield()
                ext = os.path.splitext(fname)[1]
                if flag == False:
                    if unversioned:
                        index = self.filenames.addline([fname, ext, status.get(f, '')], False)
                        item = self.filenames.GetItem(index)
                        item.SetTextColour('#999999')
                        self.filenames.SetItem(item)
                        self.fileinfos[self.filenames.GetItemData(index)] = (filename, False)
                else:
                    index = self.filenames.insertline(i, [fname, ext, status.get(f, '')], True)
                    item = self.filenames.GetItem(index)
                    item.SetTextColour(color.get(f, wx.BLACK))
                    self.filenames.SetItem(item)
                    self.fileinfos[self.filenames.GetItemData(index)] = (filename, True)
                    i += 1
            self.check_state()
        finally:
            self.filenames.Thaw()
        
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
        
    def OnSelect(self, event):
        value = event.GetEventObject().Get3StateValue()
        if value == wx.CHK_UNCHECKED:
            self.filenames.checkAll(False)
        elif value == wx.CHK_CHECKED:
            self.filenames.checkAll(True)
            
    def OnCheck(self, index, f):
        self.check_state()
    
class RevertDialog(CommitDialog):
    filetype = 'ignore'
    def __init__(self, parent, title, files):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(600, 300))
        self.parent = parent
        self.files = files
        self.fileinfos = {}
        self.filelist = []
        box = wx.BoxSizer(wx.VERTICAL)
        self.filenames = CheckList.CheckList(self, columns=[
                (tr("File"), 390, 'left'),
                (tr("Extension"), 70, 'left'),
                (tr("Status"), 100, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.Add(self.filenames, 2, wx.ALL|wx.EXPAND, 5)
        self.filenames.on_check = self.OnCheck
        
        #add selection switch checkbox
        self.chkSelect = wx.CheckBox(self, -1, tr('Select / deselect All'), 
            style=wx.CHK_3STATE)
        box.Add(self.chkSelect, 0, wx.LEFT, 5)
        
        #add ok and cancel buttons
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnOK.SetDefault()
        box2.Add(self.btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)
    
        self.SetSizer(box)
        self.SetAutoLayout(True)
        
        wx.EVT_CHECKBOX(self.chkSelect, self.chkSelect.GetId(), self.OnSelect)
        
        wx.CallAfter(self.init)

    def GetValue(self):
        files = []
        for i in range(self.filenames.GetItemCount()):
            if not self.filenames.getFlag(i):
                continue
            filename, flag = self.fileinfos[self.filenames.GetItemData(i)]
            files.append(filename)
        return files
    