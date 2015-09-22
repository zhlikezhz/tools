# -*- coding: utf-8 -*-

import os
import sys
import StoryEditorView
from PyQt4 import QtGui, QtCore

class storyWindow(QtGui.QMainWindow, StoryEditorView.Ui_storyWindow):

	def __init__(self, parent = None):
		super(storyWindow, self).__init__(parent)
		super(storyWindow, self).setupUi(self)

	def newStory(self):
		print("new")

	def saveStory(self):
		print("save")

	def openStory(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"open story", ".", 
										"story (*.lua)")
		if(filename.isEmpty() == False):
			self.loadStoryFile(filename)

	def loadStoryFile(self, filename):
		print("load %s" % (filename))
		self.statusBar.showMessage("file load success", 2000)

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	storyWindow = storyWindow()
	storyWindow.show()
	sys.exit(app.exec_())
