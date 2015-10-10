# -*- coding: utf-8 -*-
import sys
import units
import UIExcelEditor 
from CheckRule import CheckUnit, CheckRule
from OpenFolder import ExcelFileModel
from PyQt4 import QtGui, QtCore

class ExcelEditor(QtGui.QMainWindow, UIExcelEditor.Ui_excelCheckWin):
	mXmlPath = ''
	mDirPath = ''
	mFileList = []

	def __init__(self, parent = None):
		super(ExcelEditor, self).__init__(parent)
		self.setupUi(self)
		self.tableView.setParent(self)

	def addRule(self):
		self.tableView.addItem()

	def deleteRule(self):
		self.tableView.removeItem()

	def saveRules(self):
		if(len(self.mXmlPath) > 0):
			rules = self.tableView.getRules()
			units.saveXml(self.mXmlPath, self.mDirPath, rules)

	def openRules(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"new rule", ".", 
										"rule file(*.xml)")
		if(filename.isEmpty() == False):
			self.mXmlPath = filename.toUtf8()
			data = units.loadXml(self.mXmlPath)
			self.tableView.setRules(data['rules'])
			self.mDirPath = data['dirname']
			self.loadFolder(self.mDirPath)

	def newRules(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 
										"new rule", ".", 
										"rule file(*.xml)")
		if(filename.isEmpty() == False):
			self.saveRules()
			self.mXmlPath = filename.toUtf8()
			self.tableView.setRules([])
			self.listView.setModel(ExcelFileModel())

	def openFolder(self):
		dirName = QtGui.QFileDialog.getExistingDirectory(self, "导入文件夹", ".")
		if(dirName.isEmpty() == False):
			self.mDirPath = unicode(dirName.toUtf8(), 'utf-8', 'ignore')
			self.loadFolder(dirName)

	def loadFolder(self, dirName):
		print dirName
		model = ExcelFileModel()
		model.setDirPath(dirName)
		self.mFileList = model.fileList
		self.listView.setModel(model)

	def runRule(self):
		pass

	def runRules(self):
		cnt = 0
		self.saveRules()
		rules = self.tableView.getRules()
		for rule in rules:
			cnt = cnt + 1
			check = CheckRule()
			re = check.check(rule, self.mDirPath)
			if(re == -1):
				print check.error()
				self.textBrowser_2.append(check.error())
				self.textBrowser_2.append('----------------------------------')
				self.textBrowser_2.append('----------------------------------')
				self.textBrowser.append('rule %d error!!!' % (cnt))
			else:
				self.textBrowser.append('rule %d success.' % (cnt))


def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	app = QtGui.QApplication(sys.argv)
	excelCheckWin = ExcelEditor()
	excelCheckWin.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
