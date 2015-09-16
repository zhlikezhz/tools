import os
import sys
from PyQt4 import QtCore, QtGui


class FileBrower(QtGui.QDialog):

	def __init__(self, parent = None):
		super(FileBrower, self).__init__(parent)


		self.fileSystem = QtGui.QFileSystemModel()
		self.fileSystem.setRootPath(QtCore.QDir.currentPath())
		self.fileSystem.setFilter(QtCore.QDir.AllDirs)
		index = self.fileSystem.index(QtCore.QDir.currentPath())

		self.treeView = QtGui.QTreeView()
		self.treeView.setModel(self.fileSystem)
		self.treeView.expand(index);
		self.treeView.scrollTo(index);
		self.treeView.resizeColumnToContents(0)


		spacerItem = QtGui.QSpacerItem(40, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		self.confirmBtn = QtGui.QPushButton()
		self.confirmBtn.setText("confirm")

		self.cancelBtn = QtGui.QPushButton()
		self.cancelBtn.setText("cancel")

		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.addItem(spacerItem)
		self.horizontalLayout.addWidget(self.confirmBtn)
		self.horizontalLayout.addWidget(self.cancelBtn)

		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.verticalLayout.addWidget(self.treeView)
		self.verticalLayout.addLayout(self.horizontalLayout)

		QtCore.QObject.connect(self.confirmBtn, QtCore.SIGNAL("clicked()"), self.onConfirmBtn)

	def onConfirmBtn(self):
		index = self.treeView.currentIndex()
		if(index.isValid() == True):
			QtGui.QMessageBox.information(self, "Remove", ("%s") % (self.fileSystem.filePath(index)))


class ExcelConfigModify(QtGui.QDialog):

	def __init__(self, parent = None):
		super(ExcelConfigModify, self).__init__(parent)

		row = 5
		column = 6
		self.tableWidget = QtGui.QTableWidget(row, column)

		text = ["src_name", "src_sheet", "src_column", "des_name", "des_sheet", "des_column"]
		for i in range(0, column):
			textItem = QtGui.QTableWidgetItem(text[i])
			self.tableWidget.setItem(0, i, textItem)

		for i in range(1, row):
			for j in range(0, column):
				comboBox = QtGui.QComboBox()
				comboBox.addItem("1")
				self.tableWidget.setCellWidget(i, j, comboBox)

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
		verticalLayout.addWidget(self.tableWidget)
		verticalLayout.addLayout(horizontalLayout)
		
		QtCore.QObject.connect(self.addBtn, QtCore.SIGNAL("clicked()"), self.onAddBtn)
		QtCore.QObject.connect(self.removeBtn, QtCore.SIGNAL("clicked()"), self.onRemoveBtn)
		QtCore.QObject.connect(self.saveBtn, QtCore.SIGNAL("clicked()"), self.onSaveBtn)
		QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.onCancelBtn)


	def onAddBtn(self):
		print("1111111")
		row = self.tableWidget.rowCount()
		self.tableWidget.insertRow(row)
		row = self.tableWidget.rowCount()
		column = self.tableWidget.columnCount()
		for i in range(0, column):
			comboBox = QtGui.QComboBox()
			comboBox.addItem("0")
			self.tableWidget.setCellWidget(row, i, comboBox)


	def onRemoveBtn(self):
		print("2222222")
		currRow = self.tableWidget.currentRow()
		if(currRow > 0):
			self.tableWidget.removeRow(currRow)


	def onSaveBtn(self):
		print("3333333")


	def onCancelBtn(self):
		print("4444444")


class CheckExcelWidget(QtGui.QWidget):

	def __init__(self, parent = None):
		super(CheckExcelWidget, self).__init__(parent)

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
		text = 'check'
		self.inputBox.append("%s" % (text))

	def onConfigBtn(self):
		text = 'config'
		self.inputBox.append("%s" % (text))

def main():
	app = QtGui.QApplication(sys.argv)
	dialog = ExcelConfigModify()
	dialog.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
