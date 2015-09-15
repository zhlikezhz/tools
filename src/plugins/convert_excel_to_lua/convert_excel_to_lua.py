import os
from common import common

def convert_dic_to_lua(dic):
	lua = {}
	return lua


def convert_excel_to_lua(filename):
	excel = common.ToolsUtil.load_excel(filename)
	dic = common.ToolsUtil.convert_excel_to_dic(excel)
	lua = convert_dic_to_lua(dic)
	# lua = convert_dic_to_lua(dic)
