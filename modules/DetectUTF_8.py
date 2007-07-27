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
#	$Id: DetectUTF_8.py 176 2005-11-22 02:46:37Z limodou $

def utf8Detect(text):
	"""Detect if a string is utf-8 encoding"""
	lastch=0
	begin=0
	BOM=True
	BOMchs=(0xEF, 0xBB, 0xBF)
	good=0
	bad=0
	for char in text:
		ch=ord(char)
		if begin<3:
			BOM=(BOMchs[begin]==ch) and BOM
			begin += 1
			continue
		if (begin==4) and (BOM==True):
			break;
		if (ch & 0xC0) == 0x80:
			if (lastch & 0xC0) == 0xC0:
				good += 1
			elif (lastch &0x80) == 0:
				bad += 1
		elif (lastch & 0xC0) == 0xC0:
			bad += 1

		lastch = ch

	if (((begin == 4) and (BOM == True)) or
		(good >= bad and good>0)):
		return True
	else:
		return False

if __name__ == '__main__':
	import sys
	text=open(sys.argv[1]).read()
	print utf8Detect(text)