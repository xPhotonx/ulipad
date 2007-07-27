def run(mainframe, x):
    from modules.EasyGuider import EasyCommander
    easy = EasyCommander.EasyCommander(parent=mainframe, easyfile='easyDjango.py', inline=True, cmdoption='', outputencoding=x.options.encoding)
    if easy.run():
        values = easy.GetValue()
        values['secret_key'] = get_secret_key()
        if values['db_port'] == 0:
            values['db_port'] = "''"

        from meteor import TemplateScript
#        from StringIO import StringIO
#        buf = StringIO()
#        template = Template()
#        template.load('plugin.script', 'text')
#        buf.write(template.value('text', EasyUtils.str_object(values)))
#        buf.seek(0)
#        ts = TemplateScript()
        ts = TemplateScript()
        ts.run('django.script', vars=values, runtemplate=True)

        return True
    
def get_secret_key():
    from random import choice
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    return secret_key