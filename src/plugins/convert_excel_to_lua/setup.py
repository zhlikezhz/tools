import py2exe
from distutils.core import setup

# setup(console=["convert_excel_to_lua.py"])
setup(windows=[{"script":"convert_excel_to_lua.py"}], options={"py2exe":{"includes":["sip"]}})