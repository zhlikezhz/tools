# -*- coding: utf-8 -*-
import os
import sys
import units
import UIRuleEdit
from ExcelMgr import ExcelMgr
from PyQt4 import QtGui, QtCore

class RuleEdit(QtGui.QDialog, UIRuleEdit.Ui_Dialog):
	def __init__(self, parent = None):
		super(RuleEdit, self).__init__(parent)
		self.setupUi(self)

		self.mDirPath = ''
		self.srcFullPath = ''
		self.descFullPath = ''
		self.mFileList = []

		self.comboBox.addItem(units._fromUtf8('关联'))
		self.comboBox.addItem(units._fromUtf8('格式匹配'))
		self.comboBox.addItem(units._fromUtf8('数据范围'))

	def setFileList(self, fileList):
		self.mFileList = fileList
		for name in fileList:
			self.comboBox_2.addItem(units._fromUtf8(name))
			self.comboBox_5.addItem(units._fromUtf8(name))

	def setDirPath(self, dirPath):
		self.mDirPath = unicode(dirPath.toUtf8(), 'utf-8', 'ignore')

	def onSaveBtn(self):
		self.accept()

	def onCancelBtn(self):
		self.reject()

	def changeType(self, string):
		pass

	def changeSrcFile(self, string):
		string = unicode(string.toUtf8(), 'utf-8', 'ignore')
		self.srcFullPath = os.path.join(self.mDirPath, string)
		if(os.path.exists(self.srcFullPath) == False):
			return 

		sheets = ExcelMgr.getExcelSheets(self.srcFullPath)

		self.comboBox_3.clear()
		for name in sheets:
			self.comboBox_3.addItem(units._fromUtf8(name))

	def changeSrcSheet(self, string):
		if(os.path.exists(self.srcFullPath) == False):
			return 
		string = unicode(string.toUtf8(), 'utf-8', 'ignore')
		if(len(string) < 1):
			return 
		titles = ExcelMgr.getExcelTitles(self.srcFullPath, string)

		self.comboBox_4.clear()
		for name in titles:
			self.comboBox_4.addItem(units._fromUtf8(name))


	def changeSrcTitle(self, string):
		pass

	def changeDescFile(self, string):
		string = unicode(string.toUtf8(), 'utf-8', 'ignore')
		self.descFullPath = os.path.join(self.mDirPath, string)
		if(os.path.exists(self.descFullPath) == False):
			return 
		sheets = ExcelMgr.getExcelSheets(self.descFullPath)

		self.comboBox_6.clear()
		for name in sheets:
			self.comboBox_6.addItem(units._fromUtf8(name))

	def changeDescSheet(self, string):
		if(os.path.exists(self.descFullPath) == False):
			return 

		string = unicode(string.toUtf8(), 'utf-8', 'ignore')
		if(len(string) < 1):
			return 

		titles = ExcelMgr.getExcelTitles(self.descFullPath, string)

		self.comboBox_7.clear()
		for name in titles:
			self.comboBox_7.addItem(units._fromUtf8(name))

	def changeDescTitle(self, string):
		pass
