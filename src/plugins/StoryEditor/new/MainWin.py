# -*- coding: utf-8 -*-
import os
import sys
import copy
import units
import UIMainWin
import StoryData
from PyQt4 import QtGui, QtCore

def getTypelist():
	typeList = [
		{'val': '对话', 'key': 'dialog'},
		{'val': '分支', 'key': 'branch'},
		{'val': '分支选择', 'key': 'choose'},
	]
	return typeList

def typeMapping(types):
	val = "类型"
	if(types == 'choose'):
		val = '分支选择'
	elif(types == 'dialog'):
		val = '对话'
	elif(types == 'branch'):
		val = '分支'
	return val


class MainWin(QtGui.QMainWindow, UIMainWin.Ui_storyWindow):
	def __init__(self, parent = None):
		super(MainWin, self).__init__(parent)
		super(MainWin, self).setupUi(self)

		self.lock = False

		cnt = 0
		typeList = getTypelist()
		for val in typeList:
			tmp = QtCore.QString.fromUtf8(val['val'])
			self.typeCombo.insertItem(cnt, tmp)
			cnt = cnt + 1

		self.storyMgr = None
		self.chapterView.setView(self)
		self.storyView.setView(self)
		self.attributeView.setView(self)

	def setAttributeData(self, unitData):
		self.lock = True

		data = copy.deepcopy(unitData.attrib)
		self.dialogEdit.setText(unitData.sentence)

		cnt = 0
		typeList = getTypelist()
		for val in typeList:
			if(unitData.type == val['key']):
				break
			cnt = cnt + 1
		self.typeCombo.setCurrentIndex(cnt)
		self.attributeView.setData(data)

		self.lock = False

	def getAttributeData(self):
		unitData = StoryData.UnitData('element')
		index = self.typeCombo.currentIndex()
		if(self.lock == False):
			typeList = getTypelist()
			unitData.type = typeList[index]['key']
			unitData.attrib = self.attributeView.getData()
			unitData.sentence = units._toUtf8(self.dialogEdit.toPlainText())
			self.chapterView.setAttbribute(unitData)

	def cellChanged(self):
		self.getAttributeData()

	def setChapterData(self, unitData):
		self.chapterView.setData(unitData)

	def setStoryData(self, unitData):
		self.storyView.setData(unitData)

	def newStory(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 
										"save story to lua", ".", 
										"story file(*.xml)")
		if(filename.isEmpty() == False):
			self.filename = filename
			self.storyMgr = StoryData.StoryMgr()
			self.storyMgr.newData()
			self.setStoryData(self.storyMgr.getStoryData())
			self.setChapterData(StoryData.UnitData())
			self.setAttributeData(StoryData.UnitData())

	def openStory(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 
										"open story", ".", 
										"story (*.lua)(*.xml)")
		if(filename.isEmpty() == False):
			self.filename = filename
			self.storyMgr = StoryData.StoryMgr()
			self.storyMgr.loadData(filename)
			self.setStoryData(self.storyMgr.getStoryData())
			self.setChapterData(StoryData.UnitData())
			self.setAttributeData(StoryData.UnitData())

	def saveStory(self):
		if(self.storyMgr != None):
			if not (os.path.exists(self.filename)):
				return 

			self.storyMgr.save2Xml(self.filename)

	def saveToLua(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 
										"save story to lua", ".", 
										"story file(*.lua)")
		if(filename.isEmpty() == False and self.storyMgr != None):
			filename = units._toUtf8(filename)
			self.storyMgr.save2Lua(filename)

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWin()
	mainWin.show()
	sys.exit(app.exec_())