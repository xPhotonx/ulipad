from modules import Globals
import wx

def analysis(win):
    for pagename, panelname, notebook, page in Globals.mainframe.panel.getPages():
        if is_resthtmlview(page, win):
            text = html_fragment(win.GetText().encode('utf-8'))
            page.load(text)
            wx.CallAfter(win.SetFocus)
            break
    
def html_fragment(content):
    from docutils.core import publish_string

    return publish_string(content, writer_name = 'html' )

def is_resthtmlview(page, document):
    if hasattr(page, 'resthtmlview') and page.resthtmlview and page.document is document:
        return True
    else:
        return False
