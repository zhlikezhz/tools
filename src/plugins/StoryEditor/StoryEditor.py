# -*- coding: utf-8 -*-

import os
import sys
import units
import StoryEditorView
from PyQt4 import QtGui, QtCore

class storyWindow(QtGui.QMainWindow, StoryEditorView.Ui_storyWindow):

	def __init__(self, parent = None):
		self.isOpen = False
		super(storyWindow, self).__init__(parent)
		super(storyWindow, self).setupUi(self)

		cnt = 0
		typeList = units.getTypelist()
		for val in typeList:
			tmp = QtCore.QString.fromUtf8(val['val'])
			self.typeCombo.insertItem(cnt, tmp)
			cnt = cnt + 1

		self.scriptTree.setParent(self)
		self.attrTable.setParent(self)
		self.attrTable.clear()


	def newCard(self):
		self.scriptTree.appendRow()

	def newDialog(self):
		self.chapterView.appendRow()

	def newStory(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 
										"save story to lua", ".", 
										"story file(*.xml)")
		if(filename.isEmpty() == False):
			self.newStoryFile(unicode(filename.toUtf8(), 'utf-8', 'ignore'))

	def saveStory(self):
		print("save")
		if(self.story):
			self.story.saveStory(self.story.getCurrStoryFileName())

	def saveToLua(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 
										"save story to lua", ".", 
										"story file(*.lua)")
		if(filename.isEmpty() == False and self.story):
			self.story.saveToLua(unicode(filename.toUtf8(), 'utf-8', 'ignore'))

	def openStory(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"open story", ".", 
										"story (*.lua)(*.xml)")
		if(filename.isEmpty() == False):
			self.loadStoryFile(filename)

	def loadStoryFile(self, filename):
		self.story = units.Story(self)
		self.statusBar.showMessage("loading " + filename, 2000)
		self.story.loadStory(unicode(filename.toUtf8(), 'utf-8', 'ignore'))
		self.statusBar.showMessage("file load success", 2000)
		self.scriptTree.setData(self.story.getStoryData())

	def newStoryFile(self, filename):
		self.story = units.Story(self)
		self.statusBar.showMessage("loading " + filename, 2000)
		self.story.newStory(filename)
		self.scriptTree.setData(self.story.getStoryData())


	def clickStory(self, card, story):
		self.chapterView.setData(self.story.getCardStoryData(card, story))

	def showWords(self): 
		totalCnt = self.story.calTotalWords()
		self.statusBar.showMessage('total: ' + str(totalCnt))

	def showCardWords(self, card):
		totalCnt = self.story.calCardWords(card)
		self.statusBar.showMessage('card: ' + str(totalCnt))

	def showStoryWords(self, story):
		totalCnt = self.story.calStoryWords(story)
		self.statusBar.showMessage('story: ' + str(totalCnt))


	def setData(self, data):
		self.isOpen = False
		typeList = units.getTypelist()
		cnt = 0
		for val in typeList:
			if(data.itemData['type'] == val['key']):
				break
			cnt = cnt + 1
		self.typeCombo.setCurrentIndex(cnt)
		self.dialogEdit.setText(data.itemData['sentence'])
		self.attrTable.setData(data.itemData['attr'])
		self.isOpen = True

	def cellChanged(self):
		if(self.isOpen):
			self.getData()

	def cellChanged1(self, row, col):
		if(self.isOpen):
			self.getData()

	def getData(self):
		data = {}

		dialogVal = self.dialogEdit.toPlainText()
		data['sentence'] = unicode(dialogVal.toUtf8(), 'utf-8', 'ignore')

		typeList = units.getTypelist()
		index = self.typeCombo.currentIndex()
		data['type'] = typeList[index]['key']
		data['attr'] = self.attrTable.getData()
		self.chapterView.setAttr(data)

	def closeEvent(self, event): 
		ret = QtGui.QMessageBox.warning(self, units._fromUtf8('保存'), 
			units._fromUtf8('是否保存？'), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) 
		if(ret == QtGui.QMessageBox.Yes):
			self.saveStory()
		event.accept()


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	storyWindow = storyWindow()
	storyWindow.show()
	sys.exit(app.exec_())
