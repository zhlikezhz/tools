import py2exe
from distutils.core import setup

setup(windows=[{"script":"StoryEditor.py"}], options={"py2exe":{"includes":["sip"]}})