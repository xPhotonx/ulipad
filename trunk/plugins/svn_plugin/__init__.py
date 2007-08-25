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

import wx
from modules import Mixin
import os

def pref_init(pref):
    pref.svn_exe = ''
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Version'), 100, 'text', 'svn_exe', tr('Select location of subversion client'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def other_popup_menu(dirwin, projectname, menus):
    from modules import common
    
    item = dirwin.tree.GetSelection()
    if not item.IsOk(): return
    is_svn_dir = detect_svn(common.getCurrentDir(dirwin.get_node_filename(item)))
    menus.extend([ (None,
        [
            (93.3, 'IDPM_VC_COMMANDS', tr('SVN Commands'), wx.ITEM_NORMAL, '', ''),
            (93.4, '', '-', wx.ITEM_SEPARATOR, None, ''),
        ]),
        ('IDPM_VC_COMMANDS',
        [
            (900, 'IDPM_VC_COMMANDS_SETTINGS', tr('Settings'), wx.ITEM_NORMAL, 'OnVC_Settings', ''),
        ]),
    ])
    
    if is_svn_dir:
        menus.extend([ (None,
            [
                (93.1, 'IDPM_VC_UPDATE', tr('SVN Update'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (93.2, 'IDPM_VC_COMMIT', tr('SVN Commit'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            ]),
            ('IDPM_VC_COMMANDS',
            [
                (100, 'IDPM_VC_COMMANDS_LIST', tr('List'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (110, 'IDPM_VC_COMMANDS_SHOWLOG', tr('Show log'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (120, 'IDPM_VC_COMMANDS_STATUS', tr('Status'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (130, 'IDPM_VC_COMMANDS_DIFF', tr('Diff'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (145, '', '-', wx.ITEM_SEPARATOR, None, ''),
                (150, 'IDPM_VC_COMMANDS_ADD', tr('Add'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (160, 'IDPM_VC_COMMANDS_RENAME', tr('Rename'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (170, 'IDPM_VC_COMMANDS_DELETE', tr('Delete'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (180, 'IDPM_VC_COMMANDS_REVERSE', tr('Revert'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (190, '', '-', wx.ITEM_SEPARATOR, None, ''),
                (200, 'IDPM_VC_COMMANDS_EXPORT', tr('Export'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
                (210, '', '-', wx.ITEM_SEPARATOR, None, ''),
                (220, 'IDPM_VC_COMMANDS_SETTINGS', tr('Settings'), wx.ITEM_NORMAL, 'OnVC_Settings', ''),
            ]),
        ])
    else:
        menus.extend([ (None,
            [
                (93, 'IDPM_VC_CHECKOUT', tr('SVN Checkout'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            ]),
        ])
Mixin.setPlugin('dirbrowser', 'other_popup_menu', other_popup_menu)

def OnVC_DoCommand(win, event):
    mapping = {
        'IDPM_VC_CHECKOUT':'checkout',
        'IDPM_VC_COMMIT':'commit',
        'IDPM_VC_UPDATE':'update',
        'IDPM_VC_COMMANDS_LIST':'list',
        'IDPM_VC_COMMANDS_STATUS':'status',
        'IDPM_VC_COMMANDS_SHOWLOG':'log',
        'IDPM_VC_COMMANDS_ADD':'add',
        'IDPM_VC_COMMANDS_RENAME':'rename',
        'IDPM_VC_COMMANDS_DELETE':'delete',
        'IDPM_VC_COMMANDS_REVERSE':'revert',
        'IDPM_VC_COMMANDS_DIFF':'diff',
        'IDPM_VC_COMMANDS_EXPORT':'export',
    }
    item = win.tree.GetSelection()
    if item.IsOk():
        path = win.get_node_filename(item)
    else:
        path = ''
    import SvnSupport as vc
    _id = event.GetId()
    for id, cmd in mapping.items():
        if _id == getattr(win, id, None):
            vc.do(win, cmd, path)
Mixin.setMixin('dirbrowser', 'OnVC_DoCommand', OnVC_DoCommand)

def OnVC_Settings(win, event):
    dialog = [
            ('openfile', 'svn_exe', win.pref.svn_exe, tr('Select location of subversion client'), None),
        ]
    from modules.EasyGuider import EasyDialog
    dlg = EasyDialog.EasyDialog(win.mainframe, title=tr("SVN Settings"), elements=dialog)
    values = None
    if dlg.ShowModal() == wx.ID_OK:
        values = dlg.GetValue()
        win.pref.svn_exe = values['svn_exe']
        win.pref.save()
    dlg.Destroy()
Mixin.setMixin('dirbrowser', 'OnVC_Settings', OnVC_Settings)

#functions
########################################################

def detect_svn(path):
    if os.path.exists(os.path.join(path, '.svn')):
        return True