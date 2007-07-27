#---------------------------------------------------
#                   NewEdit script
# Author  :limodou
# Date    :2004/07/11
# Version :1.0
# Description:
#     Add linenum to each line of selected text
#
#---------------------------------------------------

def run(win):
	linenums = win.document.getSelectionLines()
	for i, linenum in enumerate(linenums):
		text = str(i+1).ljust(8) + win.document.getLineText(linenum)
		win.document.replaceLineText(linenum, text)

run(win)