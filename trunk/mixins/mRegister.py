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
#   $Id: mRegister.py 496 2006-01-18 01:05:58Z limodou $

import wx
import os
import sys
from modules import Mixin
from modules.Debug import error
from modules import common


if wx.Platform == '__WXMSW__':
    import _winreg

    def add_mainframe_menu(menulist):
            menulist.extend([ ('IDM_OPTION',
                [
                    (120, 'IDM_OPTION_REGISTER', tr('Register to Explore'), wx.ITEM_NORMAL, 'OnOptionRegister', tr('Registers to explore context menu.')),
                    (130, 'IDM_OPTION_UNREGISTER', tr('Unregister from Explore'), wx.ITEM_NORMAL, 'OnOptionUnRegister', tr('Unregisters from explore context menu.')),
                ]),
            ])
    Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)
    
    def OnOptionRegister(win, event):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
            filename = os.path.basename(sys.argv[0])
            f, ext = os.path.splitext(filename)
            if ext == '.exe':
                command = '"%s" %%L' % os.path.normpath(common.uni_work_file(filename))
            else:
                path = os.path.normpath(common.uni_work_file('%s.pyw' % f))
                execute = sys.executable.replace('python.exe', 'pythonw.exe')
                command = '"%s" "%s" "%%L"' % (execute, path)
            _winreg.SetValue(key, 'NewEdit\\command', _winreg.REG_SZ, command)
            wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            error.traceback()
            wx.MessageDialog(win, tr('Register to explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
    Mixin.setMixin('mainframe', 'OnOptionRegister', OnOptionRegister)
    
    def OnOptionUnRegister(win, event):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteKey(key, 'NewEdit\\command')
            _winreg.DeleteKey(key, 'NewEdit')
            wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            error.traceback()
            wx.MessageDialog(win, tr('Unregister from explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
    Mixin.setMixin('mainframe', 'OnOptionUnRegister', OnOptionUnRegister)
