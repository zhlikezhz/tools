# -*- coding: utf-8 -*-
import sys
import UIExcelEditor 
from RuleEdit import RuleEdit
from OpenFolder import ExcelFileModel
from PyQt4 import QtGui, QtCore

class ExcelEditor(QtGui.QMainWindow, UIExcelEditor.Ui_excelCheckWin):

	def __init__(self, parent = None):
		super(ExcelEditor, self).__init__(parent)
		self.setupUi(self)
		self.mFileList = []
		self.mDirPath = ''

	def addRule(self):
		rule = RuleEdit(self)
		rule.setDirPath(self.mDirPath)
		rule.setFileList(self.mFileList)
		rule.show()
		pass

	def deleteRule(self):
		pass

	def saveRules(self):
		pass

	def openRules(self):
		pass

	def openFolder(self):
		dirName = QtGui.QFileDialog.getExistingDirectory(self, "导入文件夹", ".")
		if(dirName.isEmpty() == False):
			self.mDirPath = dirName
			model = ExcelFileModel()
			model.setDirPath(dirName)
			self.mFileList = model.fileList
			self.listView.setModel(model)

	def runRule(self):
		pass

	def runRules(self):
		pass

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	app = QtGui.QApplication(sys.argv)
	excelCheckWin = ExcelEditor()
	excelCheckWin.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
