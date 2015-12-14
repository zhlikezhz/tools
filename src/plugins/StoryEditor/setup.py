import py2exe
from distutils.core import setup

setup(windows=[{"script":"MainWin.py"}], options={"py2exe":{"includes":["sip"]}})