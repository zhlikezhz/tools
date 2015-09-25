# -*- coding: utf-8 -*-
import os
import sys
import time
import units
from PyQt4 import QtGui, QtCore

class TreeItem(object):
    def __init__(self):
        pass

    def setParent(self, parent):
        self.parentItem = parent

    def getParent(self):
        return self.parentItem

    def child(self, row):
        if(row >= len(self.childItems)):
            return None
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def row(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def appendChild(self, child):
        self.childItems.append(child)

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True

class ChapterItem(TreeItem):
    def __init__(self, itemData, children, parent = None):
        super(ChapterItem, self).__init__()
        self.parentItem = parent
        self.itemData = itemData
        self.childItems = children

    def data(self, column):
        val = None
        if(column == 0):
            val = QtCore.QString.fromUtf8(units.typeMapping(self.itemData['type']))
        elif(column == 1):
            val = QtCore.QString.fromUtf8(self.itemData['sentence'])
        return val 

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        if(column == 0):
            self.itemData['type'] = unicode(value.toString().toUtf8(), 'utf-8', 'ignore')
        elif(column == 1):
            self.itemData['sentence'] = unicode(value.toString().toUtf8(), 'utf-8', 'ignore')

        return True

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = {'type': 'dialog', 'sentence': 'No data'}
            item = ChapterItem(data, [], self)
            self.childItems.insert(position, item)

        return True

    def columnCount(self):
        return 2

class StoryItem(TreeItem):

    def __init__(self, itemData, children, parent = None):
        super(StoryItem, self).__init__()
        self.parentItem = parent
        self.itemData = itemData
        self.childItems = children
        self.storyData = []

    def data(self, column):
        val = None
        if(column == 0):
            val = QtCore.QString.fromUtf8(self.itemData['desc'])
        return val

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        if(column == 0):
            desc = unicode(value.toString().toUtf8(), 'utf-8', 'ignore')
            self.itemData['desc'] = desc
            if(desc[0] == 'c'):
                print('card')
                print(desc)
                self.itemData['type'] = 'card'
            elif(desc[0] == 's'):
                print('story')
                print(desc)
                self.itemData['type'] = 'story'

        return True

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            string = ('%d') % time.time()
            data = {'type': string, 'desc': string}
            item = StoryItem(data, [], self)
            self.childItems.insert(position, item)

        return True

    def columnCount(self):
        return 1

######################################################################################################################



class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, rootItem, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = rootItem
        # self.rootItem = []
        # self.setModelData(data, self.rootItem)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

class ChapterModel(TreeModel):
    def __init__(self, rootItem, parent=None):
        super(ChapterModel, self).__init__(rootItem, parent)

    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

class StoryModel(TreeModel):
    def __init__(self, rootItem, parent=None):
        super(StoryModel, self).__init__(rootItem, parent)


######################################################################################################################