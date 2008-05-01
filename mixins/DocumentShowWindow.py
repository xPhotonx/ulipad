
import wx
import os.path
import sys

from modules.Debug import error
from modules.Mixin import Mixin
from modules.sqlite import DocBase
from mixins import mDocumentShowWindow
from modules.wxctrl import FlatButtons
from modules import common
if wx.Platform == '__WXMSW__':
    import  wx.lib.iewin    as  iewin

mk = "mk:@MSITStore:"
python_path = os.path.dirname(sys.executable)
doc_path = mk + python_path + "\\Doc\\Python%s.chm" % sys.version[0:3].replace('.', '')+ "::" 
class DocumentShowWindow(wx.Panel, Mixin):
    __mixinname__ = 'docuwindow'
    
    def __init__(self, parent, mainframe):
        self.initmixin()
        
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.mainframe = mainframe
        self.pref = mainframe.pref
        self.docbase = DocBase()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.showing = False
        self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_AUTO_URL)
        self.text_fixed_font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        self.text_default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bgcolor = '#FFFFE1'
        self.text.Bind(wx.EVT_TEXT_URL, self.OnURL, id=self.text.GetId())
        
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/plus.png'))
        btn.SetToolTip(wx.ToolTip(tr("add a link to database")))
##        btn.Bind(wx.EVT_BUTTON, self.addlink)
        box.Add(btn, 0, wx.ALL, 1)
        btn1 = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/save.gif'))
        btn1.SetToolTip(wx.ToolTip(tr("add info to database")))
        btn1.Bind(wx.EVT_BUTTON, self.saveinfo)
        box.Add(btn1, 0, wx.ALL, 1)
        
        self.word_list=[]
        self.location = wx.ComboBox(
                            self, -1, "",(90, 80), (95, -1),self.word_list,style=wx.CB_DROPDOWN|wx.PROCESS_ENTER
                            )
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
        box.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)
        
        
        
        sizer.Add(box, 0, wx.EXPAND)
        sizer.Add(self.text, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.show('document will show here!')
        
    def saveinfo(self, event):
        index = self.location.GetValue()
        value = self.text.GetValue()
        try:
            info = value[value.find(u'<info>') + 7:value.find(u'</info>')]
        except:
            return
        if info and index:
            self.docbase.insert_link(index, info)
        
        
        
        
        
    def OnLocationSelect(self, evt):
        word = self.location.GetStringSelection()
        info = self.docbase.get_link(word, True)
        if info:
            self.text.SetValue(info)
    
    def OnLocationKey(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            word = self.location.GetValue()
            if word not in self.word_list:
                self.word_list.insert(0, word)
                self.location.Append(word)
            info = self.docbase.get_link(word, True)
            if info:
                self.text.SetValue(info)
        else:
            evt.Skip()
            
    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            
    def OnURL(self, event):
        if event.MouseEvent.LeftUp():
            url = self.text.GetRange(event.URLStart,event.URLEnd)
            if "file://" in url:
                filename = url[7:]
                li = filename.split('|')
                doc = self.mainframe.editctrl.new(li[0])
                doc.GotoLine(int(li[1]))
                doc.EnsureCaretVisible()
                doc.SetFocus()
            elif "http://editor" in url:
                li = url.split('|')
                self.mainframe.document.GotoLine(int(li[1]))
                self.mainframe.document.EnsureCaretVisible()
                self.mainframe.document.SetFocus()
            elif "http://pychm::":
                li = url.split('::')
                doc = doc_path + str(li[1])
                win = self.mainframe.panel.getPage(mDocumentShowWindow.html_show_pagename)
                win.html.ie.LoadUrl(doc)
                self.mainframe.panel.showPage(mDocumentShowWindow.html_show_pagename)
            elif "http://":
                win = self.mainframe.panel.getPage(mDocumentShowWindow.html_show_pagename)
                win.html.ie.LoadUrl(url)
                self.mainframe.panel.showPage(mDocumentShowWindow.html_show_pagename)
                
        event.Skip()
        
    def show(self, text, index = None):
        self.showing = True
        self.Freeze()
        if  not self.mainframe.panel.RightIsVisible:
            self.mainframe.panel.showWindow('right', True)
        if  self.mainframe.pref.inputass_calltip_including_source_code:
            self.text.SetFont(self.text_fixed_font)
        else:
            self.text.SetFont(self.text_default_font)
        link = self.docbase.get_link(index, True)
        if link:
            text = link + '\n' + text
        self.text.SetValue(text)
        self.SetBackgroundColour(self.bgcolor)
        self.text.SetBackgroundColour(self.bgcolor)
        # if data arrive, select this documentshow window
##        self.mainframe.panel.showPage(mDocumentShowWindow.document_show_pagename)
        
        self.Show()
        self.Thaw()
        self.showing = False

    def OnSize(self,event):
        self.text.SetSize(self.parent.GetClientSize())
        event.Skip()
        
    def canClose(self):
        self.mainframe.panel.showWindow("right",False)
        
        return False
    
    
#----------------------------------------------------------------------

from mixins import HtmlPage
class HtmlShowWindow(wx.Panel, Mixin):
    
    __mixinname__ = 'htmldocuwindow'
    
    def __init__(self, parent, mainframe):
        self.initmixin()
        wx.Panel.__init__(
            self, parent, -1,
            style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN|wx.NO_FULL_REPAINT_ON_RESIZE
            )
        self.mainframe = mainframe
        self.parent = parent
        self.URL = ''
        
#        self.current = "http://wxPython.org/"
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
#        self.ie = iewin.IEHtmlWindow(self, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)
#
#        btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "Home", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnHomeButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "Search", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnSearchPageButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
#        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
#        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
#
#        txt = wx.StaticText(self, -1, "Location:")
#        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)
#
#        self.location = wx.ComboBox(
#                            self, -1, "", style=wx.CB_DROPDOWN|wx.PROCESS_ENTER
#                            )
#        
#        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
#        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
#        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
#        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)
#
#        sizer.Add(btnSizer, 0, wx.EXPAND)
#        sizer.Add(self.ie, 1, wx.EXPAND)
#
#        self.ie.LoadUrl(self.current)
#        self.location.Append(self.current)
#
#        self.SetSizer(sizer)
#        # Since this is a wxWindow we have to call Layout ourselves
#        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.url_list=[]
        
        box = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/plus.png'))
        btn.SetToolTip(wx.ToolTip(tr("add a link to database")))
        btn.Bind(wx.EVT_BUTTON, self.addlink)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/prev.gif'))
        btn.SetToolTip(wx.ToolTip(tr("previous visited page")))
        btn.Bind(wx.EVT_BUTTON, self.OnPrevPageButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/next.gif'))
        btn.SetToolTip(wx.ToolTip(tr("next visited page")))
        btn.Bind(wx.EVT_BUTTON, self.OnNextPageButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/stop1.png'))
        btn.SetToolTip(wx.ToolTip(tr("stop visiting page")))
        btn.Bind(wx.EVT_BUTTON, self.OnStopButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/classbrowserrefresh.gif'))
        btn.SetToolTip(wx.ToolTip(tr("refresh page")))
        btn.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/home.png'))
        btn.SetToolTip(wx.ToolTip(tr("goto home page")))
        btn.Bind(wx.EVT_BUTTON, self.OnHomeButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)

        btn = FlatButtons.FlatBitmapButton(self, -1, common.getpngimage('images/search.png'))
        btn.SetToolTip(wx.ToolTip(tr("search web pages")))
        btn.Bind(wx.EVT_BUTTON, self.OnSearchPageButton)
        btnSizer.Add(btn, 0, wx.ALL, 1)
        
        self.location = wx.ComboBox(
                            self, -1, "", style=wx.CB_DROPDOWN|wx.PROCESS_ENTER
                            )
        
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)
        
        if wx.Platform == '__WXMSW__':
            import  wx.lib.iewin    as  iewin
            self.html = HtmlPage.IEHtmlWindow(self)
            # Hook up the event handlers for the IE window
            self.Bind(iewin.EVT_BeforeNavigate2, self.OnBeforeNavigate2, self.html.ie)
            self.Bind(iewin.EVT_NewWindow2, self.OnNewWindow2, self.html.ie)
            self.Bind(iewin.EVT_DocumentComplete, self.OnDocumentComplete, self.html.ie)
            ##self.Bind(iewin.EVT_ProgressChange,  self.OnProgressChange, self.html.ie)
            self.Bind(iewin.EVT_StatusTextChange, self.OnStatusTextChange, self.html.ie)
            self.Bind(iewin.EVT_TitleChange, self.OnTitleChange, self.html.ie)
            
        else:
            self.html = HtmlPage.DefaultHtmlWindow(self)
            self.html.SetRelatedFrame(mainframe, mainframe.app.appname + " - Browser [%s]")
            self.html.SetRelatedStatusBar(0)
            
        self.tmpfilename = None
        box.Add(btnSizer, 0, wx.EXPAND)
        #self.load(content)
        if wx.Platform == '__WXMSW__':
            box.Add(self.html.ie, 1, wx.EXPAND|wx.ALL, 1)
        else:
            box.Add(self.html, 1, wx.EXPAND|wx.ALL, 1)
        
        self.SetSizer(box)
        self.Refresh()

    def add_url(self,url):
        if url not in self.url_list:
            if url:
                self.url_list.append(url)
                self.location.Append(url)
        else:
            pass

    def load_url(self,url=''):
        self.html.ie.LoadUrl(url)
        self.add_url(url)

        
    def addlink(self, event):
        if doc_path in self.URL:
            url = 'http://pychm::' + self.URL.split('::')[1]
            print>>sys.stdout, 96, url
            
            
    def load(self, content):
        if not self.tmpfilename:
            fd, self.tmpfilename = tempfile.mkstemp('.html')
            os.write(fd, content)
            os.close(fd)
        else:
            file(self.tmpfilename, 'w').write(content)
        self.html.Load(self.tmpfilename)
       
    def canClose(self):
        self.mainframe.panel.showWindow("right",False)
        return False
        
    def isStop(self):
        return self.chkAuto.GetValue()
    
    def OnClose(self, win):
        if self.tmpfilename:
            try:
                os.unlink(self.tmpfilename)
            except:
                pass
        
    def show(self, text):
        self.html.LoadString(text)
    
        
    def canClose(self):
        self.mainframe.panel.showWindow("right",False)
        
        return False
    
   
    
    def OnSize(self, evt):
        self.Layout()


    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.html.ie.Navigate(url)

    def OnLocationKey(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            URL = self.location.GetValue()
            self.location.Append(URL)
            self.html.ie.Navigate(URL)
        else:
            evt.Skip()


    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, "Open Location",
                                "Enter a full URL or local path",
                                self.current, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.html.ie.Navigate(self.current)

        dlg.Destroy()

    def OnHomeButton(self, event):
        self.html.ie.GoHome()    ## ET Phone Home!

    def OnPrevPageButton(self, event):
        self.html.ie.GoBack()

    def OnNextPageButton(self, event):
        self.html.ie.GoForward()

    def OnStopButton(self, evt):
        self.html.ie.Stop()

    def OnSearchPageButton(self, evt):
        self.html.ie.GoSearch()

    def OnRefreshPageButton(self, evt):
        self.html.ie.Refresh(iewin.REFRESH_COMPLETELY)




    def OnBeforeNavigate2(self, evt):
        self.URL = evt.URL
        evt.Cancel = False
        self.add_url(evt.URL)

    def OnNewWindow2(self, evt):
        self.logEvt(evt)
        # Veto the new window.  Cancel is defined as an "out" param
        # for this event.  See iewin.py
        evt.Cancel = True   

    def OnProgressChange(self, evt):
        pass
        
    def OnDocumentComplete(self, evt):
        
        self.current = evt.URL
        #self.location.SetValue(self.current)
        #self.mainframe.document.SetFocus()
        #self.mainframe.document.focus_lost = False

    def OnTitleChange(self, evt):
        pass
    def OnStatusTextChange(self, evt):
        self.mainframe.SetStatusText(evt.Text)