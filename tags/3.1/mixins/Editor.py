#   Programmer: limodou
#   E-mail:     chatme@263.net
#
#   Copyleft 2004 limodou
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
#   $Id: Editor.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import wx.stc
from modules import makemenu
from modules import Id
from modules.Debug import error
import os
import DocumentBase
from modules import common
#import threading
#import Queue
#import time

keylist = {
    'DOWN'  :wx.stc.STC_KEY_DOWN,
    'UP'    :wx.stc.STC_KEY_UP,
    'LEFT'  :wx.stc.STC_KEY_LEFT,
    'RIGHT' :wx.stc.STC_KEY_RIGHT,
    'HOME'  :wx.stc.STC_KEY_HOME,
    'END'   :wx.stc.STC_KEY_END,
    'PGUP'  :wx.stc.STC_KEY_PRIOR,
    'PGDN'  :wx.stc.STC_KEY_NEXT,
    'DEL'   :wx.stc.STC_KEY_DELETE,
    'INS'   :wx.stc.STC_KEY_INSERT,
    'ESC'   :wx.stc.STC_KEY_ESCAPE,
    'BACK'  :wx.stc.STC_KEY_BACK,
    'TAB'   :wx.stc.STC_KEY_TAB,
    'ENTER' :wx.stc.STC_KEY_RETURN,
    'PLUS'  :wx.stc.STC_KEY_ADD,
    '-'     :wx.stc.STC_KEY_SUBTRACT,
    '/'     :wx.stc.STC_KEY_DIVIDE,
}

#class OpenFileThread(threading.Thread):
#   def __init__(self, mainframe, filename, q, error):
#       threading.Thread.__init__(self)
#       self.filename = filename
#       self.q = q
#       self.mainframe = mainframe
#       self.setDaemon(True)
#
#   def run(self):
#       import os.path
#
#       blocksize = 1024 * 8
#
#       buf = []
#       filesize = os.path.getsize(self.filename)
#       nsize = filesize / blocksize
#       if filesize % blocksize:
#           nsize += 1
#       f = None
#       try:
#           try:
#               f = open(self.filename, 'rb')
#               for i in range(nsize):
#                   text = f.read(blocksize)
#                   buf.append(text)
#                   self.updateProgress((i+1)*100/nsize)
#           except:
#               error.traceback()
#               self.q.put(None)
#               return
#       finally:
#           self.mainframe.ThreadSafeDispatch(self.mainframe.progressbar.SetValue, 0)
#           if f:
#               f.close()
#       self.q.put(''.join(buf))
#
#   def updateProgress(self, i):
#       self.mainframe.ThreadSafeDispatch(self.mainframe.progressbar.SetValue, i)
#

class TextEditor(wx.stc.StyledTextCtrl, Mixin.Mixin, DocumentBase.DocumentBase):

    __mixinname__ = 'editor'
    fid = 1
    popmenulist = []
    imagelist = {}

    def __init__(self, parent, editctrl, filename, documenttype):
        self.initmixin()

        DocumentBase.DocumentBase.__init__(self, parent, filename, documenttype)

        wx.stc.StyledTextCtrl.__init__(self, parent, -1)

        self.parent = parent
        self.editctrl = editctrl
        self.mainframe = self.editctrl.mainframe
        self.app = self.mainframe.app
        self.pref = self.mainframe.pref
        if filename == '':
            self.fileid = TextEditor.fid
            TextEditor.fid += 1
        self.mwidth = 0     #max line number
        self.settext = False
        self.canedit = True

        self.defaultlocale = self.app.defaultencoding

        #editor style
        self.SetMargins(2,2)        #set left and right outer margins to 0 width
        self.setLineNumberMargin()
        self.SetMarginMask(1, 0)    #cann't place any marker in margin 1
        self.SetMarginWidth(0, 0)   #used as symbol
        self.SetMarginWidth(2, 0)   #used as folder

        #set caret width
        self.SetCaretWidth(3)
        #set caret color
        self.SetCaretForeground('red')

        #set selection background color
        self.SetSelBackground(1, 'navy')
        self.SetSelForeground(1, 'white')

        #inter modify flag
        self.modified = False

        #init key short cut
        self.initKeyShortCut()

        #set backspace to unindent
        self.SetBackSpaceUnIndents(True)

        #set scroll bar range
        self.SetEndAtLastLine(False)

        #set style
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%s,size:10" % font.GetFaceName())
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "back:#AAFFAA,face:%s,size:10" % font.GetFaceName())

        #move caret
        self.SetFocus()

        #make popup menu
        self.popmenu = None
