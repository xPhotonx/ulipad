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

from modules import common
import wx
import os
import re
from modules import Globals
from modules import Casing

#commands definition
################################################################
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
    'export':'export',
    'status':'status',
}

#export functions
################################################################
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
    elif command == 'commit':
        args = commit_dialog(dirwin, args[0])
        if not args: return
    elif command == 'revert':
        args = revert_dialog(dirwin, args[0])
    elif command == 'rename':
        newname = rename_dialog(dirwin, args[0])
        args = [args[0], newname]
    if not args: return
    cmd = u'"%s" %s %s' % (vc_exe, commands.get(command), u' '.join(args))
    run_command(cmd, dirwin.OnRefresh)

#common functions
################################################################
def convert_text(text):
    re_string = re.compile(r'\?\\(\d{3})', re.S|re.M|re.I)
    def do_sub(m):
        return chr(int(m.group(1)))
    if re_string.search(text):
        text = unicode(re.sub(re_string,do_sub, text), 'utf-8')
    else:
        text = common.decode_string(text, common.defaultfilesystemencoding)
    return text
    
def svn_input_decorator(func):
    def _func(win, text):
        text = convert_text(text)
        return func(win, text)
    return _func
    
def run_command(cmd, callback=None):
    wx.CallAfter(Globals.mainframe.RunCommand, cmd, redirect=True, hide=True, 
        input_decorator=svn_input_decorator, callback=callback)
        
def pipe_command(cmd, callback):
    def _run(cmd):
        o = os.popen(cmd)
        text = convert_text(o.read())
        if callback:
            callback(text)
    d = Casing.Casing(_run, cmd)
    d.start_thread()
  
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
                (tr("File"), 410, 'left'),
                (tr("Extension"), 80, 'left'),
                (tr("Status"), 100, 'left'),
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
            vc_exe = Globals.mainframe.pref.version_control_exe
            cmd_add = u'"%s" add %s' % (vc_exe, u' '.join(add_files))
            run_command(cmd_add)
        return ['-m "%s"' % self.text.GetValue()] + add_files + files

    def init(self):
        def _callback(text):
            status = {
                '?': tr('non-versioned'),
                'M': tr('modified'),
                'A': tr('added'),
                'D': tr('deleted'),
            }
            path = os.path.dirname(self.files)
            i = 0
            for line in text.splitlines():
                wx.SafeYield()
                line = line.strip()
                if not line: continue
                filename = common.decode_string(line[7:], common.defaultfilesystemencoding)
                ext = os.path.splitext(filename)[1]
                if line[0] == '?':
                    if self.filetype == 'all':
                        index = self.filenames.addline([filename[1+len(path):], ext, status.get(line[0], '')], False)
                        self.fileinfos[self.filenames.GetItemData(index)] = (filename, False)
                else:
                    index = self.filenames.insertline(i, [filename[1+len(path):], ext, status.get(line[0], '')], True)
                    self.fileinfos[self.filenames.GetItemData(index)] = (filename, True)
                    i += 1
        cmd = '"%s" status %s' % (self.parent.pref.version_control_exe, self.files)
        pipe_command(cmd, _callback)
        
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
        
        wx.CallAfter(self.init)

    def GetValue(self):
        files = []
        for i in range(self.filenames.GetItemCount()):
            if not self.filenames.getFlag(i):
                continue
            filename, flag = self.fileinfos[self.filenames.GetItemData(i)]
            files.append(filename)
        return files
    