def rerange(text):
    import re
    r_blank = re.compile(r'\s+')
    lines = text.splitlines(True)
    if len(lines) <= 1:
        return
    s = []
    flag = True
    pos = []
    for line in lines:
        line = line.rstrip()
        if not line: 
            s.append('')
            continue
        strings = ['']#strings
        #append leading blank
        b = r_blank.match(line)
        if b:
            p = b.end()
        else:
            p = 0
        if flag:
            pos.append(p)
        while 1:
            lastp = p
            b = feed(line, p)
            if b:
                p = p + len(b)
                strings.append(b)
            else:
                break
            b = r_blank.match(line[p:])
            if b:
                p = p + b.end()
            else:
                break
            if flag:
                pos.append(p - lastp)
            
        flag = False
        pos.append(0)
        s.append(''.join([x.ljust(y) for x, y in zip(strings, pos)]))
    return s
        
def feed(text, pos):
    s = []
    i = pos
    while i < len(text):
        c = text[i]
        if c != ' ':
            s.append(c)
            if c == "'" or c == '"':
                i += 1
                while 1 or i<len(text):
                    k = text[i]
                    if k == '\\':
                        s.append(c)
                        s.append(text[i+1])
                        i += 2
                    elif k == c:
                        s.append(k)
                        i += 1
                        break
                    else:
                        s.append(k)
                        i += 1
            else:
                i += 1
        else:
            break
    return ''.join(s)

def run(win):
    text = win.document.GetSelectedText()
    if not text: return
    s = rerange(text)
    if s:
        status = win.document.save_state()
        win.document.BeginUndoAction()
        win.document.ReplaceSelection(win.document.getEOLChar().join(s))
        win.document.EndUndoAction()
        win.document.restore_state(status)
        
run(win)
    
if __name__ == '__main__':
    s = rerange("""        self.addSyntaxItem('regex',             'Regex',                wx.stc.STC_C_REGEX,                     self.STE_STYLE_REGEX)
        self.addSyntaxItem('commentlinedoc', 'Comment line doc', wx.stc.STC_C_COMMENTLINEDOC, self.STE_STYLE_COMMENTOTHER)
        """)
    print '\n'.join(s)