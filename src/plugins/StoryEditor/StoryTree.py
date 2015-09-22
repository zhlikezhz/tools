# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import StoryData, StoryItem

class StoryModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent = None):
        super(StoryModel, self).__init__(parent)

        self.rootItem = StoryItem('剧情')
        self.setModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

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

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()
        
        return success

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def setModelData(self, data, parent):
        for item in data:
            item.parentItem = parent
            parent.appendChild(item)



class StoryView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(StoryView, self).__init__(parent)
        story = StoryData()
        self.model = StoryModel(story.getStoryData())
        super(StoryView, self).setModel(self.model)

    def menuRequested(self):
        item = self.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()
            menu = QtGui.QMenu()
            menu.addAction(units._fromUtf8('新建'), self.insertChapter)
            menu.addAction(units._fromUtf8('编辑'), self.editChapter)
            menu.addAction(units._fromUtf8('删除'), self.deleteChapter)
            menu.addAction(units._fromUtf8('剪切'), self.cutChapter)
            menu.addAction(units._fromUtf8('复制'), self.copyChapter)
            menu.addAction(units._fromUtf8('粘贴'), self.pasteChapter)
            menu.exec_(QtGui.QCursor.pos())

    def insertChapter(self):
        index = self.selectionModel().currentIndex()
        if not self.model.insertRow(index.row()+1, index.parent()):
            return

        for column in range(self.model.columnCount(index.parent())):
            child = self.model.index(index.row()+1, column, index.parent())
            self.model.setData(child, "[No data]", QtCore.Qt.EditRole)

    def copyChapter(self):
        print("copy")

    def deleteChapter(self):
        index = self.selectionModel().currentIndex()
        self.model.removeRow(index.row(), index.parent())

    def cutChapter(self):
        print("cut")

    def pasteChapter(self):
        print("paste")

    def clickChapter(self):
    	print('click')

    def editChapter(self):
    	print('edit')

    def mousePressEvent(self, evt):
        super(StoryView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()
        elif(evt.button() == QtCore.Qt.LeftButton):
        	self.clickChapter()

    def mouseDoubleClickEvent(self, evt):
        super(StoryView, self).mouseDoubleClickEvent(evt)
        if(evt.button() == QtCore.Qt.LeftButton):
            self.editChapter()