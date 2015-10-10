# -*- coding: utf-8 -*-
import os
import sys
import units
import UIRuleEdit
from CheckRule import CheckUnit
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

		self.unit = CheckUnit()

	def setFileList(self, fileList):
		self.mFileList = fileList
		for name in fileList:
			self.comboBox_2.addItem(units._fromUtf8(name))
			self.comboBox_5.addItem(units._fromUtf8(name))

	def setDirPath(self, dirPath):
		self.mDirPath = dirPath

	def getCheckUnit(self):
		return self.unit

	def setCheckUnit(self, unit):
		self.unit = unit
		idx = self.comboBox.findText(units._fromUtf8(unit.mType))
		if(idx != -1):
			self.comboBox.setCurrentIndex(idx)

		idx = self.comboBox_2.findText(units._fromUtf8(unit.mSrcName))
		if(idx != -1):
			self.comboBox_2.setCurrentIndex(idx)

		idx = self.comboBox_3.findText(units._fromUtf8(unit.mSrcSheet))
		if(idx != -1):
			self.comboBox_3.setCurrentIndex(idx)

		idx = self.comboBox_4.findText(units._fromUtf8(unit.mSrcTitle))
		if(idx != -1):
			self.comboBox_4.setCurrentIndex(idx)

		idx = self.comboBox_5.findText(units._fromUtf8(unit.mDescName))
		if(idx != -1):
			self.comboBox_5.setCurrentIndex(idx)

		idx = self.comboBox_6.findText(units._fromUtf8(unit.mDescSheet))
		if(idx != -1):
			self.comboBox_6.setCurrentIndex(idx)

		idx = self.comboBox_7.findText(units._fromUtf8(unit.mDescTitle))
		if(idx != -1):
			self.comboBox_7.setCurrentIndex(idx)

		self.textEdit.setText(units._fromUtf8(unit.mRule))

	def onSaveBtn(self):
		self.unit.mType = unicode(self.comboBox.currentText(), 'utf-8', 'ignore')
		self.unit.mRule = unicode(self.textEdit.toPlainText(), 'utf-8', 'ignore')
		self.unit.mSrcName = unicode(self.comboBox_2.currentText(), 'utf-8', 'ignore')
		self.unit.mSrcSheet = unicode(self.comboBox_3.currentText(), 'utf-8', 'ignore')
		self.unit.mSrcTitle = unicode(self.comboBox_4.currentText(), 'utf-8', 'ignore')
		self.unit.mDescName = unicode(self.comboBox_5.currentText(), 'utf-8', 'ignore')
		self.unit.mDescSheet = unicode(self.comboBox_6.currentText(), 'utf-8', 'ignore')
		self.unit.mDescTitle = unicode(self.comboBox_7.currentText(), 'utf-8', 'ignore')
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
