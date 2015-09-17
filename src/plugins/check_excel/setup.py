import py2exe
from distutils.core import setup

setup(windows=[{"script":"check_excel.py"}], options={"py2exe":{"includes":["sip"]}})