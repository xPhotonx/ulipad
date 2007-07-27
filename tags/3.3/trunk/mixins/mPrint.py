#       Programmer:     limodou
#       E-mail:         limodou@gmail.com
#
#       Copyleft 2006 limodou
#
#       Distributed under the terms of the GPL (GNU Public License)
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
#       $Id: mPrint.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'print'

import wx
import os
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_FILE',
        [
            (200, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (210, 'IDM_FILE_PRINT_MENU', tr('Print'), wx.ITEM_NORMAL, '', None),
        ]),
        ('IDM_FILE_PRINT_MENU',
        [
            (100, 'wx.ID_PRINT_SETUP', tr('Page Setup...'), wx.ITEM_NORMAL, 'OnFilePageSetup', tr('Set page layout and options.')),
#            (110, 'IDM_FILE_PRINTER_SETUP', tr('Printer Setup...'), wx.ITEM_NORMAL, 'OnFilePrinterSetup', tr('Selects a printer and printer connection.')),
            (120, 'wx.ID_PREVIEW', tr('Print Preview...'), wx.ITEM_NORMAL, 'OnFilePrintPreview', tr('Displays the document on the screen as it would appear printed.')),
            (130, 'wx.ID_PRINT', tr('Print...'), wx.ITEM_NORMAL, 'OnFilePrint', tr('Prints a document.')),
            (140, 'IDM_FILE_HTML', tr('Html File'), wx.ITEM_NORMAL, '', None),
        ]),
        ('IDM_FILE_HTML',
        [
            (100, 'IDM_FILE_HTML_PRINT_PREVIEW', tr('Html File Preview...'), wx.ITEM_NORMAL, 'OnFileHtmlPreview', tr('Displays the html document on the screen as it would appear printed.')),
            (110, 'IDM_FILE_HTML_PRINT', tr('Html File Print...'), wx.ITEM_NORMAL, 'OnFileHtmlPrint', tr('Prints a html document.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (125, 'print'),
    ])

    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'print':(wx.ITEM_NORMAL, 'wx.ID_PRINT', 'images/printer.gif', tr('print'), tr('Prints a document.'), 'OnFilePrint'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def mainframe_init(win):
    from Print import MyPrinter

    win.printer = MyPrinter(win)
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def OnFilePageSetup(win, event):
    win.printer.PageSetup()
Mixin.setMixin('mainframe', 'OnFilePageSetup', OnFilePageSetup)

def OnFilePrint(win, event):
    win.printer.PrintText(win.printer.convertText(win.document.GetText()), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFilePrint', OnFilePrint)

def OnFilePrintPreview(win, event):
    win.printer.PreviewText(win.printer.convertText(win.document.GetText()), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFilePrintPreview', OnFilePrintPreview)

#def OnFilePrinterSetup(win, event):
#       win.printer.PrinterSetup()
#Mixin.setMixin('mainframe', 'OnFilePrinterSetup', OnFilePrinterSetup)

def OnFileHtmlPreview(win, event):
    win.printer.PreviewText(win.document.GetText(), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFileHtmlPreview', OnFileHtmlPreview)

def OnFileHtmlPrint(win, event):
    win.printer.PrintText(win.document.GetText(), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFileHtmlPrint', OnFileHtmlPrint)
