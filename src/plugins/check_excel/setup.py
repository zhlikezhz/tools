import py2exe
from distutils.core import setup

setup(windows=[{"script":"mainView.py"}], options={"py2exe":{"includes":["sip"]}})