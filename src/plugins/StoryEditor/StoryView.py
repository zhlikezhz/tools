# -*- coding: utf-8 -*-
import os
import sys
import copy
import units
import StoryData
from PyQt4 import QtGui, QtCore

class StoryItem():
	def __init__(self, data = StoryData.UnitData('default')):
		self.children = []
		self.unitData = data

	def getType(self):
		return self.unitData.name

	def clone(self):
		return copy.deepcopy(self)

	def rowCount(self):
		return len(self.children)

	def columnCount(self):
		return 1

	def appendRow(self, item):
		self.children.append(item)
		self.unitData.children.append(item.unitData)
		item.setParent(self)

	def insertRow(self, row, item):
		count = self.rowCount()
		if(row < 0): 
			row = 0

		if(row > count):
			row = count

		self.children.insert(row, item)
		self.unitData.children.insert(row, item.unitData)
		item.setParent(self)

	def removeRow(self, row):
		count = self.rowCount()
		if(0 <= row and row < count):
			self.children.pop(row)
			self.unitData.children.pop(row)

	def data(self, column):
		if(column == 0):
			return units._fromUtf8(self.unitData.desc)
		return None

	def setData(self, column, value):
		if(column == 0):
			self.unitData.desc = units._toUtf8(value.toString())

	def getParent(self):
		return self.parent

	def setParent(self, parent):
		self.parent = parent

	def child(self, row):
		count = self.rowCount()
		if(0 <= row and row < count):
			return self.children[row]
		return None

	def rowChild(self, child):
		row = 0
		for unit in self.children:
			if(unit == child):
				return row
			row = row + 1

	def calculateWords(self):
		totalWords = 0
		if(self.getType() == "story"):
			def calculate(parent):
				wordCnt = 0
				for element in parent.children:
					wordCnt += len(element.sentence)
					wordCnt += calculate(element)
				return wordCnt
			totalWords = calculate(self.unitData)
		else:
			for child in self.children:
				totalWords += child.calculateWords()
		return totalWords

class StoryModel(QtCore.QAbstractItemModel):
	def __init__(self, itemRoot, parent = None):
		self.itemRoot = itemRoot
		self.copyIndex = QtCore.QModelIndex()
		super(StoryModel, self).__init__(parent)

	def getItem(self, index):
		if(index.isValid()):
			return index.internalPointer()
		return self.itemRoot

	# 通过父节点得到子节点，没有父节点为QtCore.QModelIndex
	def index(self, row, column, parent = QtCore.QModelIndex()):
		if (parent.isValid()):
			parentItem = parent.internalPointer()
			item = parentItem.child(row)
			return self.createIndex(row, column, item) 
		return self.createIndex(row, column, self.itemRoot.child(row))

	# 得到父节点
	def parent(self, index):
		if(index.isValid()):
			item = index.internalPointer()
			parent = item.getParent()
			if(parent == self.itemRoot):
				return QtCore.QModelIndex()
			else:
				pparent = parent.getParent()
				if(pparent == self.itemRoot):
					row = self.itemRoot.rowChild(parent)
					return self.createIndex(row, 0, parent)
				else:
					row = pparent.rowChild(parent)
					return self.createIndex(row, 0, parent)
		return QtCore.QModelIndex()

	#行数，每个节点的子节点的个数
	def rowCount(self, parent = QtCore.QModelIndex()):
		if(parent.isValid()):
			return parent.internalPointer().rowCount()
		return self.itemRoot.rowCount()

	#列数
	def columnCount(self, parent = QtCore.QModelIndex()):
		return self.itemRoot.columnCount()

	#得到数据，根据role的不同得到不同的数据
	def data(self, index, role = QtCore.Qt.DisplayRole):
		if not (index.isValid()):
			return None

		item = index.internalPointer()
		if (role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole):
			return item.data(index.column())
		return None

###########setion+1为列，每列的标题名##########
	def headerData(self, setion, orientation, role = QtCore.Qt.DisplayRole):
		if(role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal):
			if(setion == 0):
				return units._fromUtf8("类型")
		return None

	def flags(self, index):
		if(index.isValid()):
			return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable
		return super(StoryModel, self).flags(index)

