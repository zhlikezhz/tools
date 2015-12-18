# -*- coding: utf-8 -*-
import os
import sys
import units
import AttributeData
import xml.etree.ElementTree as xml
from PyQt4 import QtGui, QtCore

class MComBoBox(QtGui.QComboBox):
	def __init__(self, parent = None):
		super(MComBoBox, self).__init__(parent)
		QtCore.QObject.connect(self, QtCore.SIGNAL(units._fromUtf8("currentIndexChanged(int)")), self.comboChanged)
		self.callbackList = []

	def setPosition(self, row, col):
		self.row = row
		self.column = col

	def comboChanged(self):
		for func in self.callbackList:
			func(self.row, self.column)

	def connectCallback(self, func):
		if(func):
			self.callbackList.append(func)

class AttributeView(QtGui.QTableWidget):
	def __init__(self, parent = None):
		super(AttributeView, self).__init__(parent)
		self.attributeList = AttributeData.MatchMgr().attributeList
		self.initData()

	def changed(self, row, col):
		string = units._toUtf8(self.cellWidget(row, 0).currentText())
		self.updateData(self.attributeList[row], string)
		self.delegateView.getAttributeData()

	def initData(self, filename = 'config.xml'):
		self.setRowCount(0)
		self.setColumnCount(0)
		size = len(self.attributeList)

		if(size > 0):
			self.setRowCount(size)
			self.setColumnCount(1)

			for attr in self.attributeList:
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(attr.getShowValue()))
				self.setVerticalHeaderItem(attr.row, item)

				if(attr.type == 'combo'):
					comboView = MComBoBox()
					self.setCellWidget(attr.row, 0, comboView)
					comboView.setPosition(attr.row, 0)
					comboView.addItem('')
					for combo in attr.comboList:
						comboView.addItem(units._fromUtf8(combo.getShowValue()))
					comboView.connectCallback(self.changed)
				elif(attr.type == 'text'):
					self.setItem(attr.row, 0, QtGui.QTableWidgetItem())

			cnt = 0
			headValue = ["值"]
			for string in headValue:
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(string))
				self.setHorizontalHeaderItem(cnt, item)
				cnt += 1

			self.resizeRowsToContents()
			self.resizeColumnsToContents()
			self.setCurrentCell(0, 0)

	def setView(self, view):
		self.delegateView = view

	def setData(self, data):

		for attr in self.attributeList:
			if(attr.type == 'combo'):
				comboView = self.cellWidget(attr.row, 0)
				comboView.setCurrentIndex(0)
			elif(attr.type == 'text'):
				textView = self.item(attr.row, 0)
				textView.setText(units._fromUtf8(''))

		tmpStack = []
		updateStack = []
		for (saveKey, saveValue) in data.iteritems():
			item = []
			item.append(saveKey)
			item.append(saveValue)
			for attr in self.attributeList:
				if(attr.getSaveValue() == saveKey):
					item.append(attr.row)
					if(attr.hasParent == True):
						if attr.parentRow in tmpStack:
							index = tmpStack.index(attr.parentRow)
							tmpStack.insert(index, attr.row)
							updateStack.insert(index, item)
						else:
							updateStack.append(item)
							tmpStack.append(attr.row)
					else:
						updateStack.append(item)
						tmpStack.append(attr.row)
					break

		while(len(updateStack) > 0):
			item = updateStack.pop()
			saveKey = item[0]
			saveValue = item[1]
			attr = self.attributeList[item[2]]

			if(attr.type == 'combo'):
				comboView = self.cellWidget(attr.row, 0)
				index = comboView.findText(units._fromUtf8(attr.getChildShowValue(saveValue)))
				if(index == -1):
					index = 0
				comboView.setCurrentIndex(index)
			elif(attr.type == 'text'):
				textView = self.item(attr.row, 0)
				textView.setText(units._fromUtf8(saveValue))

	def getData(self):
		data = {}
		for attr in self.attributeList:
			string = ''
			if(attr.type == 'combo'):
				showValue = units._toUtf8(self.cellWidget(attr.row, 0).currentText())
				if(attr.hasParent == True):
					parentRow = attr.parentRow
					showParentName = units._toUtf8(self.cellWidget(parentRow, 0).currentText())
					string = attr.getChildSaveValue(showValue, showParentName)
				else:
					string = attr.getChildSaveValue(showValue)
			elif(attr.type == 'text'):
				string = units._toUtf8(self.item(attr.row, 0).text())
			if(len(string) > 0):
				data[attr.getSaveValue()] = string

		return data

	def updateData(self, attr, value):
		if(attr.hasChild == False):
			return 

		for child in attr.children:
			if(child.type == 'combo'):
				comboView = self.cellWidget(child.row, 0)
				comboView.clear()
				comboView.addItem('')
				for combo in child.comboList:
					if(combo.parentName == value):
						comboView.addItem(units._fromUtf8(combo.getShowValue()))
				comboView.setCurrentIndex(0)
		self.resizeRowsToContents()
		self.resizeColumnsToContents()