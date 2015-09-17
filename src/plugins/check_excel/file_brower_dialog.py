#-*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore, QtGui
import xml.etree.ElementTree as xml

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
		QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.onCancelBtn)

	def onConfirmBtn(self):
		index = self.treeView.currentIndex()
		if(index.isValid() == True):
			parent = self.parentWidget()
			parent.setExcelPath(self.fileSystem.filePath(index))
			self.close()
			# QtGui.QMessageBox.information(self, "Remove", ("%s") % (self.fileSystem.filePath(index)))


	def onCancelBtn(self):
		self.close()