##########改变值##########
	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if (role == QtCore.Qt.EditRole):
			item = index.internalPointer()
			item.setData(index.column(), value)
			self.dataChanged.emit(index, index)
			return True
		return False


##########拖动##########
	def mimeData(self, index):
		self.drapIndex = index[0]
		mimeData = QtCore.QMimeData()
		mimeData.setData('text/xml', 'story')
		return mimeData

	def dropMimeData(self, data, action, row, column, parent):
		if(action == QtCore.Qt.IgnoreAction):
			return True

		if not (data.hasFormat("text/xml")):
			return False

		if not (data.data('text/xml') == 'story'):
			return False

		if(column > 0):
			return False

		if(parent.isValid() and row == -1):
			dropParent = self.parent(parent)
			dropRow = parent.row() + 1
			self.moveRow(self.drapIndex, dropRow, dropParent)

		return True

	def mimeTypes(self):
		return ['text/xml']

	def supportedDropActions(self): 
		return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction   

	def supportedDrapActions(self): 
		return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction   

	def moveRow(self, drapIndex, row, dropIndexParent):
		drapIndexParent = self.parent(drapIndex)
		if not ((drapIndexParent.isValid() and dropIndexParent.isValid()) 
			or drapIndexParent == dropIndexParent):
			return False

		drapItem = drapIndex.internalPointer()
		dropItem = drapItem.clone()

		if(dropIndexParent.isValid()):
			self.beginInsertRows(dropIndexParent, row, row)
			dropItemParent = dropIndexParent.internalPointer()
			dropItemParent.insertRow(row, dropItem)
			self.endInsertRows()
		else:
			self.beginInsertRows(QtCore.QModelIndex(), row, row)
			self.itemRoot.insertRow(row, dropItem)
			self.endInsertRows()

		if(dropIndexParent.isValid()):
			drapItemParent = drapIndexParent.internalPointer()
			row = drapItemParent.rowChild(drapItem)
			self.beginRemoveRows(drapIndexParent, row, row)
			drapItemParent.removeRow(row)
			self.endRemoveRows()
		else:
			row = self.itemRoot.rowChild(drapItem)
			self.beginRemoveRows(QtCore.QModelIndex(), row, row)
			self.itemRoot.removeRow(row)
			self.endRemoveRows()

		return True

	def insertRow(self, row, parent = QtCore.QModelIndex()):
		item = self.getItem(parent)
		size = item.rowCount()

		if(row < 0 or size < row):
			return False

		if(item == self.itemRoot):
			data = StoryData.UnitData('card')
			data.desc = 'new card'
		elif(item.unitData.name == "card"):
			data = StoryData.UnitData('story')
			data.desc = 'new story'

			element = StoryData.UnitData('element')
			element.type = 'dialog'
			element.sentence = 'not data'
			data.children.append(element)
		else:
			return False

		self.beginInsertRows(parent, row, row)
		item.insertRow(row, StoryItem(data))
		self.endInsertRows()
		return True

	def removeRow(self, row, parent = QtCore.QModelIndex()):
		item = self.getItem(parent)
		size = item.rowCount()

		if(row < 0 or size < row):
			return False

		self.beginRemoveRows(parent, row, row)
		item.removeRow(row)
		self.endRemoveRows()
		return True

	def copyRow(self, index):
		self.copyIndex = index

	def pasteRow(self, pasteIndex):
		if not (self.copyIndex.isValid() and pasteIndex.isValid()):
			return False

		copyIndex = self.copyIndex
		copyIndexParent = self.parent(copyIndex)
		pasteIndexParent = self.parent(pasteIndex)
		if not ((copyIndexParent.isValid() and pasteIndexParent.isValid()) 
			or copyIndexParent == pasteIndexParent):
			return False

		row = pasteIndex.row() + 1
		copyItem = copyIndex.internalPointer()
		pasteItem = copyItem.clone()

		if(pasteIndexParent.isValid()):
			self.beginInsertRows(pasteIndexParent, row, row)
			pasteItemParent = pasteIndexParent.internalPointer()
			pasteItemParent.insertRow(row, pasteItem)
			self.endInsertRows()
		else:
			self.beginInsertRows(QtCore.QModelIndex(), row, row)
			self.itemRoot.insertRow(row, pasteItem)
			self.endInsertRows()

		self.copyIndex = QtCore.QModelIndex()

	def calculateWords(self, index):
		item = self.getItem(index)
		return item.calculateWords()

	def calculateTotalWords(self):
		return self.itemRoot.calculateWords()

