#!/usr/bin/env python
#coding=utf-8
# I know this hack is simple,but it is better than nothing.
#
#
#
import sys
import os.path
import fnmatch
def get_std_lib():
    if sys.platform == "win32":
        libdir = os.path.join(sys.prefix, "Lib")
    else:
        libdir = os.path.join(sys.prefix, "lib", os.path.basename(sys.prefix))
    sitelibdir = os.path.join(libdir, "site-packages")
    return libdir, sitelibdir


def get_names_from_lib(path, flag=False):
    """
    get import names from installed python dir
    """
    std_names = []
    extns = ["*.py"]
    try:    lst = os.listdir(path)
    except: return
    for file in lst:
        a = os.path.join(path, file)
        if os.path.isfile(a):
            for extn in extns:
                if fnmatch.fnmatch(file, str(extn)):
                    if flag:
                        std_names.insert(0, os.path.splitext(file)[0] + '?4')
                    else:
                        std_names.insert(0, os.path.splitext(file)[0])
                    continue 
        elif os.path.isdir(a):
            if os.path.exists(os.path.join(a, "__init__.py")):
                if flag:
                    std_names.insert(0, file + '?27')
                else:
                    std_names.insert(0, file)
    return std_names

def get_names_from_site_pkg():
    pass
