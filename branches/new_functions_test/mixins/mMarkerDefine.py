#!/usr/bin/env python
#coding=utf-8
"""
There are 32 markers, numbered 0 to 31, and you can assign any combination of them to each line in the document.
Markers appear in the selection margin to the left of the text.
If the selection margin is set to zero width, the background colour of the whole line is changed instead. 
Marker numbers 25 to 31 are used by Scintilla in folding margins, and have symbolic names of the form SC_MARKNUM_*, 
for example SC_MARKNUM_FOLDEROPEN.

Marker numbers 0 to 24 have no pre-defined function; 
you can use them to mark syntax errors or the current point of execution, break points, 
or whatever you need marking. If you do not need folding, you can use all 32 for any purpose you wish.
Each marker number has a symbol associated with it. 
You can also set the foreground and background colour for each marker number, 
so you can use the same symbol more than once with different colouring for different uses. 
Scintilla has a set of symbols you can assign (SC_MARK_*) or you can use characters. 
By default, all 32 markers are set to SC_MARK_CIRCLE with a black foreground and a white background.

The markers are drawn in the order of their numbers, 
so higher numbered markers appear on top of lower numbered ones. 
Markers try to move with their text by tracking where the start of their line moves. 
When a line is deleted, its markers are combined, by an OR operation, with the markers of the previous line.
"""
import wx
from modules import Mixin



