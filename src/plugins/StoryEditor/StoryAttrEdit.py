# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryAttrEditUI import Ui_storyAttrEditor


class StoryAttrEdit(QtGui.QDialog, Ui_storyAttrEditor):
	def __init__(self, parent = None):
		super(StoryAttrEdit, self).__init__(parent)
		self.setupUi(self)
		self.mParent = parent

		cnt = 0
		typeList = units.getTypelist()
		for val in typeList:
			tmp = QtCore.QString.fromUtf8(val['val'])
			self.typeCombo.insertItem(cnt, tmp)
			cnt = cnt + 1

	def setData(self, data):
		typeList = units.getTypelist()
		cnt = 0
		for val in typeList:
			if(data.itemData['type'] == val['key']):
				break
			cnt = cnt + 1
		self.typeCombo.setCurrentIndex(cnt)
		self.dialogEdit.setText(data.itemData['sentence'])
		self.attrTable.setData(data.itemData['attr'])

	def onSaveBtn(self):

		data = {}

		dialogVal = self.dialogEdit.toPlainText()
		data['sentence'] = unicode(dialogVal.toUtf8(), 'utf-8', 'ignore')

		typeList = units.getTypelist()
		index = self.typeCombo.currentIndex()
		data['type'] = typeList[index]['key']

		data['attr'] = self.attrTable.getData()
		# attrList = self.attrTable.getData()
		# for (key, value) in attrList.iteritems():
		# 	data['attr'][key] = value

		self.mParent.setAttr(data)
		self.accept()

	def onCalBtn(self):
		self.reject()
		pass



if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	app = QtGui.QApplication(sys.argv)
	storyWindow = StoryAttrEdit()
	storyWindow.show()
	sys.exit(app.exec_())

