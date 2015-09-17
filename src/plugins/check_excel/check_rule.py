import os
import sys
# from common import common
from PyQt4 import QtCore, QtGui
import xml.etree.ElementTree as xml

class Rule:
	types = ""
	des_excel_sheet_col = ""
	src_excel_sheet_col = ""
	des_excel_sheet_name = ""
	src_excel_sheet_name = ""
	des_excel_name = ""
	src_excel_name = ""

	def __init__(self):
		print ""

class CheckRule:
	root = None
	rules = None
	repeats = None
	excel_path = None
	save_rules_list = None
	xml_path = ""

	def __init__(self):
		# xml_path = common.ToolsUtil.plugin_path
		self.xml_path = "E:/codes/projects/tools/src/plugins/check_excel"
		self.xml_path = os.path.join(self.xml_path, "excel_check_rule.xml")
		self.excel_check_rule = xml.parse(self.xml_path)

		self.root = self.excel_check_rule.getroot()
		self.excel_path = self.root.attrib["src_directory"]
		self.rules = self.get_excel_rule_list()
		self.repeats = self.get_excel_repeat_list()

	def get_excel_rule_list(self):
		rules = []
		rule_list = self.root.find("rule_list")
		for val in rule_list:
			rule = Rule()
			rule.src_excel_name = val.attrib["src_excel_name"]
			rule.src_excel_sheet_name = val.attrib["src_excel_sheet_name"]
			rule.src_excel_sheet_col = val.attrib["src_excel_sheet_col"]
			rule.des_excel_name = val.attrib["des_excel_name"]
			rule.des_excel_sheet_name = val.attrib["des_excel_sheet_name"]
			rule.des_excel_sheet_col = val.attrib["des_excel_sheet_col"]
			rules.append(rule)
		return rules

	def get_excel_repeat_list(self):
		repeats = []
		repeat_list = self.root.find("repeat_list")
		for val in repeat_list:
			rule = Rule()
			rule.src_excel_name = val.attrib["src_excel_name"]
			rule.src_excel_sheet_name = val.attrib["src_excel_sheet_name"]
			rule.src_excel_sheet_col = val.attrib["src_excel_sheet_col"]
			repeats.append(rule)
		return repeats

	def save_rules(self):
		if(self.save_rules == None):
			return

		root = xml.Element('check_list', {'src_directory' : self.excel_path})
		tree = xml.ElementTree(root)

		rule_list = xml.Element("rule_list")
		repeat_list = xml.Element("repeat_list")
		root.append(rule_list)
		root.append(repeat_list)

		for val in self.save_rules_list:
			rule = xml.Element(val.types,
					{'src_excel_name' : val.src_excel_name,
					'src_excel_sheet_name' : val.src_excel_sheet_name,
					'src_excel_sheet_col' : val.src_excel_sheet_col,
					'des_excel_name' : val.des_excel_name,
					'des_excel_sheet_name' : val.des_excel_sheet_name,
					'des_excel_sheet_col' : val.des_excel_sheet_col})

			if(val.types == "rule"):
				rule_list.append(rule)
			else:
				repeat_list.append(rule)

		tree.write(self.xml_path, "utf-8")