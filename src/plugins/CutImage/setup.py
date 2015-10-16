import py2exe
from distutils.core import setup

setup(windows = ["CutImage.py"], options = {"py2exe":{"dll_excludes":["VCOMP90.DLL"]}})