
def run(win):
    class MOD:pass

    mod = MOD()

    mod.dialog = [
    ('savefile', 'imagefile', '', 'Saving image filename:', None),
    ('single', 'filetype', 'png', 'Image file type:', [('Gif', 'gif'), ('Png', 'png'), ('Jpeg', 'jpg')]),
    ('string', 'args', '', 'Other command line options:', None),
    ]
    mod.title = 'Input dot command line'

    from modules.EasyGui import EasyCommander
    from modules.Debug import error
    from modules import common

    easy = EasyCommander.EasyCommander(win, mod, cmdoption='')
    if easy.run():
        values = easy.GetValue()
        import os
        try:
            cmd = 'dot -T%s -o%s %s %s' % (values['filetype'], common.encode_string(values['imagefile'], common.defaultfilesystemencoding), values['args'], win.document.filename)
            os.system(cmd)
        except:
            error.traceback()
            common.showerror(win, tr("Cann't execute [%s]") % cmd)
            return
        if os.path.exists(values['imagefile']):
            from modules import ImageWin
            try:
                win = ImageWin.ImageWin(win, values['imagefile'])
                win.Show()
            except:
                common.showerror(win, tr("Cann't open image file %s") % values['imagefile'])

run(win)