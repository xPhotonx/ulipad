import wx
from wx import ImageFromStream, BitmapFromImage
import cStringIO, zlib
import wx.lib.mixins.listctrl as listmix
import sys


def getUncheckData():
    return zlib.decompress(
"x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2\x02 \xcc\xc1\
\x06$\xe5?\xffO\x04R,\xc5N\x9e!\x1c@P\xc3\x91\xd2\x01\xe4\xbb{\xba8\x86X\xf4\
&\xa7\xa4$\xa5-`1\x08\\2\xbb\xb1\xb1\x91\xf5\xd8\x84o\xeb\xff\xfaw\x1d[.=[2\
\x90'\x01\x08v\xec]\xd3\xa3qvU`l\x81\xd9\xd18\t\xd3\x84+\x0cll[\xa6t\xcc9\
\xd4\xc1\xda\xc3<O\x9a1\xc3\x88\xc3j\xfa\x86_\xee@#\x19<]\xfd\\\xd69%4\x01\
\x00\xdc\x80-\x05" )

def getUncheckBitmap():
    return BitmapFromImage(getUncheckImage())

def getUncheckImage():
    stream = cStringIO.StringIO(getUncheckData())
    return ImageFromStream(stream)

#----------------------------------------------------------------------
def getCheckData():
    return zlib.decompress(
'x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2\x02 \xcc\xc1\
\x06$\xe5?\xffO\x04R,\xc5N\x9e!\x1c@P\xc3\x91\xd2\x01\xe47{\xba8\x86X\xf4&\
\xa7\xa4$\xa5-`1\x08\\2\xbb\xb1\xb1\x91\xf5\xd8\x84o\xeb\xff\xfaw\x1d[.=[2\
\x90\'\x01\x08v\xec\\2C\xe3\xec+\xc3\xbd\x05fG\xe3\x14n1\xcc5\xad\x8a8\x1a\
\xb9\xa1\xeb\xd1\x853-\xaa\xc76\xecb\xb8i\x16c&\\\xc2\xb8\xe9Xvbx\xa1T\xc3U\
\xd6p\'\xbd\x85\x19\xff\xbe\xbf\xd7\xe7R\xcb`\xd8\xa5\xf8\x83\xe1^\xc4\x0e\
\xa1"\xce\xc3n\x93x\x14\xd8\x16\xb0(\x15q)\x8b\x19\xf0U\xe4\xb10\x08V\xa8\
\x99\xf3\xdd\xde\xad\x06t\x0e\x83\xa7\xab\x9f\xcb:\xa7\x84&\x00\xe0HE\xab' )

def getCheckBitmap():
    return BitmapFromImage(getCheckImage())

def getCheckImage():
    stream = cStringIO.StringIO(getCheckData())
    return ImageFromStream(stream)

class List(wx.ListView, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, columns, style=wx.LC_REPORT):
        wx.ListView.__init__(self, parent, -1, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.parent = parent
        self.columns = columns

        self.createlist(self.columns)

    def createlist(self, columns):
        self.columns_num = len(columns)

        self.DeleteAllItems()

        for i, v in enumerate(columns):
            info = wx.ListItem()
            info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT

            name, length, align = v

            if align == 'left':
                info.m_format = wx.LIST_FORMAT_LEFT
            elif align == 'center':
                info.m_format = wx.LIST_FORMAT_CENTER
            else:
                info.m_format = wx.LIST_FORMAT_RIGHT
            info.m_text = name
            self.InsertColumnInfo(i, info)
            self.SetColumnWidth(i, length)

    def load(self, getdata):
        for v in getdata():
            i = v[0]
            index = self.InsertStringItem(sys.maxint, i)
            for i, t in enumerate(v[1:]):
                self.SetStringItem(index, i+1, t)

    def GetValue(self):
        for i in range(self.GetItemCount()):
            s = []
            for j in range(self.GetColumnCount()):
                s.append(self.GetItem(i, j).GetText())
            yield tuple(s)

class CheckListMixin:
    def __init__(self, check_image=None, uncheck_image=None):
        self.imagelist = wx.ImageList(16, 16)
        if not check_image:
            check_image = getCheckBitmap()
        if not uncheck_image:
            uncheck_image = getUncheckBitmap()
        self.uncheck_image = self.imagelist.Add(uncheck_image)
        self.check_image = self.imagelist.Add(check_image)
        self.SetImageList(self.imagelist, wx.IMAGE_LIST_SMALL)

        wx.EVT_LEFT_DOWN(self, self.OnLeftDown)
        
        self.on_check = None

        self.values = {}

    def load(self, getdata):
        self.values = {}
        for flag, v in getdata():
            index = self.InsertImageStringItem(sys.maxint, v[0], int(flag))
            self.values[index] = int(flag)
            self.SetItemData(index, index)
            for i, t in enumerate(v[1:]):
                self.SetStringItem(index, i+1, t)

    def OnLeftDown(self,event):
        (index, flags) = self.HitTest(event.GetPosition())
        if flags == wx.LIST_HITTEST_ONITEMICON:
            i = self.GetItemData(index)
            self.values[i] ^= 1
            self.SetItemImage(index, self.values[i])
            if self.on_check:
                self.on_check(index, self.values[i])
            else:
                self.OnCheck(index, self.values[i])
        event.Skip()

    def OnCheck(self, index, f):
        pass

    def GetValue(self):
        for i in range(self.GetItemCount()):
            s = []
            for j in range(self.GetColumnCount()):
                s.append(self.GetItem(i, j).GetText())
            yield (self.values[self.GetItemData(i)], tuple(s))

    def getFlag(self, index):
        i = self.GetItemData(index)
        return self.values[i]

    def setFlag(self, index, f):
        i = self.GetItemData(index)
        self.values[i] = f
        self.SetItemImage(index, self.values[i])

    def notFlag(self, index):
        f = self.getFlag(index)
        self.setFlag(index, f ^ 1)

class CheckList(List, CheckListMixin):
    def __init__(self, parent, columns, check_image=None, uncheck_image=None, style=wx.LC_REPORT):
        List.__init__(self, parent, columns, style=style)
        CheckListMixin.__init__(self, check_image, uncheck_image)

    def load(self, getdata):
        CheckListMixin.load(self, getdata)

    def GetValue(self):
        for i in CheckListMixin.GetValue(self):
            yield i