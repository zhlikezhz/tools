# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import ChapterItem, ChapterModel

class ChapterView(QtGui.QTreeView):
    def __init__(self, parent = None):
        self.model = None
        super(ChapterView, self).__init__(parent)

    def setData(self, story):
        self.reset()
        self.story = story
        self.model = ChapterModel(story)
        super(ChapterView, self).setModel(self.model)

    def menuRequested(self):
        index = self.currentIndex()
        if index.isValid():
            item = index.internalPointer()
            menu = QtGui.QMenu()

            types = item.itemData['type']
            if(types == 'dialog'):
                menu.addAction(units._fromUtf8('增加对话'), self.insertRow)
                menu.addAction(units._fromUtf8('删除'), self.removeRow)
            elif(types == 'choose'):
                menu.addAction(units._fromUtf8('增加对话'), self.insertRow)
                menu.addAction(units._fromUtf8('插入分支'), self.insertChild)
                menu.addAction(units._fromUtf8('删除'), self.removeRow)
            elif(types == 'branch'):
                menu.addAction(units._fromUtf8('增加分支'), self.insertRow)
                menu.addAction(units._fromUtf8('插入对话'), self.insertChild)
                menu.addAction(units._fromUtf8('删除'), self.removeRow)

            menu.exec_(QtGui.QCursor.pos())

    def copyRow(self):
        print("copy")

    def cutRow(self):
        print("cut")

    def pasteRow(self):
        print('paste')

    def addItem(self):
        if self.hasFocus():
            self.insertRow()

    def deleteItem(self):
        if self.hasFocus():
            self.removeRow()


    def editRow(self):
        from StoryAttrEdit import StoryAttrEdit

        index = self.selectionModel().currentIndex()
        # item = self.model.getItem(index)
        item = index.internalPointer()

        edit = StoryAttrEdit(self)
        edit.setData(item)
        edit.exec_()

    def setAttr(self, data):
        print("chapter getAttr")
        index = self.selectionModel().currentIndex()
        item = index.internalPointer()
        parent = index.parent()
        row = index.row()
        child = self.model.index(row, 0, parent)
        self.model.setData(child, QtCore.QVariant(data['type']), QtCore.Qt.EditRole)
        child = self.model.index(row, 1, parent)
        self.model.setData(child, QtCore.QVariant(data['sentence']), QtCore.Qt.EditRole)
        item.itemData['attr'] = data['attr']

    def mousePressEvent(self, evt):
        super(ChapterView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()

    def mouseDoubleClickEvent(self, evt):
        super(ChapterView, self).mouseDoubleClickEvent(evt)
        if(evt.button() == QtCore.Qt.LeftButton):
            self.editRow()

    def insertChild(self):
        if(self.model == None):
            return 

        curIdx = self.selectionModel().currentIndex()
        curItem = self.model.getItem(curIdx)
        row = curItem.childCount()

        if(curItem == self.model.rootItem or
            not self.model.insertRow(row, curIdx)):
            return 

        data = []
        data.append('dialog')
        data.append('No data')
        for column in range(self.model.columnCount(curIdx)):
            child = self.model.index(row, column, curIdx)
            self.model.setData(child, QtCore.QVariant(data[column]), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, curIdx), QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()


    def insertRow(self):
        if(self.model == None):
            return

        curIdx = self.selectionModel().currentIndex()
        curItem = self.model.getItem(curIdx)
        row = curItem.row() + 1
        if(curIdx == self.model.rootItem):
            return

        parentIdx = self.model.parent(curIdx)
        parentItem = self.model.getItem(parentIdx)
        if not self.model.insertRow(row, parentIdx):
            return

        data = []
        data.append(curItem.itemData['type'])
        data.append('No data')
        for column in range(self.model.columnCount(parentIdx)):
            child = self.model.index(row, column, parentIdx)
            self.model.setData(child, QtCore.QVariant(data[column]), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, parentIdx), QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()

    def appendRow(self):
        if(self.model == None):
            return 

        curItem = self.model.rootItem
        curIdx = self.model.createIndex(curItem.childNumber(), 0, curItem)
        row = curItem.childCount()

        if not self.model.insertRow(row, curIdx):
            return 

        data = []
        data.append('dialog')
        data.append('No data')
        for column in range(self.model.columnCount(curIdx)):
            child = self.model.index(row, column, curIdx)
            self.model.setData(child, QtCore.QVariant(data[column]), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, curIdx), QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()

    def removeRow(self):
        index = self.selectionModel().currentIndex()

        if (self.model.removeRow(index.row(), index.parent())):
            self.updateActions()

    def updateActions(self):
        if self.selectionModel().currentIndex().isValid():
            self.closePersistentEditor(self.selectionModel().currentIndex())