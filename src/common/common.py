__author__ = 'plantang'

import os
import time
import hashlib

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


