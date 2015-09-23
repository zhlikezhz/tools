# -*- coding: utf-8 -*-

import os
import sys
from units import Story
import StoryEditorView
from PyQt4 import QtGui, QtCore
# from StroyTree import StoryTree

class storyWindow(QtGui.QMainWindow, StoryEditorView.Ui_storyWindow):

	def __init__(self, parent = None):
		super(storyWindow, self).__init__(parent)
		super(storyWindow, self).setupUi(self)

	def newCard(self):
		self.scriptTree.insertRow()

	def newDialog(self):
		self.chapterView.insertRow()

	def newStory(self):
		print("new")

	def saveStory(self):
		print("save")
		if(self.story):
			self.story.saveStory(self.story.getCurrStoryFileName())

	def saveToLua(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"save story", ".", 
										"story (*.lua)")
		if(filename.isEmpty() == False and self.story):
			self.story.saveToLua(filename)

	def openStory(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"open story", ".", 
										"story (*.lua)(*.xml)")
		if(filename.isEmpty() == False):
			self.loadStoryFile(filename)

	def loadStoryFile(self, filename):
		self.story = Story()
		self.statusBar.showMessage("loading " + filename, 2000)
		self.story.loadStory(unicode(filename.toUtf8(), 'utf-8', 'ignore'))
		self.statusBar.showMessage("file load success", 2000)
		self.scriptTree.setData(self.story.getStoryData())

	def clickStory(self, card, story):
		self.chapterView.setData(self.story.getCardStoryData(card, story))

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	storyWindow = storyWindow()
	storyWindow.show()
	sys.exit(app.exec_())