#       self.popmenu = makemenu.makepopmenu(self, TextEditor.popmenulist, TextEditor.imagelist)

        wx.stc.EVT_STC_MODIFIED(self, self.GetId(), self.OnModified)
        wx.stc.EVT_STC_MARGINCLICK(self, self.GetId(), self.OnMarginClick)
        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_CHAR(self, self.OnChar)
        wx.EVT_RIGHT_DOWN(self, self.OnPopUp)

        #set some flags
        self.cansavefileflag = True
        self.needcheckfile = True
        self.savesession = True
        self.canopenfileflag = True

        self.callplugin('init', self)
        
    def isModified(self):
        return self.modified or self.GetModify()

    def canopenfile(self, filename):
        if (self.filename == '') and self.canopenfileflag and not self.isModified():
            return True
        else:
            return False

    def openfile(self, filename, encoding=None, delay=False, defaulttext=''):
        if delay:
            self.filename = filename
            self.encoding = encoding
            self.opened = False

            return

        self.callplugin('openfile', self, filename)

        oldfilename = self.filename
        self.filename = filename

        if filename:
            stext = []
            flag = self.execplugin('readfiletext', self, filename, stext)
            if not flag:
                try:
                    f = open(filename, 'rb')
                    text = f.read()
                    f.close()
                except:
                    error.traceback()
                    raise
