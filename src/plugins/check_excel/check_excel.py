import os
import sys
import xlrd
from common import common
import xml.etree.ElementTree as xml

class Rule:
	des_excel_sheet_col = ""
	src_excel_sheet_col = ""
	des_excel_sheet_name = ""
	src_excel_sheet_name = ""
	des_excel_name = ""
	src_excel_name = ""

	def __init__(self):
		print ""

def load_excel(filename):
    try:
        excel = xlrd.open_workbook(filename)
        return excel
    except Exception, e:
    	print "[error: file not exist]: \n[file name: %s]" % (filename)
        print(e)
        exit(1)

def get_excel_row(filename, sheet_name, sheet_col):
    excel = load_excel(filename)
    sheet = excel.sheet_by_name(sheet_name)

    count = 0
    first_row_data = sheet.row_values(0)
    for i in first_row_data:
        if(i == sheet_col):
            return sheet.col_values(count)[1:]
        count = count + 1

    print "[error: sheet not exist]: \n[sheet: %s][column: %s]" % (sheet_name, sheet_col)
    exit(1)

def check_excel_rule(rule, excel_path):
	des_full_file_name = os.path.join(excel_path, rule.des_excel_name)
	des_col = get_excel_row(des_full_file_name, rule.des_excel_sheet_name, rule.des_excel_sheet_col)

	src_full_file_name = os.path.join(excel_path, rule.src_excel_name)
	src_col = get_excel_row(src_full_file_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col)

	for src in src_col:
		sign = False
		for des in des_col:
			if(src == des):
				sign = True
				break
		if(sign == False):
			print "[error: rule error]: \n[filename: %s][sheet: %s][column: %s][value: %s] not exist in [filename: %s][sheet: %s][column: %s]" % (rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, src, rule.des_excel_name, rule.des_excel_sheet_name, rule.des_excel_sheet_col) 

def check_excel_repeat(rule, excel_path):
	src_full_file_name = os.path.join(excel_path, rule.src_excel_name)
	src_col = get_excel_row(src_full_file_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col)

	dic_id = {}
	for id in src_col:
		if(dic_id.get(id, False) == True):
			print "[error: repeat error]: \n[filename: %s][sheet: %s][column: %s][value: %s]" % (rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, id)
		else:
			dic_id[id] = True

def get_excel_rule_list(root):
	rules = []
	rule_list = root.find("rule_list")
	for val in rule_list:
		rule = Rule
		rule.src_excel_name = val.attrib["src_excel_name"]
		rule.src_excel_sheet_name = val.attrib["src_excel_sheet_name"]
		rule.src_excel_sheet_col = val.attrib["src_excel_sheet_col"]
		rule.des_excel_name = val.attrib["des_excel_name"]
		rule.des_excel_sheet_name = val.attrib["des_excel_sheet_name"]
		rule.des_excel_sheet_col = val.attrib["des_excel_sheet_col"]
		rules.append(rule)
	return rules

def get_excel_repeat_list(root):
	repeats = []
	repeat_list = root.find("repeat_list")
	for val in repeat_list:
		rule = Rule
		rule.src_excel_name = val.attrib["src_excel_name"]
		rule.src_excel_sheet_name = val.attrib["src_excel_sheet_name"]
		rule.src_excel_sheet_col = val.attrib["src_excel_sheet_col"]
		repeats.append(rule)
	return repeats


if __name__ != '__main__':
	xml_path = common.ToolsUtil.plugin_path
	xml_path = os.path.join(xml_path, "excel_check_rule.xml")
	excel_check_rule = xml.parse(xml_path)

	root = excel_check_rule.getroot()
	excel_path = root.attrib["src_directory"]

	rule_list = get_excel_rule_list(root)
	for rule in rule_list:
		check_excel_rule(rule, excel_path)

	repeat_list = get_excel_repeat_list(root)
	for rule in repeat_list:
		check_excel_repeat(rule, excel_path)