import os
from CheckRule import CheckUnit
from PyQt4 import QtGui, QtCore
import xml.etree.ElementTree as xml

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


def loadXml(xmlPath):
	rules = []
	if(os.path.exists(xmlPath) == False):
		return 

	data = xml.parse(xmlPath)
	root = data.getroot()
	ruleList = root.find("rules")
	dirname = root.attrib['dirname']
	for val in ruleList:
		rule = CheckUnit()
		rule.mType = val.attrib["type"]
		rule.mRule = val.attrib["rule"]
		rule.mSrcName = val.attrib["src_excel_name"]
		rule.mSrcSheet = val.attrib["src_excel_sheet_name"]
		rule.mSrcTitle = val.attrib["src_excel_sheet_col"]
		rule.mDescName = val.attrib["des_excel_name"]
		rule.mDescSheet = val.attrib["des_excel_sheet_name"]
		rule.mDescTitle = val.attrib["des_excel_sheet_col"]
		rules.append(rule)

	ruleData = {
		'dirname' : dirname,
		'rules' : rules
	}

	return ruleData

def saveXml(xmlPath, dirName, rules):
	root = xml.Element('check_list', {'dirname' : dirName})
	tree = xml.ElementTree(root)
	ruleList = xml.Element("rules")
	root.append(ruleList)

	for val in rules:
		rule = xml.Element('rule',
							{'type' : val.mType,
							'rule' : val.mRule,
							'src_excel_name' : val.mSrcName,
							'src_excel_sheet_name' : val.mSrcSheet,
							'src_excel_sheet_col' : val.mSrcTitle,
							'des_excel_name' : val.mDescName,
							'des_excel_sheet_name' : val.mDescSheet,
							'des_excel_sheet_col' : val.mDescTitle})
		ruleList.append(rule)
	print xmlPath

	tree.write(xmlPath, "utf-8")