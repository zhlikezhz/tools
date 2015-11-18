# -*- coding: utf-8 -*-
import os
import sys
import units
import xml.etree.ElementTree as xml
from PyQt4 import QtGui, QtCore

class Connect(object):
	def __init__(self):
		self.row = 0
		self.keyList = []

class Attrib(object):
	def __init__(self):
		self.key = ''
		self.type = ''
		self.value = ''
		self.connect = ''
		self.connectRow = -1
		self.hasConnect = False
		self.connectList = []
		self.comboList = []

class MComBoBox(QtGui.QComboBox):
	def __init__(self, parent = None):
		super(MComBoBox, self).__init__(parent)
		self.callbackList = []
		QtCore.QObject.connect(self, QtCore.SIGNAL(units._fromUtf8("currentIndexChanged(int)")), self.comboChanged)

	def setPosition(self, row, col):
		self.row = row
		self.column = col

	def comboChanged(self):
		for func in self.callbackList:
			func(self.row, self.column)

	def connectCallback(self, func):
		if(func):
			self.callbackList.append(func)


class StoryAttrTable(QtGui.QTableWidget):
	def __init__(self, parent = None):
		super(StoryAttrTable, self).__init__(parent)
		self.mparent = None
		self.mColCnt = 1
		self.mRowCnt = 0
		self.attribList = []
		self.configFileName = 'config.xml'
		self.data = {}

	def changed(self, row, col):
		string = unicode(self.cellWidget(row, col).currentText().toUtf8(), 'utf-8', 'ignore')
		self.updateComboValue(self.attribList[row].connectList, string)
		self.mparent.cellChanged1(row, col)

	def clear(self):
		self.setRowCount(0)
		self.setColumnCount(0)

		if(self.loadConfig()):
			self.mRowCnt = len(self.attribList)
			self.setRowCount(self.mRowCnt)
			self.setColumnCount(self.mColCnt)
			self.parseConfig(self.attribList)

			cnt = 0
			for row in self.attribList:
				string = row.key
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(string))
				self.setVerticalHeaderItem(cnt, item)

				if(row.type == 'combo'):
					combo = MComBoBox()
					combo.connectCallback(self.changed)
					# combo.connectCallback(self.mparent.cellChanged1)
					self.setCellWidget(cnt, 0, combo)
					combo.setPosition(cnt, 0)
					combo.addItem('')
					for info in row.comboList:
						combo.addItem(units._fromUtf8(info.key))
				elif(row.type == 'text'):
					self.setItem(cnt, 0, QtGui.QTableWidgetItem())
				cnt = cnt + 1

			cnt = 0
			colValue = ["值"]
			for string in colValue:
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(string))
				self.setHorizontalHeaderItem(cnt, item)
			cnt = cnt + 1
			self.resizeRowsToContents()
			self.resizeColumnsToContents()

			self.setCurrentCell(0, 0)

	def setParent(self, parent):
		self.mparent = parent

	def getData(self):

		data = {}
		if(os.path.exists(self.configFileName) == False):
			return self.data

		for row in range(0, self.mRowCnt):
			info = self.attribList[row]
			if(info.type == 'combo'):

				parent = ''
				if(info.connectRow >= 0):
					parent = unicode(self.cellWidget(info.connectRow, 0).currentText().toUtf8(), 'utf-8', 'ignore')

				string = unicode(self.cellWidget(row, 0).currentText().toUtf8(), 'utf-8', 'ignore')
				for combo in info.comboList:
					if(string == combo.key and (len(parent) == 0 or combo.connect == parent)):
						string = combo.value
						break
				if(len(string) > 0):
					data[info.value] = string
			elif(info.type == 'text'):
				string = unicode(self.item(row, 0).text().toUtf8(), 'utf-8', 'ignore')
				data[info.value] = string

		return data


	def setData(self, data):
		if( os.path.exists(self.configFileName) == False):
			return 

		updateVal = []
		updateStack = []
		for (key, val) in data.iteritems():
			print("key = %s value = %s" % (key, val))
			row = 0
			for attrib in self.attribList:
				if(attrib.value == key):
					if(attrib.connectRow >= 0):
						if attrib.connectRow in updateStack: 
							index = updateStack.index(attrib.connectRow)
							updateStack.insert(index, row)
							updateVal.insert(index, val)
						else:
							updateStack.append(row)
							updateVal.append(val)
					else:
						updateStack.append(row)
						updateVal.append(val)
				row += 1


		for row in range(0, len(self.attribList)):
			if row in updateStack:
				pass
			else:
				comboBox = self.cellWidget(row, 0)
				comboBox.setCurrentIndex(0)

		while len(updateStack):
			val = updateVal.pop()
			row = updateStack.pop()
			attrib = self.attribList[row]
			if(attrib.type == 'combo'):

				parent = ""
				if(attrib.connectRow >= 0):
					parent = unicode(self.cellWidget(attrib.connectRow, 0).currentText().toUtf8(), 'utf-8', 'ignore')

				for combo in attrib.comboList:
					if(combo.value == val and (len(parent) == 0 or combo.connect == parent)):
						comboBox = self.cellWidget(row, 0)
						idx = comboBox.findText(units._fromUtf8(combo.key))
						if(idx != -1):
							comboBox.setCurrentIndex(idx)
						else:
							comboBox.setCurrentIndex(0)
						val = combo.key
						break

				self.updateComboValue(attrib.connectList, val)

			elif(attrib.type == 'text'):
				item = self.item(row, 0)
				item.setText(units._fromUtf8(val))

	def updateComboValue(self, connectList, parent):
		for index in connectList:
			combo = self.cellWidget(index, 0)
			if(combo == None):
				return 
			attrib = self.attribList[index]

			combo.clear()
			combo.addItem('')
			for info in attrib.comboList:
				if(info.connect == parent):
					combo.addItem(units._fromUtf8(info.key))
			combo.setCurrentIndex(0)

	def loadConfig(self):
		if(os.path.exists(self.configFileName) == False):
			return False

		self.attribList = []
		storyAttr = xml.parse(self.configFileName).getroot()
		for attr in storyAttr.findall('attr'):
			attrib = Attrib()
			attrib.type = attr.attrib['type']
			attrib.key = attr.attrib['key']
			attrib.value = attr.attrib['value']
			if(attrib.type == 'combo'):
				if(attr.attrib.has_key('connect') == True):
					attrib.connect = attr.attrib['connect']
				for combo in attr.findall('combo'):
					comboAttr = Attrib()
					comboAttr.key = combo.attrib['key']
					comboAttr.value = combo.attrib['value']
					if(combo.attrib.has_key('connect') == True):
						comboAttr.connect = combo.attrib['connect']
					attrib.comboList.append(comboAttr)
			self.attribList.append(attrib)
		return True

	def parseConfig(self, attrList):
		row = 0
		for attrib in attrList:
			if(attrib.type == 'combo' and len(attrib.connect) > 0):
				connectRow = 0
				for connectAttrib in attrList:
					if(connectAttrib.key == attrib.connect and connectAttrib.type == 'combo'):
						connectAttrib.connectList.append(row)
						attrib.connectRow = connectRow
						break
					connectRow = connectRow + 1
			row = row + 1