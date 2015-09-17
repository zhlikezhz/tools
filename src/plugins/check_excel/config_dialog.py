#-*- coding: utf-8 -*- 
import os
import sys
import check_rule
import file_brower_dialog
from PyQt4 import QtCore, QtGui

class ConfigDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		super(ConfigDialog, self).__init__(parent)

		self.initConfigTable()

		self.addressBtn = QtGui.QPushButton()
		self.addressBtn.setText(self.rule.excel_path)

		self.addBtn = QtGui.QPushButton()
		self.addBtn.setText("add")

		self.removeBtn = QtGui.QPushButton()
		self.removeBtn.setText("remove")

		self.saveBtn = QtGui.QPushButton()
		self.saveBtn.setText("save")

		self.cancelBtn = QtGui.QPushButton()
		self.cancelBtn.setText("cancel")

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		horizontalLayout = QtGui.QHBoxLayout()
		horizontalLayout.addWidget(self.addBtn)
		horizontalLayout.addWidget(self.removeBtn)
		horizontalLayout.addItem(spacerItem)
		horizontalLayout.addWidget(self.saveBtn)
		horizontalLayout.addWidget(self.cancelBtn)

		verticalLayout = QtGui.QVBoxLayout(self)
		verticalLayout.addWidget(self.addressBtn)
		verticalLayout.addWidget(self.tableWidget)
		verticalLayout.addLayout(horizontalLayout)
		
		QtCore.QObject.connect(self.addBtn, QtCore.SIGNAL("clicked()"), self.onAddBtn)
		QtCore.QObject.connect(self.removeBtn, QtCore.SIGNAL("clicked()"), self.onRemoveBtn)
		QtCore.QObject.connect(self.saveBtn, QtCore.SIGNAL("clicked()"), self.onSaveBtn)
		QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.onCancelBtn)
		QtCore.QObject.connect(self.addressBtn, QtCore.SIGNAL("clicked()"), self.onAddressBtn)


	def initConfigTable(self):
		self.rule = check_rule.CheckRule()

		column = 7
		row = len(self.rule.rules) + len(self.rule.repeats) + 1
		self.tableWidget = QtGui.QTableWidget(row, column)

		text = ["type", "src_name", "src_sheet", "src_column", "des_name", "des_sheet", "des_column"]
		for i in range(0, column):
			textItem = QtGui.QTableWidgetItem(text[i])
			self.tableWidget.setItem(0, i, textItem)

		for i in range(0, len(self.rule.rules)):
			row = i + 1
			self.addItem(row, "rule", self.rule.rules[i])

		for i in range(0, len(self.rule.repeats)):
			row = i + len(self.rule.rules) + 1
			repeat = self.rule.repeats[i]
			self.addItem(row, "repeat", self.rule.repeats[i])

	def setExcelPath(self, excel_path):
		# self.rule.excel_path = excel_path
		self.addressBtn.setText(excel_path)

	def onAddressBtn(self):
		self.fileBrower = file_brower_dialog.FileBrower(self)
		self.fileBrower.show()

	def addItem(self, row, type, rule):
		textItem = QtGui.QTableWidgetItem(rule.src_excel_name)
		self.tableWidget.setItem(row, 1, textItem)
		textItem = QtGui.QTableWidgetItem(rule.src_excel_sheet_name)
		self.tableWidget.setItem(row, 2, textItem)
		textItem = QtGui.QTableWidgetItem(rule.src_excel_sheet_col)
		self.tableWidget.setItem(row, 3, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_name)
		self.tableWidget.setItem(row, 4, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_sheet_name)
		self.tableWidget.setItem(row, 5, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_sheet_col)
		self.tableWidget.setItem(row, 6, textItem)
		textItem = QtGui.QTableWidgetItem(type)
		self.tableWidget.setItem(row, 0, textItem)

	# def addCombox(self, row, type, rule):
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.src_excel_name)
		# self.tableWidget.setCellWidget(row, 1, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.src_excel_sheet_name)
		# self.tableWidget.setCellWidget(row, 2, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.src_excel_sheet_col)
		# self.tableWidget.setCellWidget(row, 3, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.des_excel_name)
		# self.tableWidget.setCellWidget(row, 4, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.des_excel_sheet_name)
		# self.tableWidget.setCellWidget(row, 5, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(rule.des_excel_sheet_col)
		# self.tableWidget.setCellWidget(row, 6, comboBox)
		# comboBox = QtGui.QComboBox()
		# comboBox.addItem(type)
		# self.tableWidget.setCellWidget(row, 0, comboBox)

		# if(type == "rule"):
		# 	comboBox.addItem("repeat")
		# else:
		# 	comboBox.addItem("rule")

	def onAddBtn(self):
		row = self.tableWidget.rowCount()
		self.tableWidget.insertRow(row)

	# def onAddBtn(self):
	# 	row = self.tableWidget.rowCount()
	# 	self.tableWidget.insertRow(row)
	# 	rule = check_rule.Rule()
	# 	self.addCombox(row, "rule", rule)

	def onRemoveBtn(self):
		currRow = self.tableWidget.currentRow()
		if(currRow > 0):
			self.tableWidget.removeRow(currRow)

	def onSaveBtn(self):
		row = self.tableWidget.rowCount()
		column = self.tableWidget.columnCount()

		self.rule.save_rules_list = []
		self.rule.excel_path = unicode(self.addressBtn.text(), 'utf-8', 'ignore')
		for i in range(1, row):
			rule = check_rule.Rule()
			rule.types = unicode(self.tableWidget.item(i, 0).text(), 'utf-8', 'ignore')
			rule.src_excel_name = unicode(self.tableWidget.item(i, 1).text(), 'utf-8', 'ignore')
			rule.src_excel_sheet_name = unicode(self.tableWidget.item(i, 2).text(), 'utf-8', 'ignore')
			rule.src_excel_sheet_col = unicode(self.tableWidget.item(i, 3).text(), 'utf-8', 'ignore')
			rule.des_excel_name = unicode(self.tableWidget.item(i, 4).text(), 'utf-8', 'ignore')
			rule.des_excel_sheet_name = unicode(self.tableWidget.item(i, 5).text(), 'utf-8', 'ignore')
			rule.des_excel_sheet_col = unicode(self.tableWidget.item(i, 6).text(), 'utf-8', 'ignore')
			self.rule.save_rules_list.append(rule)
		self.rule.save_rules()

	# def onSaveBtn(self):
	# 	row = self.tableWidget.rowCount()
	# 	column = self.tableWidget.columnCount()

	# 	self.rule.save_rules_list = []
	# 	for i in range(1, row):
	# 		rule = check_rule.Rule()
	# 		rule.types = unicode(self.tableWidget.cellWidget(i, 0).currentText(), 'utf-8', 'ignore')
	# 		rule.src_excel_name = unicode(self.tableWidget.cellWidget(i, 1).currentText(), 'utf-8', 'ignore')
	# 		rule.src_excel_sheet_name = unicode(self.tableWidget.cellWidget(i, 2).currentText(), 'utf-8', 'ignore')
	# 		rule.src_excel_sheet_col = unicode(self.tableWidget.cellWidget(i, 3).currentText(), 'utf-8', 'ignore')
	# 		rule.des_excel_name = unicode(self.tableWidget.cellWidget(i, 4).currentText(), 'utf-8', 'ignore')
	# 		rule.des_excel_sheet_name = unicode(self.tableWidget.cellWidget(i, 5).currentText(), 'utf-8', 'ignore')
	# 		rule.des_excel_sheet_col = unicode(self.tableWidget.cellWidget(i, 6).currentText(), 'utf-8', 'ignore')
	# 		self.rule.save_rules_list.append(rule)
	# 	self.rule.save_rules()

	def onCancelBtn(self):
		self.close()