class StoryView(QtGui.QTreeView):
	def __init__(self, parent = None):
		super(StoryView, self).__init__(parent)
		self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		# self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.model = None

	def setData(self, unitData):

		itemRoot = StoryItem(unitData)
		for card in unitData.children:
			cardItem = StoryItem(card)
			itemRoot.children.append(cardItem)
			cardItem.setParent(itemRoot)
			for story in card.children:
				storyItem = StoryItem(story)
				cardItem.children.append(storyItem)
				storyItem.setParent(cardItem)

		self.model = StoryModel(itemRoot)
		self.setModel(self.model)

	def getData(self):
		storyData = []
		for cardItem in self.model.itemRoot.children:
			cardData = StoryData.UnitData('card')
			cardData.desc = cardItem.unitData.desc
			for storyItem in cardItem.children:
				storyData = StoryData.UnitData('story')
				storyData.desc = storyItem.unitData.desc
				storyData.children.append(storyItem.unitData)
		return storyData

	def setView(self, view):
		self.delegateView = view

	def addItem(self):
		if(self.hasFocus()):
			index = self.selectionModel().currentIndex()
			parent = self.model.parent(index)
			self.model.insertRow(index.row() + 1, parent)

	def deleteItem(self):
		if(self.hasFocus()):
			ret = QtGui.QMessageBox.warning(self, units._fromUtf8('删除'),
											units._fromUtf8('是否删除？'),
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			if(ret == QtGui.QMessageBox.Yes):
				index = self.selectionModel().currentIndex()
				parent = self.model.parent(index)
				self.model.removeRow(index.row(), parent)

	def appendItem(self):
		if(self.hasFocus()):
			index = self.selectionModel().currentIndex()
			self.model.insertRow(self.model.rowCount(index), index)

	def clickRowLeft(self):
		if (self.model == None or self.selectionModel() == None):
			return False

		if(self.hasFocus()):
			index = self.selectionModel().currentIndex()
			item = self.model.getItem(index)
			if(item.getType() == "card"):
				self.delegateView.setChapterData(StoryData.UnitData())
				self.delegateView.setAttributeData(StoryData.UnitData())
			elif(item.getType() == 'story'):
				self.delegateView.setChapterData(item.unitData)
				self.delegateView.setAttributeData(StoryData.UnitData())
			self.calculateWords()

	def clickRowRight(self):
		if (self.model == None or self.selectionModel() == None):
			return False

		index = self.selectionModel().currentIndex()
		item = self.model.getItem(index)

		menu = QtGui.QMenu()
		if(item.getType() == 'card'):
			menu.addAction(units._fromUtf8("新建"), self.addItem)
			menu.addAction(units._fromUtf8("删除"), self.deleteItem)
			menu.addAction(units._fromUtf8("新建子节点"), self.appendItem)
		elif(item.getType() == 'story'):
			menu.addAction(units._fromUtf8("新建"), self.addItem)
			menu.addAction(units._fromUtf8("删除"), self.deleteItem)
		menu.exec_(QtGui.QCursor.pos())

	def mousePressEvent(self, evt):
		super(StoryView, self).mousePressEvent(evt)
		if(evt.button() == QtCore.Qt.RightButton):
			self.clickRowRight()
		elif(evt.button() == QtCore.Qt.LeftButton):
			self.clickRowLeft()

	def calculateWords(self):
		index = self.selectionModel().currentIndex()
		wordCnt = self.model.calculateWords(index)
		self.delegateView.setWords(wordCnt)

	def calculateTotalWords(self):
		return self.model.calculateTotalWords()

	def copy(self):
		if (self.model == None or self.selectionModel() == None):
			return False

		if (self.hasFocus()):
			index = self.selectionModel().currentIndex()
			self.model.copyRow(index)

	def paste(self):
		if (self.model == None or self.selectionModel() == None):
			return False

		if (self.hasFocus()):
			index = self.selectionModel().currentIndex()
			self.model.pasteRow(index)

	def repeal(self):
		pass


