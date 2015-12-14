# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, QtCore

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s
try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)


class StoryModel(QtCore.QAbstractItemModel):
	def __init__(self, parent = None):
		super(StoryModel, self).__init__(parent)
		self.data = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

	# 通过父节点得到子节点，没有父节点为QtCore.QModelIndex
	def index(self, row, column, parent = QtCore.QModelIndex()):
		if not (parent.isValid()):
			return self.createIndex(row, column, 0)
		parent_idx = parent.internalId()
		idx = parent_idx * 2 + (row + 1)
		return self.createIndex(row, column, idx)

	# 得到父节点
	def parent(self, index):
		if (index.internalId() == 0):
			return QtCore.QModelIndex()
		parent_idx = (index.internalId() - 1) / 2
		return self.createIndex((parent_idx + 1) % 2, 0, parent_idx)

	#行数，每个节点的子节点的个数
	def rowCount(self, parent = QtCore.QModelIndex()):
		if not (parent.isValid()):
			return 1
		if(parent.internalId() < 15 / 2):
			return 2
		return 0

	#列数
	def columnCount(self, parent = QtCore.QModelIndex()):
		return 2

	#得到数据，根据role的不同得到不同的数据
	def data(self, index, role = QtCore.Qt.DisplayRole):
		if not (index.isValid()):
			return None

		if (role == QtCore.Qt.DisplayRole):
			value = self.data[index.internalId()]
			return value
		elif (role == QtCore.Qt.EditRole):
			value = self.data[index.internalId()]
			return value
		return None

	# setion+1为列，每列的标题名
	def headerData(self, setion, orientation, role):
		if(role == QtCore.Qt.DisplayRole 
		and orientation == QtCore.Qt.Horizontal):
			if(setion == 0):
				return _fromUtf8("人物")
			elif(setion == 1):
				return _fromUtf8("语句")
		return None

	def flags(self, index):
		if index.isValid(): 
			return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
		return super(StoryModel, self).flags(index)

	def setData(self, index, value, role):
		if(role != QtCore.Qt.EditRole):
			return False

		idx = index.internalId()
		self.data[idx] = value.toString()
		self.dataChanged.emit(index, index)
		return True

	def mimeData(self, index):
		# print(indexes)
		self.drapIndex = index[0]
		# print(index[0].row())
		# print(index[0].column())
		mimeData = QtCore.QMimeData()
		mimeData.setData('text/xml', 'story')
		return mimeData

	def supportedDropActions(self): 
		return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction   

	def dropMimeData(self, data, action, row, column, parent):
		print(QtCore.Qt.IgnoreAction)
		print 'dropMimeData %s %s %s %s %s' % (data.data('text/xml'), action, row, column, parent) 
		if(data.data('text/xml') == "story"): 
			drapIndex = self.drapIndex
			drapParent = self.parent(drapIndex)

			print(row)
			if(row != -1):
				dropRow = row
				dropParent = self.index(dropRow, column, parent)
			elif(parent.isValid()):
				dropRow = self.rowCount(parent) + 1
				dropParent = parent
			else:
				dropRow = self.rowCount(QtCore.QModelIndex())
				dropParent = QtCore.QModelIndex()

			if(drapIndex and dropParent):
				self.insertRow(dropRow, dropParent)
				self.removeRow(drapIndex.row(), drapParent)

		return True

	def mimeTypes(self):
		return ['text/xml']

	def removeRow(self, row, parent = QtCore.QModelIndex()):
		if(parent.isValid()):
			self.beginRemoveRows(parent, row, row)
			parent_idx = parent.internalId()
			idx = parent_idx * 2 + (row + 1) 
			self.data[idx] = 0
			self.endRemoveRows()
		else:
			pass

	def insertRow(self, row, parent = QtCore.QModelIndex()):
		if(parent.isValid()):
			self.beginInsertRows(parent, row, row)
			parent_idx = parent.internalId()
			idx = parent_idx * 2 + (row + 1) 
			print(parent_idx)
			print(row)
			print(idx)
			self.data[idx] = idx
			self.endInsertRows()
		else:
			pass

class StoryView(QtGui.QTreeView):
	def __init__(self, parent = None):
		super(StoryView, self).__init__(parent)

		model = StoryModel()
		self.setModel(model)
		self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

		# headerView = QtGui.QHeaderView(QtCore.Qt.Horizontal)
		# headerView.setModel(model)
		# self.setHeader(headerView)

		# model.setHeaderData(0,  QtCore.Qt.Horizontal, _fromUtf8("类型"))
		#_fromUtf8("人物"), _fromUtf8("语句")])



if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")

	app = QtGui.QApplication(sys.argv)
	view = QtGui.QTreeView()
	view.show()

	sys.exit(app.exec_())

