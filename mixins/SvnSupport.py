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

from modules import common
import wx
import os
from modules import Globals
from modules import Casing

commands = {
    'update': 'update',
    'checkout':'checkout',
    'commit':'commit',
    'list':'list',
    'log':'log',
    'add':'add',
    'rename':'rename',
    'delete':'delete',
    'revert':'revert',
    'diff':'diff',
    'export':'export --force',
    'status':'status',
}

def svn_input_decorator(func):
    def _func(win, text):
        import re
        re_string = re.compile(r'\?\\(\d{3})', re.S|re.M|re.I)
        def do_sub(m):
            return chr(int(m.group(1)))
        print type(text), text
        text = unicode(re.sub(re_string,do_sub, text), 'utf-8')
        return func(win, text)
    return _func
    
def run_command(cmd):
    wx.CallAfter(Globals.mainframe.RunCommand, cmd, redirect=True, hide=True, 
        input_decorator=None)
    
def do(dirwin, command, *args):
    m = dirwin.mainframe
    vc_exe = m.pref.version_control_exe
    if not vc_exe:
        common.showerror(dirwin, tr('You should set the version control settings\nfirst in Preference Dialog.'))
        return
    
    if not commands.get(command, None):
        common.showerror(dirwin, tr('Unsupported command [%s]') % command)
        return
    
    if command == 'export':
        path = get_path(dirwin.pref.version_control_export_path)
        dirwin.pref.version_control_export_path = path
        dirwin.pref.save()
        if not path:
            return
        args = args + (os.path.join(path, os.path.basename(args[0])),)
    elif command == 'checkout':
        args = check_dialog(dirwin)
    elif command == 'commit':
        args = commit_dialog(dirwin, args[0])
        if not args: return
    elif command == 'revert':
        args = revert_dialog(dirwin, args[0])
    elif command == 'rename':
        newname = rename_dialog(dirwin, args[0])
        args = [args[0], newname]
    if not args: return
    cmd = '"%s" %s %s' % (vc_exe, commands.get(command), ' '.join(args))
    run_command(cmd)

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
        return args
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
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(self, -1, label=tr('Message')), 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.text = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
        box.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)
        self.filenames = CheckList.CheckList(self, columns=[
                (tr("File"), 430, 'left'),
                (tr("Status"), 130, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.Add(self.filenames, 2, wx.ALL|wx.EXPAND, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnOK.SetDefault()
        box2.Add(self.btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)

        self.SetSizer(box)
        self.SetAutoLayout(True)
        
        d = Casing.Casing(self.init)
        wx.CallAfter(d.start_thread)

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
            vc_exe = Globals.mainframe.pref.version_control_exe
            cmd_add = '"%s" add %s' % (vc_exe, ' '.join(add_files))
            run_command(cmd_add)
        return ['-m "%s"' % self.text.GetValue()] + add_files + files

    def init(self):
        status = {
            '?': tr('non-versioned'),
            'M': tr('modified'),
            'A': tr('added'),
            'D': tr('deleted'),
        }
        cmd = '"%s" status %s' % (self.parent.pref.version_control_exe, self.files)
        path = os.path.dirname(self.files)
        o = os.popen(cmd)
        def f():
            i = 0
            for line in o:
                line = line.strip()
                if not line: continue
                filename = line[7:]
                if line[0] == '?':
                    if self.filetype == 'all':
                        index = self.filenames.addline([filename[1+len(path):], status.get(line[0], '')], False)
                        self.fileinfos[self.filenames.GetItemData(index)] = (filename, False)
                else:
                    index = self.filenames.insertline(i, [filename[1+len(path):], status.get(line[0], '')], True)
                    self.fileinfos[self.filenames.GetItemData(index)] = (filename, True)
                    i += 1
        wx.CallAfter(f)
        
class RevertDialog(CommitDialog):
    filetype = 'm'
    def __init__(self, parent, title, files):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title, size=(600, 300))
        self.parent = parent
        self.files = files
        self.fileinfos = {}
        box = wx.BoxSizer(wx.VERTICAL)
        self.filenames = CheckList.CheckList(self, columns=[
                (tr("File"), 430, 'left'),
                (tr("Status"), 130, 'left'),
                ], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        box.Add(self.filenames, 2, wx.ALL|wx.EXPAND, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnOK.SetDefault()
        box2.Add(self.btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)
    
        self.SetSizer(box)
        self.SetAutoLayout(True)
        
        d = Casing.Casing(self.init)
        wx.CallAfter(d.start_thread)

    def GetValue(self):
        files = []
        for i in range(self.filenames.GetItemCount()):
            if not self.filenames.getFlag(i):
                continue
            filename, flag = self.fileinfos[self.filenames.GetItemData(i)]
            files.append(filename)
        return files
    