from modules import Globals

def analysis(win):
    for pname, v in Globals.mainframe.panel.getPages().items():
        page = v[2]
        if hasattr(page, 'resthtmlview') and page.document is win:
            text = html_fragment(win.GetText().encode('utf-8'))
            page.load(text)
    
def html_fragment(content):
    from docutils.core import publish_string

    return publish_string(content, writer_name = 'html' )

