import os
import sys
import xlrd
import check_rule
import config_dialog
from PyQt4 import QtCore, QtGui





class CheckDialog(QtGui.QWidget):

	def __init__(self, parent = None):
		super(CheckDialog, self).__init__(parent)

		self.verticalLayout = QtGui.QVBoxLayout(self)

		self.inputBox = QtGui.QTextBrowser(self)
		self.verticalLayout.addWidget(self.inputBox)

		self.horizontalLayout = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout)

		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)

		self.checkBtn = QtGui.QPushButton(self)
		self.horizontalLayout.addWidget(self.checkBtn)
		self.checkBtn.setText("check")

		self.configBtn = QtGui.QPushButton(self)
		self.horizontalLayout.addWidget(self.configBtn)
		self.configBtn.setText("config")

		self.setWindowTitle("check")
		QtCore.QObject.connect(self.checkBtn, QtCore.SIGNAL("clicked()"), self.onCheckBtn)
		QtCore.QObject.connect(self.configBtn, QtCore.SIGNAL("clicked()"), self.onConfigBtn)

	def onCheckBtn(self):
		self.inputBox.clear()

		# self.inputBox.append("begin................")

		rule = check_rule.CheckRule()
		if(rule == None):
			return None

		for val in rule.rules:
			self.check_excel_rule(val, rule.excel_path)

		for val in rule.repeats:
			self.check_excel_repeat(val, rule.excel_path)

		# self.inputBox.append("complete!!!!!!!!!!!!!!!")


	def onConfigBtn(self):
		config = config_dialog.ConfigDialog(self)
		config.show()


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
				self.inputBox.append("\n\n[error: rule error]: \n[filename: %s][sheet: %s][column: %s][value: %s] not exist in [filename: %s][sheet: %s][column: %s]\n\n" % (rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, src, rule.des_excel_name, rule.des_excel_sheet_name, rule.des_excel_sheet_col))

		if(dSign == False):
			self.inputBox.append("ok")



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
				self.inputBox.append("\n\n[error: repeat error]: \n[filename: %s][sheet: %s][column: %s][value: %s]\n\n" % (rule.src_excel_name, rule.src_excel_sheet_name, rule.src_excel_sheet_col, id))
			else:
				dic_id[id] = True

		if(dSign == False):
			self.inputBox.append("ok")

	def load_excel(self, filename): 
		try: 
			excel = xlrd.open_workbook(filename) 
			return excel
		except Exception, e: 
			self.inputBox.append("\n\n[error: file not exist]: \n[file name: %s]\n\n" % (filename)) 
			print(e) 
			return None
			# exit(1)

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
		self.inputBox.append("\n\n[error: sheet not exist]: \n[sheet: %s][column: %s]\n\n" % (sheet_name, sheet_col))
		return None
    	# exit(1)
