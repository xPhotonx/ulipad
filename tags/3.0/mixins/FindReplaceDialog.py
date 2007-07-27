#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
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
#	$Id: FindReplaceDialog.py 93 2005-10-11 02:51:02Z limodou $

import wx
import wx.stc
#import wx.lib.dialogs
import re
import wx.xrc

def getRawText(string):
	if wx.USE_UNICODE:
		s = string.encode('utf-8')
		return s
	else:
		return string

class Finder:
	def __init__(self):
		self.findtext = ''
		self.regular = False
		self.rewind = True
		self.matchcase = False
		self.wholeword = False
		self.inselection = False
		self.direction = 0
		self.replacetext = ''

	def getFlags(self):
		flags = 0
		if self.wholeword:
			flags |= wx.stc.STC_FIND_WHOLEWORD
		if self.matchcase:
			flags |= wx.stc.STC_FIND_MATCHCASE
		if self.regular:
			flags |= wx.stc.STC_FIND_REGEXP

		return flags

	def setWindow(self, win):
		self.win = win

	def find(self, direction=0):
		if direction == 0:		#forwards
			r = self.findNext()
		else:
			r = self.findPrev()

		if r:
			self.setSelection(*r)

	def findNext(self):
		length = len(getRawText(self.findtext))
		if length == 0:
			return None
		if self.regular:
			return self.findReNext()
		start = self.win.GetCurrentPos()
		end = self.win.GetLength()
		pos = self.win.FindText(start, end, self.findtext, self.getFlags())
		if pos == -1:	#not found
			if self.rewind:
				pos = self.win.FindText(0, start, self.findtext, self.getFlags())
			if pos == -1:
				message = tr("Cann't find the text !")
				self.showMessage(message)
				return None

		return (pos, pos + length)

	def findPrev(self):
		length = len(getRawText(self.findtext))
		if length == 0:
			return None
		start = self.win.GetCurrentPos()
		text = self.win.GetSelectedText()
		if text == self.findtext:
			start -= len(getRawText(text))+1
			start = max ([start, 0])
		pos = self.win.FindText(start, 0, self.findtext, self.getFlags())
		if pos == -1:	#not found
			if self.rewind:
				pos = self.win.FindText(self.win.GetLength(), start, self.findtext, self.getFlags())
			if pos == -1:
				message = tr("Cann't find the text !")
				self.showMessage(message)
				return None

		return (pos, pos + length)

	def showMessage(self, message):
		wx.MessageDialog(self.win, message, tr("Find result"), wx.OK).ShowModal()

	def findReNext(self):
		length = len(getRawText(self.findtext))
		if length == 0:
			return None

		start = self.win.GetCurrentPos()
		end = self.win.GetLength()

		result = self.regularSearch(start, end)
		if result == None:
			if self.rewind:
				result = self.regularSearch(0, start)
			if result == None:
				message = tr("Cann't find the text !")
				self.showMessage(message)
				return None

		return result

	def setSelection(self, start, end):
		self.win.GotoPos(start)
		self.win.EnsureCaretVisible()
		self.win.SetSelectionStart(start)
		self.win.SetSelectionEnd(end)

	def regularSearch(self, start, end):
		case = 0
		if not self.matchcase:
			case = re.IGNORECASE

		re_search = re.compile(getRawText(self.findtext), case | re.MULTILINE)
		matchedtext = re_search.search(self.win.getRawText(), start, end)
		if matchedtext == None:
			return None
		else:
			return matchedtext.span()

	def replace(self):
		text = self.win.GetSelectedText()
		length = len(text)
		if length > 0:
			if self.regular:
				r = self.regularSearch(self.win.GetSelectionStart(), self.win.GetSelectionEnd())
				if r:
					b, e = r
					if (e - b) == length:
						self.win.ReplaceSelection(self.regularReplace(text))
			else:
				if self.matchcase and (text == self.findtext):
					self.win.ReplaceSelection(self.replacetext)
				if (not self.matchcase) and (text.lower() == self.findtext.lower()):
					self.win.ReplaceSelection(self.replacetext)

		self.find(self.direction)

	def replaceAll(self, section):
		length = len(getRawText(self.findtext))
		if section == 0:	#whole document
			start = 0
			end = self.win.GetLength()
		else:
			start, end = self.win.GetSelection()

		if self.regular:
			r = self.regularSearch(start, end)
			if r:
				b, e = r
			else:
				b = -1
		else:
			b = self.win.FindText(start, end, self.findtext, self.getFlags())
		count = 0
		while b != -1:
			count += 1
			if not self.regular:
				e = b + length
			self.win.SetTargetStart(b)
			self.win.SetTargetEnd(e)
			if self.regular:
				rtext = self.regularReplace(self.win.GetTextRange(b, e))
			else:
				rtext = self.replacetext
			self.win.ReplaceTarget(rtext)
			diff = len(rtext) - length
			end += diff
			start = b + len(rtext)
			if self.regular:
				r = self.regularSearch(start, end)
				if r:
					b, e = r
				else:
					b = -1
			else:
				b = self.win.FindText(start, end, self.findtext, self.getFlags())

		if count == 0:
			message = tr("Cann't find the text !")
		else:
			message = tr("Total replaced %d places!") % count
		self.showMessage(message)

	def regularReplace(self, text):
		return re.sub(self.findtext, self.replacetext, text)

class FindDialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

	def init(self, finder):
		self.finder = finder
		self.pref = finder.win.pref
		self.obj_ID_CLOSE.SetId(wx.ID_CANCEL)
		wx.EVT_BUTTON(self, self.ID_FIND, self.OnFind)
		wx.EVT_BUTTON(self, wx.ID_CANCEL, self.OnClose)
		wx.EVT_CHECKBOX(self, self.ID_REGEX, self.OnCheckRegular)
		wx.EVT_CLOSE(self, self.OnClose)

		text = self.finder.win.GetSelectedText()
		if (len(text) > 0) and (text.count(self.finder.win.getEOLChar()) == 0):
			self.obj_ID_FINDTEXT.SetValue(text)
			self.finder.findtext = text
		else:
			self.obj_ID_FINDTEXT.SetValue(self.finder.findtext)

		for s in self.pref.findtexts:
			self.obj_ID_FINDTEXT.Append(s)

		self.setValue()

	def OnFind(self, event):
		self.getValue()
		self.addFindString(self.finder.findtext)
		self.finder.find(self.finder.direction)

	def addFindString(self, text):
		if text in self.pref.findtexts:
			self.pref.findtexts.remove(text)
			self.pref.findtexts.insert(0, text)
		else:
			self.pref.findtexts.insert(0, text)
		while len(self.pref.findtexts) > self.pref.max_number:
			del self.pref.findtexts[-1]

		self.pref.save()

		self.obj_ID_FINDTEXT.Clear()
		for s in self.pref.findtexts:
			self.obj_ID_FINDTEXT.Append(s)

		self.obj_ID_FINDTEXT.SetValue(text)
		self.obj_ID_FINDTEXT.SetMark(0, len(text))

	def OnClose(self, event):
		self.getValue()
		self.Destroy()

	def OnCheckRegular(self, event):
		self.obj_ID_WHOLEWORD.SetValue(0)
		self.obj_ID_WHOLEWORD.Enable(not self.obj_ID_REGEX.GetValue())
		if self.obj_ID_REGEX.GetValue():
			self.obj_ID_DIRECTION.SetSelection(not self.obj_ID_REGEX.GetValue())
		self.obj_ID_DIRECTION.Enable(not self.obj_ID_REGEX.GetValue())

	def getValue(self):
		self.finder.findtext = self.obj_ID_FINDTEXT.GetValue()
		self.finder.regular = self.obj_ID_REGEX.GetValue()
		self.finder.rewind = self.obj_ID_REWIND.GetValue()
		self.finder.matchcase = self.obj_ID_MATCHCASE.GetValue()
		self.finder.wholeword = self.obj_ID_WHOLEWORD.GetValue()
		self.finder.direction = self.obj_ID_DIRECTION.GetSelection()

	def setValue(self):
		self.obj_ID_REGEX.SetValue(self.finder.regular)
		self.obj_ID_REWIND.SetValue(self.finder.rewind)
		self.obj_ID_MATCHCASE.SetValue(self.finder.matchcase)
		self.obj_ID_WHOLEWORD.SetValue(self.finder.wholeword)
		self.obj_ID_DIRECTION.SetSelection(self.finder.direction)
		self.obj_ID_DIRECTION.Enable(not self.finder.regular)
		self.obj_ID_WHOLEWORD.Enable(not self.obj_ID_REGEX.GetValue())

class FindReplaceDialog(FindDialog):
	def __init__(self, *args, **kwargs):
		FindDialog.__init__(self, *args, **kwargs)

	def init(self, finder):
		FindDialog.init(self, finder)
		wx.EVT_BUTTON(self, self.ID_REPLACE, self.OnReplace)
		wx.EVT_BUTTON(self, self.ID_REPLACEALL, self.OnReplaceAll)

		text = self.finder.win.GetSelectedText()
		if len(text) > 0:
			self.obj_ID_SECTION.SetSelection(1)

		for s in self.pref.replacetexts:
			self.obj_ID_REPLACETEXT.Append(s)

		self.setValue()

	def addReplaceString(self, text):
		if self.pref.replacetexts.count(text) > 0:
			self.pref.replacetexts.remove(text)
			self.pref.replacetexts.insert(0, text)
		else:
			self.pref.replacetexts.insert(0, text)
		while len(self.pref.replacetexts) > self.pref.max_number:
			del self.pref.replacetexts[-1]

		self.pref.save()

		self.obj_ID_REPLACETEXT.Clear()
		for s in self.pref.replacetexts:
			self.obj_ID_REPLACETEXT.Append(s)

		self.obj_ID_REPLACETEXT.SetValue(text)
		self.obj_ID_REPLACETEXT.SetMark(0, len(text))

	def OnReplace(self, event):
		self.getValue()
		self.addFindString(self.finder.findtext)
		self.addReplaceString(self.finder.replacetext)
		self.finder.replace()

	def OnReplaceAll(self, event):
		self.getValue()
		self.addFindString(self.finder.findtext)
		self.addReplaceString(self.finder.replacetext)
		self.finder.replaceAll(self.obj_ID_SECTION.GetSelection())

	def getValue(self):
		FindDialog.getValue(self)
		self.finder.replacetext = self.obj_ID_REPLACETEXT.GetValue()

	def setValue(self):
		FindDialog.setValue(self)
		self.obj_ID_REPLACETEXT.SetValue(self.finder.replacetext)


