# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\codes\qt\pyqt\test1\mainView.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import os
import re
import sys
import xlrd
import check_rule
import file_brower_dialog
from PyQt4 import QtCore, QtGui

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

class MainView(object):
    def setupUi(self, mainView):
        mainView.setObjectName(_fromUtf8("mainView"))
        mainView.resize(987, 662)
        mainView.setSizeGripEnabled(True)
        self.verticalLayoutWidget = QtGui.QWidget(mainView)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 281, 661))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.documentBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.documentBtn.setObjectName(_fromUtf8("documentBtn"))
        self.verticalLayout.addWidget(self.documentBtn)
        self.listView = QtGui.QListView(self.verticalLayoutWidget)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout.addWidget(self.listView)
        self.verticalLayoutWidget_2 = QtGui.QWidget(mainView)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(290, 0, 691, 661))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.textBrowser = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addBtn = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.addBtn.setObjectName(_fromUtf8("addBtn"))
        self.horizontalLayout.addWidget(self.addBtn)
        self.saveBtn = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.removeBtn = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.removeBtn.setObjectName(_fromUtf8("removeBtn"))
        self.horizontalLayout.addWidget(self.removeBtn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.convertBtn = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.convertBtn.setObjectName(_fromUtf8("convertBtn"))
        self.horizontalLayout.addWidget(self.convertBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        # self.tableView = QtGui.QTableView(self.verticalLayoutWidget_2)
        # self.tableView.setObjectName(_fromUtf8("tableView"))

        self.retranslateUi(mainView)
        QtCore.QMetaObject.connectSlotsByName(mainView)

    def retranslateUi(self, mainView):
        mainView.setWindowTitle(_translate("mainView", "MMEditor", None))
        self.documentBtn.setText(_translate("mainView", "PushButton", None))
        self.addBtn.setText(_translate("mainView", "增加", None))
        self.removeBtn.setText(_translate("mainView", "删除", None))
        self.convertBtn.setText(_translate("mainView", "运行", None))
        self.saveBtn.setText(_translate("mainView", "保存", None))

class MainDialog(QtGui.QDialog):

	def __init__(self, parent=None):
		super(MainDialog, self).__init__(parent)
		self.ui = MainView()
		self.ui.setupUi(self)

		QtCore.QObject.connect(self.ui.addBtn, QtCore.SIGNAL("clicked()"), self.onAddBtn)
		QtCore.QObject.connect(self.ui.removeBtn, QtCore.SIGNAL("clicked()"), self.onRemoveBtn)
		QtCore.QObject.connect(self.ui.convertBtn, QtCore.SIGNAL("clicked()"), self.onCheckBtn)
		QtCore.QObject.connect(self.ui.saveBtn, QtCore.SIGNAL("clicked()"), self.onSaveBtn)
		QtCore.QObject.connect(self.ui.documentBtn, QtCore.SIGNAL("clicked()"), self.onDocumentBtn)

		self.checkXml = check_rule.CheckRule()
		self.ui.documentBtn.setText(self.checkXml.excel_path)

		column = 7
		row = len(self.checkXml.rules) + len(self.checkXml.repeats) + len(self.checkXml.formats) + 1
		self.ui.tableWidget = QtGui.QTableWidget(row, column)
		self.ui.verticalLayout_2.addWidget(self.ui.tableWidget)

		text = ["type", "src_name", "src_sheet", "src_column", "des_name", "des_sheet", "des_column"]
		for i in range(0, column):
			textItem = QtGui.QTableWidgetItem(text[i])
			self.ui.tableWidget.setItem(0, i, textItem)

		for i in range(0, len(self.checkXml.rules)):
			row = i + 1
			self.addItem(row, "rule", self.checkXml.rules[i])

		for i in range(0, len(self.checkXml.repeats)):
			row = i + len(self.checkXml.rules) + 1
			self.addItem(row, "repeat", self.checkXml.repeats[i])

		for i in range(0, len(self.checkXml.formats)):
			row = i + len(self.checkXml.rules) + len(self.checkXml.repeats) + 1
			self.addItem(row, "format", self.checkXml.formats[i])

	def addItem(self, row, type, rule):
		textItem = QtGui.QTableWidgetItem(rule.src_excel_name)
		self.ui.tableWidget.setItem(row, 1, textItem)
		textItem = QtGui.QTableWidgetItem(rule.src_excel_sheet_name)
		self.ui.tableWidget.setItem(row, 2, textItem)
		textItem = QtGui.QTableWidgetItem(rule.src_excel_sheet_col)
		self.ui.tableWidget.setItem(row, 3, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_name)
		self.ui.tableWidget.setItem(row, 4, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_sheet_name)
		self.ui.tableWidget.setItem(row, 5, textItem)
		textItem = QtGui.QTableWidgetItem(rule.des_excel_sheet_col)
		self.ui.tableWidget.setItem(row, 6, textItem)

		comboBox = QtGui.QComboBox()
		self.ui.tableWidget.setCellWidget(row, 0, comboBox)
		comboBox.addItem(type)

		if(type == "rule"):
			comboBox.addItem("repeat")
			comboBox.addItem("format")
		elif(type == "repeat"):
			comboBox.addItem("rule")
			comboBox.addItem("format")
		elif(type == "format"):
			comboBox.addItem("repeat")
			comboBox.addItem("rule")
		else:
			comboBox.addItem("rule")
			comboBox.addItem("repeat")
			comboBox.addItem("format")


	def onAddBtn(self):
		row = self.ui.tableWidget.rowCount()
		self.ui.tableWidget.insertRow(row)
		rule = check_rule.Rule()
		self.addItem(row, "", rule)

	def onRemoveBtn(self):
		currRow = self.ui.tableWidget.currentRow()
		if(currRow > 0):
			self.ui.tableWidget.removeRow(currRow)

	def onSaveBtn(self):
		row = self.ui.tableWidget.rowCount()
		column = self.ui.tableWidget.columnCount()

		self.checkXml.save_rules_list = []
		self.checkXml.excel_path = unicode(self.ui.documentBtn.text(), 'utf-8', 'ignore')
		for i in range(1, row):
			rule = check_rule.Rule()
			rule.types = unicode(self.ui.tableWidget.cellWidget(i, 0).currentText(), 'utf-8', 'ignore')
			rule.src_excel_name = unicode(self.ui.tableWidget.item(i, 1).text(), 'utf-8', 'ignore')
			rule.src_excel_sheet_name = unicode(self.ui.tableWidget.item(i, 2).text(), 'utf-8', 'ignore')
			rule.src_excel_sheet_col = unicode(self.ui.tableWidget.item(i, 3).text(), 'utf-8', 'ignore')
			rule.des_excel_name = unicode(self.ui.tableWidget.item(i, 4).text(), 'utf-8', 'ignore')
			rule.des_excel_sheet_name = unicode(self.ui.tableWidget.item(i, 5).text(), 'utf-8', 'ignore')
			rule.des_excel_sheet_col = unicode(self.ui.tableWidget.item(i, 6).text(), 'utf-8', 'ignore')
			self.checkXml.save_rules_list.append(rule)
		self.checkXml.save_rules()



	def onCheckBtn(self):
		self.onSaveBtn()
		self.ui.textBrowser.clear()

		rule = check_rule.CheckRule()
		if(rule == None):
			return None

		for val in rule.rules:
			self.check_excel_rule(val, rule.excel_path)

		for val in rule.repeats:
			self.check_excel_repeat(val, rule.excel_path)

		for val in rule.formats:
			self.check_excel_format(val, rule.excel_path)


	def onDocumentBtn(self):
		self.fileBrower = file_brower_dialog.FileBrower(self)
		self.fileBrower.show()

	def setExcelPath(self, text):
		self.ui.documentBtn.setText(text)



	def check_excel_rule(self, rule, excel_path):
		des_full_file_name = os.path.join(excel_path, rule.des_excel_name)
		des_col = self.get_excel_row(des_full_file_name, rule.des_excel_sheet_name, rule.des_excel_sheet_col)
		if(des_col == None):
			return

		src_full_file_name = os.path.join(excel_path, rule.src_excel_name)
		src_col = self.get_excel_row(src_full_file_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col)
		if(src_col == None):
			return
		dSign = False

		for src in src_col:
			sign = False
			for des in des_col:
				if(src == des):
					sign = True
					break
			if(sign == False):
				dSign = True
				self.ui.textBrowser.append("[error: rule error]: \n[filename: %s][sheet: %s][column: %s][value: %s] \
					not exist in [filename: %s][sheet: %s][column: %s]\n-----------------------------------------------------------\n" % \
					(rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, src, rule.des_excel_name, rule.des_excel_sheet_name, rule.des_excel_sheet_col))

		if(dSign == False):
			self.ui.textBrowformatsend("ok")



	def check_excel_format(self, rule, excel_path):
		src_full_file_name = os.path.join(excel_path, rule.src_excel_name)
		src_col = self.get_excel_row(src_full_file_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col)
		if(src_col == None):
			return

		srcSting = src_col[0]
		srcFormat = ''.join(re.findall("[#$@&,.;:]", srcSting))

		row = 1
		for desString in src_col:
			desFormat = ''.join(re.findall("[#$@&,.;:]", desString))
			if(srcFormat == desFormat):
				print("")
			else:
				self.ui.textBrowser.append("[error: format error]: \
					\n[filename: %s][sheet: %s][column: %s][row: %s]\n\n[srouce string: %s]\n\n[fail string: %s]\n-----------------------------------------------------------\n" % \
					(rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, row, srcSting, desString))
			row = row + 1


	def check_excel_repeat(self, rule, excel_path):
		src_full_file_name = os.path.join(excel_path, rule.src_excel_name)
		src_col = self.get_excel_row(src_full_file_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col)
		if(src_col == None):
			return

		dSign = False
		dic_id = {}
		for id in src_col:
			if(dic_id.get(id, False) == True):
				dSign = True
				self.ui.textBrowser.append("[error: repeat error]: \n\
					[filename: %s][sheet: %s][column: %s][value: %s]\n-----------------------------------------------------------\n" % \
					(rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, id))
			else:
				dic_id[id] = True

		if(dSign == False):
			self.ui.textBrowser.append("ok")

	def load_excel(self, filename): 
		try: 
			excel = xlrd.open_workbook(filename) 
			return excel
		except Exception, e: 
			self.ui.textBrowser.append("\n\n[error: file not exist]: \n[file name: %s]\n\n" % (filename)) 
			return None

	def get_excel_row(self, filename, sheet_name, sheet_col): 
		excel = self.load_excel(filename) 
		if(excel == None):
			return
		sheet = excel.sheet_by_name(sheet_name) 

		count = 0 
		first_row_data = sheet.row_values(0) 
		for i in first_row_data: 
			if(i == sheet_col): 
				return sheet.col_values(count)[1:] 
			count = count + 1 
		self.ui.textBrowser.append("\n\n[error: sheet not exist]: \n[sheet: %s][column: %s]\n\n" % (sheet_name, sheet_col))
		return None


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	mainView = MainDialog()
	mainView.show()
	sys.exit(app.exec_())