class Marker(object):
    
    def __init__(self, editor):
        self.editor = editor
        self.error_xpm= [
            #* width height ncolors cpp [x_hot y_hot] */
            "34 34 4 1 0 0",
            #/* colors */
            " 	s none	m none	c none",
            ".	s iconColor3	m black	c #FF0000",
            "X	s bottomShadowColor	m black	c #5D6069",
            "o	s iconColor2	m white	c #FFFFFF",
            #/* pixels */
            "                                  ",
            "            ........              ",
            "          ............            ",
            "        ................          ",
            "       ..................         ",
            "      ....................X       ",
            "     ......................X      ",
            "    ........................X     ",
            "   .......o..........o.......X    ",
            "   ......ooo........ooo......X    ",
            "  ......ooooo......ooooo......X   ",
            "  .......ooooo....ooooo.......X   ",
            " .........ooooo..ooooo.........X  ",
            " ..........oooooooooo..........X  ",
            " ...........oooooooo...........XX ",
            " ............oooooo............XX ",
            " ............oooooo............XX ",
            " ...........oooooooo...........XX ",
            " ..........oooooooooo..........XX ",
            " .........ooooo..ooooo.........XX ",
            "  .......ooooo....ooooo.......XX  ",
            "  ......ooooo......ooooo......XX  ",
            "   ......ooo........ooo......XXX  ",
            "   .......o..........o.......XX   ",
            "    ........................XXX   ",
            "     ......................XXX    ",
            "     X....................XXX     ",
            "      X..................XXX      ",
            "       X................XXX       ",
            "        XX............XXXX        ",
            "          XX........XXXXX         ",
            "            XXXXXXXXXXX           ",
            "              XXXXXXX             ",
            "                                  ", 
        ]

        self.quest_xpm = [
            # /* width height ncolors cpp [x_hot y_hot] */
            "34 34 4 1 0 0",
            # /* colors */
            " 	s none	m none	c none",
            ".	s iconColor2	m white	c #FFFFFF",
            "X	s bottomShadowColor	m black	c #5D6069",
            "o	s iconColor1	m black	c #000000",
            # /* pixels */
            "                                  ",
            "            ........              ",
            "         ...XXXXXXXX...           ",
            "       ..XXXXXXXXXXXXXX..         ",
            "      .XXXXXXXXXXXXXXXXXX.        ",
            "     .XXXXXXXXoooooXXXXXXXo       ",
            "    .XXXXXXXXoXXXXooXXXXXXXo      ",
            "   .XXXXXXXXoooXXXXooXXXXXXXo     ",
            "  .XXXXXXXXXooooXXXooXXXXXXXXo    ",
            "  .XXXXXXXXXXooXXXoooXXXXXXXXo.   ",
            " .XXXXXXXXXXXXXXXooooXXXXXXXXXo.  ",
            " .XXXXXXXXXXXXXXooooXXXXXXXXXXo.  ",
            " .XXXXXXXXXXXXXoooooXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooXXXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXooXXXXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoXXXXXXXXXXXXXXXo.. ",
            "  .XXXXXXXXXXXoXXXXXXXXXXXXXXo... ",
            "  .XXXXXXXXXXXXXXXXXXXXXXXXXXo... ",
            "   .XXXXXXXXXXooXXXXXXXXXXXXo...  ",
            "    oXXXXXXXXooooXXXXXXXXXXo....  ",
            "     oXXXXXXXXooXXXXXXXXXXo....   ",
            "      oXXXXXXXXXXXXXXXXXXo....    ",
            "       ooXXXXXXXXXXXXXXoo....     ",
            "        .oooXXXXXXXXooo.....      ",
            "         ...oooXXXXo.......       ",
            "           ....oXXXo.....         ",
            "              .oXXXo..            ",
            "                oXXo..            ",
            "                 oXo..            ",
            "                  oo..            ",
            "                   ...            ",
            "                    ..            ",
            "                                  ", 
        ]

        self.info_xpm = [
            # /* width height ncolors cpp [x_hot y_hot] */
            "34 34 4 1 0 0",
            # / * colors */
            " 	s none	m none	c none",
            ".	s iconColor3	m black	c #FF0000",
            "X	s bottomShadowColor	m black	c #FFFFFF",
            "o	s iconColor2	m white	c #FF0000",
            # /* pixels */
            "                                  ",
            "            ........              ",
            "         ...XXXXXXXX...           ",
            "       ..XXXXXXXXXXXXXX..         ",
            "      .XXXXXXXXXXXXXXXXXX.        ",
            "     .XXXXXXXXooooXXXXXXXXo       ",
            "    .XXXXXXXXooooooXXXXXXXXo      ",
            "   .XXXXXXXXXooooooXXXXXXXXXo     ",
            "  .XXXXXXXXXXXooooXXXXXXXXXXXo    ",
            "  .XXXXXXXXXXXXXXXXXXXXXXXXXXo.   ",
            " .XXXXXXXXXXXXXXXXXXXXXXXXXXXXo.  ",
            " .XXXXXXXXXXoooooooXXXXXXXXXXXo.  ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            " .XXXXXXXXXXXXoooooXXXXXXXXXXXo.. ",
            "  .XXXXXXXXXXXoooooXXXXXXXXXXo... ",
            "  .XXXXXXXXXXXoooooXXXXXXXXXXo... ",
            "   .XXXXXXXXXXoooooXXXXXXXXXo...  ",
            "    oXXXXXXXoooooooooXXXXXXo....  ",
            "     oXXXXXXXXXXXXXXXXXXXXo....   ",
            "      oXXXXXXXXXXXXXXXXXXo....    ",
            "       ooXXXXXXXXXXXXXXoo....     ",
            "        .oooXXXXXXXXooo.....      ",
            "         ...oooXXXXo.......       ",
            "           ....oXXXo.....         ",
            "              .oXXXo..            ",
            "                oXXo..            ",
            "                 oXo..            ",
            "                  oo..            ",
            "                   ...            ",
            "                    ..            ",
            "                                  ", 
        ]
        self.find_xpm = [
            # /* width height ncolors cpp [x_hot y_hot] */
            "18 18 5 1 0 0",
            # /* colors */
            " 	s none	m none	c none",
            ".	s iconColor1	m black	c #FF0000",
            "X	s iconColor2	m none	c #FFFFFF",
            "O	s iconGray2	m none	c #bdbdbd",
            "+	s bottomShadowColor	m black	c #5D6069",
            # /* pixels */
            "                  ",
            " .........        ",
            " .XXXXXXX..       ",
            " .XXXXXXX.O.      ",
            " .XXXXXXX....     ",
            " .XXXXXXXXXX.     ",
            " .XXXXXXX....     ",
            " .XXXXXX.OOOO.    ",
            " .XXXXX.OXXOOO.   ",
            " .XXXXX.OXOOOO.   ",
            " .XXXXX.OOOOOO.   ",
            " .XXXXX.OOOXOO.   ",
            " .XXXXXX.OOOO.+   ",
            " .XXXXXXX....+..  ",
            " .XXXXXXXXXX.+... ",
            " ............+ .. ",
            "    ++++++++++    ",
            "                  ", 
        ]
        self.help_xpm = [
            # /* width height ncolors cpp [x_hot y_hot] */
            "18 18 3 1 0 0",
            # /* colors */
            " 	s none	m none	c none",
            ".	s iconColor1	m black	c #F372DD",
            "X	s bottomShadowColor	m black	c #F372DD",
            # /* pixels */
            "                  ",
            "                  ",
            "      .....X      ",
            "     ..  X..X     ",
            "    ..X   ...     ",
            "    ..X   ...     ",
            "    X..  X..X     ",
            "         ..X      ",
            "        ..        ",
            "       ..X        ",
            "       ..X        ",
            "                  ",
            "       ..X        ",
            "       ..X        ",
            "       ..X        ",
            "        XX        ",
            "                  ",
            "                  ", 
        ]
        self.default_marker_collect = {
            "arrow"                          :wx.stc.STC_MARK_ARROW,
            "arrowdown"                      :wx.stc.STC_MARK_ARROWDOWN, 
            "arrows"                         :wx.stc.STC_MARK_ARROWS, 
            "background"                     :wx.stc.STC_MARK_BACKGROUND, 
            "boxminus"                       :wx.stc.STC_MARK_BOXMINUS, 
            "boxminusconnected"              :wx.stc.STC_MARK_BOXMINUSCONNECTED,
            "boxplus"                        :wx.stc.STC_MARK_BOXPLUS, 
            "boxplusconnected "              :wx.stc.STC_MARK_BOXPLUSCONNECTED,
            "character"                      :wx.stc.STC_MARK_CHARACTER, 
            "circle"                         :wx.stc.STC_MARK_CIRCLE,
            "circleminus"                    :wx.stc.STC_MARK_CIRCLEMINUS, 
            "circleminusconnected"           :wx.stc.STC_MARK_CIRCLEMINUSCONNECTED, 
            "circleplus"                     :wx.stc.STC_MARK_CIRCLEPLUS, 
            "circleplusconnected"            :wx.stc.STC_MARK_CIRCLEPLUSCONNECTED,
            "empty"                          :wx.stc.STC_MARK_EMPTY,
            "dotdotdot "                     :wx.stc.STC_MARK_DOTDOTDOT, 
            "lcorner"                        :wx.stc.STC_MARK_LCORNER,
            "minus"                          :wx.stc.STC_MARK_MINUS,
            "fullrect"                       :wx.stc.STC_MARK_FULLRECT,
            "lcornercurve"                   :wx.stc.STC_MARK_LCORNERCURVE,   
            "pixmap "                        :wx.stc.STC_MARK_PIXMAP,
            "plus"                           :wx.stc.STC_MARK_PLUS,
            "roundrect"                      :wx.stc.STC_MARK_ROUNDRECT, 
            "shortarrow"                     :wx.stc.STC_MARK_SHORTARROW, 
            "smallrect"                      :wx.stc.STC_MARK_SMALLRECT, 
            "tcorner"                        :wx.stc.STC_MARK_TCORNER,
            "tcornercurve"                   :wx.stc.STC_MARK_TCORNERCURVE, 
            "vline"                          :wx.stc.STC_MARK_VLINE, 
            # the xpm symbol 
            "error_xpm"                          :self.error_xpm, 
            "quest_xpm"                          :self.quest_xpm, 
            "info_xpm"                           :self.info_xpm, 
            "find_xpm"                           :self.find_xpm, 
            "help_xpm"                           :self.help_xpm, 
        }
        
        self.fix_marker_number = {
        "bookmarker":0
        # next is "something:1,something:2,something:3... etc.
        }
        
        self.fix_marker_big_number = {
        "errormarker":24, 
        "snippet":23, 
        "vimmarker":22
        # next is "something:23,something:22,something:21... etc.
        }
        
        def number_define():
            for x in xrange(len(self.fix_marker_number.keys()), 25 - len(self.fix_marker_big_number.keys()) + 1):
                yield x
        self.marker_number = number_define()

    
    def marker_define(self, name, color_fore='red', color_back='blue', fix_number=None):
        """
        useage:
            
        marker_define('arrow', color_fore, color_back) 
        marker_define('A', color_fore, color_back)
        marker_define('xpm')
         
        overright STC MarkerDefine
        
        @author: ygao
        
        @param self: editor
        @type self: instance
        @param name: stand for wx.stc.STC_MAKE_*
        @type name: 
        @param color_back: wx.Color
        @type color_back: 
        @param color_fore: 
        @type color_fore: 
        @return:  number, marker
        @rtype:   int, int
        """
            
        try:
            keycode = ord(name)
        except:
            keycode = None
        if keycode:
            symbol = wx.stc.STC_MARK_CHARACTER + keycode
        else:
            symbol = self.default_marker_collect.get(name, None)
        if fix_number:
            temp = self.fix_marker_big_number.get(fix_number, None)
            temp1 = self.fix_marker_number.get(fix_number, None)
            if temp is not None:
                number = temp
            elif temp1 is not None:
                number = temp1
            else:
                raise ValueError("the fix marker number name is not correct.")
        else:
            number = self.marker_number.next()
        mask = self.get_mask(number)
        if isinstance(symbol, list):
            self.editor.MarkerDefineBitmap(number, wx.BitmapFromXPMData(symbol))
            return [number, mask]
        self.editor.MarkerDefine(number, symbol, color_fore, color_back)
        
        # don't use return (number,marker),it can complain.        
        return [number, mask]
    
    def get_mask(self, marker_number):
        return 1<<1*marker_number

    def toggle_mark(self, lineno, marker_number):
        marker = self.editor.MarkerGet(lineno)
        if marker & self.get_mask(marker_number):
            self.editor.MarkerDelete(lineno, marker_number)
        else:
            self.editor.MarkerAdd(lineno, marker_number)
            
    def get_marks(self, marker_number):
        """Gets a list of all lines containing  the marks of the mask
        @return: list of line numbers

        """
        return [mark for mark in xrange(self.editor.GetLineCount()) if self.editor.MarkerGet(mark) & self.get_mask(marker_number)]


    def get_marker_next(self, line, mask, cycle=True):
        marker = self.editor.MarkerGet(line)
        if marker & mask:
            line += 1
        f = self.editor.MarkerNext(line, mask)
        if f > -1:
            return (f + 1)
        else:
            if not cycle:
                return None
            f = self.editor.MarkerNext(0, mask)
            if f > -1:
                return (f + 1)
            return None

    def get_marker_previous(self, line, mask, cycle=True):
        marker = self.editor.MarkerGet(line)
        if marker & mask:
            line -= 1
        f = self.editor.MarkerPrevious(line, mask)
        if f > -1:
            return f + 1
        else:
            if not cycle:
                return None
            f = self.editor.MarkerPrevious(self.editor.GetLineCount()-1, mask)
            if f > -1:
                return f + 1
            return  None
 