#               q = Queue.Queue()
#               t = OpenFileThread(self.mainframe, filename, q, error)
#               t.start()
#               while 1:
#                   try:
#                       wx.GetApp().Yield()
#                       text = q.get_nowait()
#                       break
#                   except:
#                       pass
#               if not text:
#                   raise Exception, tr("Open file error!")
            else:
                text = stext[0]
                if text is None:
                    raise

            stext = [text]
            #stext is a list of the file text. To get the file text you can use
            #stext[0]. Then you can reset the value in order to change the text
            try:
                self.callplugin('openfileencoding', self, stext, encoding)
                self.callplugin('openfiletext', self, stext)
            except:
                error.traceback()
                self.filename = oldfilename
                raise

            self.settext = True
            self.SetText(stext[0])
            self.EmptyUndoBuffer()
            self.SetSavePoint()
            self.settext = False
        else:
            if defaulttext:
                self.settext = True
                self.SetText(defaulttext)
                self.EmptyUndoBuffer()
                self.SetSavePoint()
                self.settext = False

        self.callplugin('afteropenfile', self, filename)

        self.opened = True

    def savefile(self, filename, encoding):
        self.callplugin('savefile', self, filename)

        oldfilename = self.filename
        self.filename = filename

        #call plugin to process text
        stext = [self.GetText()]

        try:
            self.callplugin('savefileencoding', self, stext, encoding)
            self.callplugin('savefiletext', self, stext)
        except:
            error.traceback()
            self.filename = oldfilename
            raise

        flag = self.execplugin('writefiletext', self, filename, stext[0])
        if not flag:
            #test if the file can be write
            tmp = filename + '.tmp'
            f = file(tmp, 'wb')
            f.write(stext[0])
            f.close()

            if os.path.exists(filename):
                os.remove(filename)
            os.rename(tmp, filename)

            self.SetSavePoint()
            self.modified = False
            wx.CallAfter(self.editctrl.showTitle, self)
        else:
            f, ff = flag
            if ff:
                self.SetSavePoint()
                self.modified = False
                wx.CallAfter(self.editctrl.showTitle, self)

        self.callplugin('aftersavefile', self, filename)

    def getIndentChar(self):
        if self.GetUseTabs():
            return '\t'
        else:
            return ' ' * self.GetTabWidth()

    def getFilename(self):
        if self.title:
            return self.title

        if self.filename:
            return self.filename
        else:
            return 'Untitled %d' % self.fileid

    def getEOLChar(self):
        if self.eolmode == 2:
            eolchar = '\r'
        elif self.eolmode == 1:
            eolchar = '\r\n'
        else:
            eolchar = '\n'
        return eolchar

    def hasSelection(self):
        start, end = self.GetSelection()
        return (end - start) > 0

    def getSelectionLines(self):
        if self.hasSelection():
            start, end = self.GetSelection()
            startline = self.LineFromPosition(start)
            endline = self.LineFromPosition(end)
            text = self.GetSelectedText()
            if text[-1] == self.getEOLChar()[-1]:
                endline -= 1
            return range(startline, endline + 1)
        else:
            return [self.GetCurrentLine()]

    def getLineText(self, line):
        """not include the end line char"""
        start = self.PositionFromLine(line)
        end = self.GetLineEndPosition(line)
        text = self.GetTextRange(start, end)
        return text

    def getChar(self, pos):
        return chr(self.GetCharAt(pos))

    def getRawText(self):
        if wx.USE_UNICODE:
            return self.GetText().encode('utf-8')
        else:
            return self.GetText()

    def OnUpdateUI(self, event):
        self.callplugin('on_update_ui', self, event)

    def OnModified(self, event):
        if self.documenttype == 'edit' and not self.settext:
            if not self.isModified():
                self.SetSavePoint()
            wx.CallAfter(self.editctrl.showTitle, self)
            wx.CallAfter(self.editctrl.showPageTitle, self)
        self.setLineNumberMargin()
        self.callplugin('on_modified', self, event)

    def OnMarginClick(self, event):
        self.callplugin('on_margin_click', self, event)

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        f = wx.ACCEL_NORMAL
        if event.ControlDown():
            f |= wx.ACCEL_CTRL
        if event.ShiftDown():
            f |= wx.ACCEL_SHIFT
        if event.AltDown():
            f |= wx.ACCEL_ALT

        if self.mainframe.editorkeycodes.has_key((f, key)):
            idname, func = self.mainframe.editorkeycodes[(f, key)]
            fu = getattr(self.mainframe, func)
            id = Id.makeid(self.mainframe, idname)
            event.SetId(id)
            fu(event)
            return

        if not self.execplugin('on_key_down', self, event):
            event.Skip()

    def OnChar(self, event):
        if not self.execplugin('on_char', self, event):
            event.Skip()

    def getLinePositionTuple(self, pos=None):
        if pos == None:
            pos = self.GetCurrentPos()
        line = self.LineFromPosition(pos)
        start = self.PositionFromLine(line)
        end = start + self.LineLength(line)
        return start, end

    def replaceLineText(self, line, text):
        start = self.PositionFromLine(line)
        end = self.GetLineEndPosition(line)
        self.SetTargetStart(start)
        self.SetTargetEnd(end)
        self.ReplaceTarget(text)

    def initKeyShortCut(self):
        self.CmdKeyClearAll()

        action = [

#       wxSTC_CMD_BACKTAB Dedent the selected lines
            ('Shift+Tab', wx.stc.STC_CMD_BACKTAB),
#       wxSTC_CMD_CANCEL Cancel any modes such as call tip or auto-completion list display
            ('Esc', wx.stc.STC_CMD_CANCEL),
#       wxSTC_CMD_CHARLEFT Move caret left one character
            ('Left', wx.stc.STC_CMD_CHARLEFT),
#       wxSTC_CMD_CHARLEFTEXTEND Move caret left one character extending selection to new caret position
            ('Shift+Left', wx.stc.STC_CMD_CHARLEFTEXTEND),
#       wxSTC_CMD_CHARRIGHT Move caret right one character
            ('Right', wx.stc.STC_CMD_CHARRIGHT),
#       wxSTC_CMD_CHARRIGHTEXTEND Move caret right one character extending selection to new caret position
            ('Shift+Right', wx.stc.STC_CMD_CHARRIGHTEXTEND),
#       wxSTC_CMD_CLEAR
            ('Del', wx.stc.STC_CMD_CLEAR),
#       wxSTC_CMD_COPY Copy the selection to the clipboard
#           ('Ctrl+C', wx.stc.STC_CMD_COPY),
#       wxSTC_CMD_CUT Cut the selection to the clipboard
#           ('Ctrl+X', wx.stc.STC_CMD_CUT),
#       wxSTC_CMD_DELETEBACK Delete the selection or if no selection, the character before the caret
            ('Back', wx.stc.STC_CMD_DELETEBACK),
#       wxSTC_CMD_DELETEBACKNOTLINE Delete the selection or if no selection, the character before the caret. Will not delete the character before at the start of a line.
#       wxSTC_CMD_DELWORDLEFT Delete the word to the left of the caret
            ('Ctrl+Back', wx.stc.STC_CMD_DELWORDLEFT),
#       wxSTC_CMD_DELWORDRIGHT Delete the word to the right of the caret
            ('Ctrl+Del', wx.stc.STC_CMD_DELWORDRIGHT),
#       wxSTC_CMD_DOCUMENTEND Move caret to last position in document
            ('Ctrl+End', wx.stc.STC_CMD_DOCUMENTEND),
#       wxSTC_CMD_DOCUMENTENDEXTEND Move caret to last position in document extending selection to new caret position
            ('Ctrl+Shift+End', wx.stc.STC_CMD_DOCUMENTENDEXTEND),
#       wxSTC_CMD_DOCUMENTSTART Move caret to first position in document
            ('Ctrl+Home', wx.stc.STC_CMD_DOCUMENTSTART),
#       wxSTC_CMD_DOCUMENTSTARTEXTEND Move caret to first position in document extending selection to new caret position
            ('Ctrl+Shift+Home', wx.stc.STC_CMD_DOCUMENTSTARTEXTEND),
#       wxSTC_CMD_EDITTOGGLEOVERTYPE Switch from insert to overtype mode or the reverse
            ('Ins', wx.stc.STC_CMD_EDITTOGGLEOVERTYPE),
#       wxSTC_CMD_FORMFEED Insert a Form Feed character
#       wxSTC_CMD_HOME Move caret to first position on line
#       wxSTC_CMD_HOMEDISPLAY Move caret to first position on display line
#           ('Shift+Home', wx.stc.STC_CMD_HOMEDISPLAY),
#       wxSTC_CMD_HOMEDISPLAYEXTEND Move caret to first position on display line extending selection to new caret position
#           ('Shift+Alt+Home', wx.stc.STC_CMD_HOMEDISPLAYEXTEND),
#       wxSTC_CMD_HOMEEXTEND Move caret to first position on line extending selection to new caret position
#       wxSTC_CMD_LINECUT Cut the line containing the caret
            ('Ctrl+Shift+D', wx.stc.STC_CMD_LINECUT),
#       wxSTC_CMD_LINEDELETE Delete the line containing the caret
            ('Ctrl+D', wx.stc.STC_CMD_LINEDELETE),
#       wxSTC_CMD_LINEDOWN Move caret down one line
            ('Down', wx.stc.STC_CMD_LINEDOWN),
#       wxSTC_CMD_LINEDOWNEXTEND Move caret down one line extending selection to new caret position
            ('Shift+Down', wx.stc.STC_CMD_LINEDOWNEXTEND),
#       wxSTC_CMD_LINEEND Move caret to last position on line
#       wxSTC_CMD_LINEENDDISPLAY Move caret to last position on display line
            ('End', wx.stc.STC_CMD_LINEENDDISPLAY),
#       wxSTC_CMD_LINEENDDISPLAYEXTEND Move caret to last position on display line extending selection to new caret position
            ('Shift+End', wx.stc.STC_CMD_LINEENDDISPLAYEXTEND),
#       wxSTC_CMD_LINEENDEXTEND Move caret to last position on line extending selection to new caret position
#       wxSTC_CMD_LINESCROLLDOWN Scroll the document down, keeping the caret visible
            ('Ctrl+Down', wx.stc.STC_CMD_LINESCROLLDOWN),
#       wxSTC_CMD_LINESCROLLUP Scroll the document up, keeping the caret visible
            ('Ctrl+Up', wx.stc.STC_CMD_LINESCROLLUP),
#       wxSTC_CMD_LINETRANSPOSE Switch the current line with the previous
            ('Alt+S', wx.stc.STC_CMD_LINETRANSPOSE),
#       wxSTC_CMD_LINEUP Move caret up one line
            ('Up', wx.stc.STC_CMD_LINEUP),
#       wxSTC_CMD_LINEUPEXTEND Move caret up one line extending selection to new caret position
            ('Shift+Up', wx.stc.STC_CMD_LINEUPEXTEND),
#       wxSTC_CMD_LOWERCASE Transform the selection to lower case
#           ('Ctrl+L', wx.stc.STC_CMD_LOWERCASE),
#       wxSTC_CMD_NEWLINE Insert a new line, may use a CRLF, CR or LF depending on EOL mode
            ('Enter', wx.stc.STC_CMD_NEWLINE),
#       wxSTC_CMD_PAGEDOWN Move caret one page down
            ('Pgdn', wx.stc.STC_CMD_PAGEDOWN),
#       wxSTC_CMD_PAGEDOWNEXTEND Move caret one page down extending selection to new caret position
            ('Shift+Pgdn', wx.stc.STC_CMD_PAGEDOWNEXTEND),
#       wxSTC_CMD_PAGEUP Move caret one page up
            ('Pgup', wx.stc.STC_CMD_PAGEUP),
#       wxSTC_CMD_PAGEUPEXTEND Move caret one page up extending selection to new caret position
            ('Shift+Pgup', wx.stc.STC_CMD_PAGEUPEXTEND),
#       wxSTC_CMD_REDO Redoes the next action on the undo history
#           ('Ctrl+Y', wx.stc.STC_CMD_REDO),
#       wxSTC_CMD_SELECTALL Select all the text in the document
#           ('Ctrl+A', wx.stc.STC_CMD_SELECTALL),
#       wxSTC_CMD_TAB If selection is empty or all on one line replace the selection with a tab character. If more than one line selected, indent the lines
            ('Tab', wx.stc.STC_CMD_TAB),
#       wxSTC_CMD_UNDO Redoes the next action on the undo history
#           ('Ctrl+Z', wx.stc.STC_CMD_UNDO),
#       wxSTC_CMD_UPPERCASE Transform the selection to upper case
#           ('Ctrl+U', wx.stc.STC_CMD_UPPERCASE),
#       wxSTC_CMD_VCHOME Move caret to before first visible character on line. If already there move to first character on line
            ('Home', wx.stc.STC_CMD_VCHOME),
#       wxSTC_CMD_VCHOMEEXTEND Like VCHome but extending selection to new caret position
            ('Shift+Home', wx.stc.STC_CMD_VCHOMEEXTEND),
#       wxSTC_CMD_WORDLEFT Move caret left one word
            ('Ctrl+Left', wx.stc.STC_CMD_WORDLEFT),
#       wxSTC_CMD_WORDLEFTEXTEND Move caret left one word extending selection to new caret position
            ('Ctrl+Shift+Left', wx.stc.STC_CMD_WORDLEFTEXTEND),
#       wxSTC_CMD_WORDRIGHT Move caret right one word
            ('Ctrl+Right', wx.stc.STC_CMD_WORDRIGHT),
#       wxSTC_CMD_WORDRIGHTEXTEND Move caret right one word extending selection to new caret position
            ('Ctrl+Shift+Right', wx.stc.STC_CMD_WORDRIGHTEXTEND),
#       wxSTC_CMD_ZOOMIN Magnify the displayed text by increasing the sizes by 1 point
#           ('Ctrl+B', wx.stc.STC_CMD_ZOOMIN),
#       wxSTC_CMD_ZOOMOUT Make the displayed text smaller by decreasing the sizes by 1 point
#           ('Ctrl+N', wx.stc.STC_CMD_ZOOMOUT),
#       wxSTC_CMD_DELLINELEFT: Use 2395 Delete back from the current position to the start of the line
            ('Alt+Back', wx.stc.STC_CMD_DELLINELEFT),
#       wxSTC_CMD_DELLINERIGHT: Use 2396 Delete forwards from the current position to the end of the line
            ('Alt+Del', wx.stc.STC_CMD_DELLINERIGHT),
#       wxSTC_CMD_WORDPARTLEFT: Use 2390 Move to the next change in capitalisation
            ('Alt+Left', wx.stc.STC_CMD_WORDPARTLEFT),
#       wxSTC_CMD_WORDPARTLEFTEXTEND: Use 2391 Move to the previous change in capitalisation extending selection to new caret position
            ('Alt+Shift+Left', wx.stc.STC_CMD_WORDPARTLEFTEXTEND),
#       wxSTC_CMD_WORDPARTRIGHT: Use 2392 Move caret right one word extending selection to new caret position
            ('Alt+Right', wx.stc.STC_CMD_WORDPARTRIGHT),
#       wxSTC_CMD_WORDPARTRIGHTEXTEND: Use 2393 Move to the next change in capitalisation extending selection to new caret position.
            ('Alt+Shift+Right', wx.stc.STC_CMD_WORDPARTRIGHTEXTEND),
        ]

        for keys, cmd in action:
            f = 0
            ikey = 0
            for k in keys.split('+'):
                uk = k.upper()
                if uk == 'CTRL':
                    f |= wx.stc.STC_SCMOD_CTRL
                elif uk == 'ALT':
                    f |= wx.stc.STC_SCMOD_ALT
                elif uk == 'SHIFT':
                    f |= wx.stc.STC_SCMOD_SHIFT
                elif keylist.has_key(uk):
                    ikey = keylist[uk]
                elif len(uk) == 1:
                    ikey = ord(uk)
                else:
                    error.error("[TextEditor] Undefined char [%s]" % uk)
                    continue
            self.CmdKeyAssign(ikey, f, cmd)

    def setLineNumberMargin(self):
        lines = self.GetLineCount() #get # of lines, ensure text is loaded first!
        mwidth = len(str(lines))
        if self.mwidth < mwidth:
            self.mwidth = mwidth
            width = self.TextWidth(wx.stc.STC_STYLE_LINENUMBER, 'O'*(self.mwidth+1))
            self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER )
            self.SetMarginWidth(1, width)

    def CanView(self):
        return True

    def ZoomIn(self):
        self.CmdKeyExecute(wx.stc.STC_CMD_ZOOMIN)

    def ZoomOut(self):
        self.CmdKeyExecute(wx.stc.STC_CMD_ZOOMOUT)

    def OnIdle(self, event):
        self.callplugin('on_idle', self, event)
        
    def goto(self, lineno):
        self.SetFocus()
        self.EnsureCaretVisible()
        if lineno:
            lineno -= 1
            self.GotoLine(lineno)
        
    def OnPopUp(self, event):
        other_menus = []
        if self.popmenu:
            self.popmenu.Destroy()
            self.popmenu = None
        self.callplugin('other_popup_menu', self, common.getProjectName(self.filename), other_menus)
        import copy
        if other_menus:
            pop_menus = copy.deepcopy(TextEditor.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(TextEditor.popmenulist)
        self.popmenu = pop_menus = makemenu.makepopmenu(self, pop_menus, TextEditor.imagelist)

        self.PopupMenu(self.popmenu, event.GetPosition())
        