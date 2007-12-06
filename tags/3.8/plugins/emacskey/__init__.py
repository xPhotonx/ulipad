#   Programmer: wlvong


import wx
from modules import Mixin

inPartialShortcut = False
currentPartialMatch = ''


def keyDown(editor, event):
    global inPartialShortcut
    global currentPartialMatch

    shortcuts = {
        'ctrl+a':(True, wx.stc.STC_CMD_VCHOME),
        'ctrl+b':(True, wx.stc.STC_CMD_CHARLEFT),
        'ctrl+d':(False, pressDelete),
        'ctrl+g':(False, cancelAllCommand),
        'ctrl+h':(True, wx.stc.STC_CMD_DELETEBACK),
        'ctrl+u':(True, wx.stc.STC_CMD_DELLINELEFT),
        'ctrl+f':(True, wx.stc.STC_CMD_CHARRIGHT),
        'ctrl+e':(True, wx.stc.STC_CMD_LINEEND),
        'ctrl+p':(True, wx.stc.STC_CMD_LINEUP),
        'ctrl+n':(True, wx.stc.STC_CMD_LINEDOWN),
        'ctrl+v':(True, wx.stc.STC_CMD_PAGEDOWN),
        'ctrl+w':(True, wx.stc.STC_CMD_CUT),
        'ctrl+y':(True, wx.stc.STC_CMD_PASTE),
        'alt+b':(True, wx.stc.STC_CMD_WORDLEFT),
        'alt+f':(True, wx.stc.STC_CMD_WORDRIGHT),
        'alt+d':(True, wx.stc.STC_CMD_DELWORDRIGHT),
        'alt+v':(True, wx.stc.STC_CMD_PAGEUP),
        'alt+w':(True, wx.stc.STC_CMD_COPY),
        'ctrl+x,k':(False, closeCurrentDoc),
    }

    scs = assembleShortcutString(event)
    print scs
    if scs in shortcuts:
        if shortcuts[scs][0] == True:
            editor.CmdKeyExecute(shortcuts[scs][1])
            return True
        else:
            shortcuts[scs][1](editor, event)
            return True
    if matchPartial(scs, shortcuts):
        inPartialShortcut = True
        currentPartialMatch = scs
        return True
    if len(scs.split(',')) > 1 and scs != ',': # multi-key shortcut reach here
                                # means invalid key
        return True

    return False
Mixin.setMixin('editor', 'on_first_keydown', keyDown)


def matchPartial(scs, shortcuts):
    for key in shortcuts.keys():
        if scs == key.split(',')[0]:
            print 'match partial'
            return True
    return False


def assembleShortcutString(event):
    global inPartialShortcut
    global currentPartialMatch

    key = event.GetKeyCode()
    sc = ''
    #print event.GetModifiers()
    if event.ControlDown():
        sc = 'ctrl'

    if event.AltDown():
        if len(sc) > 0:
            sc = sc + '+'
        sc = sc + 'alt'

    if event.ShiftDown():
        if len(sc) > 0:
            sc = sc + '+'
        sc = sc + 'shift'

    if len(sc) > 0:
        sc = sc + '+'
    sc = sc + chr(key).lower()

    if inPartialShortcut is True and len(currentPartialMatch) > 0:
        sc = currentPartialMatch + ',' + sc
        inPartialShortcut = False
        currentPartialMatch = ''
    return sc


def pressDelete(editor, event):
    event.m_keyCode = wx.WXK_DELETE
    event.m_controlDown = False
    editor.GetEventHandler().AddPendingEvent(event)


def closeCurrentDoc(editor, event):
    editor.SetEvtHandlerEnabled(False)
    editor.mainframe.CloseFile(editor)
    editor.SetEvtHandlerEnabled(True)


def cancelAllCommand(editor, event):
    global inPartialShortcut
    global partialMatch
    inPartialShortcut = False
    partialMatch = ''