def editor_init(self):
    self.marker = Marker(self)
    self.marker_define = self.marker.marker_define
    self.toggle_mark = self.marker.toggle_mark
    self.get_marker_next = self.marker.get_marker_next
    self.get_marker_previous = self.marker.get_marker_previous
    self.get_marks = self.marker.get_marks

Mixin.setPlugin('editor', 'init', editor_init, Mixin.HIGH, 1)

def editor_init(self):
    # ygao note: snippet_marker
    MARK_SNIPPET_COLOR =  '#508559'
    self.snippet_marker, self.snippet_mask = self.marker_define('circle', MARK_SNIPPET_COLOR, MARK_SNIPPET_COLOR, 'snippet')
    
    # bookmarks
    self.bookmark_number, self.bookmarker_mask = self.marker_define('shortarrow', 'blue', 'blue', 'bookmarker')
    
    # the error marker
    self.error_number, self.error_mask = self.marker_define('minus','red','red', 'errormarker')
##    self.error_number, self.error_mask = self.marker_define('error_xpm')
    
    # the vim indicator
##    self.vim_number, self.vim_mask = self.marker_define('plus','#0C1021','red', 'vimmarker')
##    self.vim_number, self.vim_mask = self.marker_define('info_xpm',fix_number='vimmarker')
    self.vim_number, self.vim_mask = self.marker_define('help_xpm', fix_number='vimmarker')
    
    # the search_marker
    self.search_marker_number, self.search_mask = self.marker_define("arrowdown", "red", "red")
##    self.search_marker_number2, self.search_mask2 = self.marker_define("arrowdown", "yellow", "yellow")
    self.search_marker_number2, self.search_mask2 = self.marker_define("find_xpm")
Mixin.setPlugin('editor', 'init', editor_init)

