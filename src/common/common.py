__author__ = 'plantang'

import os
import time
import hashlib
from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ToolsUtil:
    plugin_path = ""
    command_args = []

    def __init__(self):
        print ''

    @staticmethod
    def get_day_time() :
        return time.strftime("%Y%m%d", time.localtime(time.time()))

    @staticmethod
    def get_second_time() :
        return time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(time.time()))

    @staticmethod
    def generate_file_md5value(file_name):
        with open(file_name, 'rb') as file_handle :
            m = hashlib.md5()
            m.update(file_handle.read())
            return m.hexdigest()

    @staticmethod
    def get_command_args():
        return ToolsUtil.command_args

    @staticmethod
    def print_log(*args):
        print(args)


