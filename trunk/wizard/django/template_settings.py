from meteor import *

body = T('''# Django settings for <#proj_name#> project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('<#username#>',  '<#email#>'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = '<#database#>' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '<#db_file#>'             # Or path to database file if using sqlite3.
DATABASE_USER = '<#db_user#>'             # Not used with sqlite3.
DATABASE_PASSWORD = '<#db_password#>'         # Not used with sqlite3.
DATABASE_HOST = '<#db_host#>'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = <#db_port#>             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = '<#time_zone#>'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = '<#language#>'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '<#proj_dir#>/<#proj_name#>/media'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '<#secret_key#>'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.core.template.loaders.filesystem.load_template_source',
    'django.core.template.loaders.app_directories.load_template_source',
#     'django.core.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.sessions.SessionMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

ROOT_URLCONF = '<#proj_name#>.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    '<#proj_dir#>/<#proj_name#>/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
)
''')

text = T('''<#body#>''')