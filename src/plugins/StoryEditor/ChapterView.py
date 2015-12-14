# -*- coding: utf-8 -*-
import os
import sys
import units
import copy
import StoryData
from PyQt4 import QtGui, QtCore

class ChapterItem():
	def __init__(self, data = StoryData.UnitData('element')):
		self.children = []
		self.unitData = data

	def getType(self):
		return self.unitData.type

	def clone(self):
		return copy.deepcopy(self)

	def rowCount(self):
		return len(self.children)

	def columnCount(self):
		return 2

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
			return units._fromUtf8(units.typeMapping(self.getType()))
		elif(column == 1):
			return units._fromUtf8(self.unitData.sentence)
		return None

	def setData(self, column, value):
		if(column == 0):
			value1 = units._toUtf8(value.toString())
			typeList = units.getTypelist()
			for unitType in typeList:
				if(unitType['val'] == value1):
					self.unitData.type = unitType['key']
		elif(column == 1):
			self.unitData.sentence = units._toUtf8(value.toString())

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

class ChapterModel(QtCore.QAbstractItemModel):
	def __init__(self, itemRoot, parent = None):
		self.itemRoot = itemRoot
		self.copyIndex = QtCore.QModelIndex()
		super(ChapterModel, self).__init__(parent)

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
			elif(setion == 1):
				return units._fromUtf8("语句")
		return None

	def flags(self, index):
		if(index.isValid()):
			return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
		return super(ChapterModel, self).flags(index)

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
		mimeData.setData('text/xml', 'chapter')
		return mimeData

	def dropMimeData(self, data, action, row, column, parent):
		if(action == QtCore.Qt.IgnoreAction):
			return True

		if not (data.hasFormat("text/xml")):
			return False

		if not (data.data('text/xml') == 'chapter'):
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

		data = StoryData.UnitData('element')
		data.sentence = "not data"
		data.type = "dialog"

		self.beginInsertRows(parent, row, row)
		item.insertRow(row, ChapterItem(data))
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


class ChapterView(QtGui.QTreeView):
	def __init__(self, parent = None):
		super(ChapterView, self).__init__(parent)
		self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.index = None
		self.model = None
		self.multiChoose = False

	def updateSelection(self, selected, deselected):
		selectionModel = self.selectionModel()
		indexes = selectionModel.selectedIndexes()
		number = len(indexes) / 2

		if(number > 1):
			self.multiChoose = True
			self.delegateView.setAttributeData(StoryData.UnitData())
		else:
			self.multiChoose = False

	def setView(self, view):
		self.delegateView = view

	def setData(self, unitData):
		itemRoot = ChapterItem(unitData)
		def addTree(parent, parentItem):
			for element in parent.children:
				item = ChapterItem(element)
				parentItem.children.append(item)
				item.setParent(parentItem)
				addTree(element, item)
		addTree(unitData, itemRoot)

		self.model = ChapterModel(itemRoot)
		self.setModel(self.model)

		QtCore.QObject.connect(self.selectionModel(), QtCore.SIGNAL(units._fromUtf8("selectionChanged(QItemSelection, QItemSelection)")), self.updateSelection)

	def setAttbribute(self, unitData):
		if(self.multiChoose == False):
			if(self.index != None and self.index.isValid()):
				currIndex = self.selectionModel().currentIndex()
				if(self.index.internalPointer() == currIndex.internalPointer()):
					parentIndex = self.model.parent(currIndex)
					index = self.model.index(currIndex.row(), 0, parentIndex)
					self.model.setData(index, QtCore.QVariant(units._fromUtf8(unitData.type)))

					index = self.model.index(currIndex.row(), 1, parentIndex)
					self.model.setData(index, QtCore.QVariant(units._fromUtf8(unitData.sentence)))

					item = index.internalPointer()
					item.unitData.attrib = copy.deepcopy(unitData.attrib)
		else:
			selectionModel = self.selectionModel()
			indexes = selectionModel.selectedIndexes()
			number = len(indexes)

			indexRowList = []
			for index in indexes:
				row = index.row()
				if not (row in indexRowList):
					indexRowList.append(row)
					item = index.internalPointer()
					for (key, value) in unitData.attrib.iteritems():
						item.unitData.attrib[key] = value
					item.unitData.attrib = self.delegateView.cleanAttribute(item.unitData.attrib)

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
		if (self.model == None or self.selectionModel() == None or self.multiChoose == True):
			return False

		index = self.selectionModel().currentIndex()
		if(index.isValid()):
			self.index = index
			item = self.model.getItem(index)
			self.delegateView.setAttributeData(item.unitData)

	def clickRowRight(self):
		if (self.model == None or self.selectionModel() == None):
			return False

		index = self.selectionModel().currentIndex()

		if(index.isValid()):
			item = self.model.getItem(index)

			menu = QtGui.QMenu()
			if(item.getType() == 'dialog'):
				menu.addAction(units._fromUtf8("新建"), self.addItem)
				menu.addAction(units._fromUtf8("删除"), self.deleteItem)
			elif(item.getType() == 'choose'):
				menu.addAction(units._fromUtf8("新建"), self.addItem)
				menu.addAction(units._fromUtf8("删除"), self.deleteItem)
				menu.addAction(units._fromUtf8("新建子节点"), self.appendItem)
			elif(item.getType() == 'branch'):
				menu.addAction(units._fromUtf8("新建"), self.addItem)
				menu.addAction(units._fromUtf8("删除"), self.deleteItem)
				menu.addAction(units._fromUtf8("新建子节点"), self.appendItem)
			menu.exec_(QtGui.QCursor.pos())

	def mousePressEvent(self, evt):
		super(ChapterView, self).mousePressEvent(evt)
		if(evt.button() == QtCore.Qt.RightButton):
			self.clickRowRight()
		elif(evt.button() == QtCore.Qt.LeftButton):
			self.clickRowLeft()

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


