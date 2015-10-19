# -*- coding: utf-8 -*-
import os
import sys
import units
import res.res
from PyQt4 import QtGui, QtCore
from StoryData import StoryItem, StoryModel, ChapterItem

class StoryView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(StoryView, self).__init__(parent)
        self.clickStory = QtCore.pyqtSignal(int, int)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self.starPos = -10
        self.isDrap = False

    def setData(self, story):
        self.reset()
        self.rootItem = story
        self.model = StoryModel(story, self)
        super(StoryView, self).setModel(self.model)
        self.clickRow()

    def menuRequested(self):
        model = self.selectionModel()
        if(model == None):
            return

        item = model.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()

            menu = QtGui.QMenu()
            if(chapterItem.itemData['type'] == 'card'):
                menu.addAction(units._fromUtf8('插入卡牌'), self.insertRow)
                menu.addAction(units._fromUtf8('加入剧情'), self.insertChild)
                menu.addAction(units._fromUtf8('删除'), self.removeRow)
            elif(chapterItem.itemData['type'] == 'story'):
                menu.addAction(units._fromUtf8('插入剧情'), self.insertRow)
                menu.addAction(units._fromUtf8('删除'), self.removeRow)
            menu.exec_(QtGui.QCursor.pos())

    def copyRow(self):
        print("copy")

    def cutRow(self):
        print("cut")

    def pasteRow(self):
        print("paste")

    def addItem(self):
        if self.hasFocus():
            self.insertRow()

    def deleteItem(self):
        if self.hasFocus():
            self.removeRow()

    def clickRow(self):
        model = self.selectionModel()
        if(model == None):
            return

        childItem = model.currentIndex()
        if(childItem == None):
            return 

        fatherItem = self.model.parent(childItem)
        if(fatherItem == None):
            return

        self.emit(QtCore.SIGNAL("clickStory(int,int)") , fatherItem.row(), childItem.row())

    def mousePressEvent(self, evt):
        super(StoryView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()
        elif(evt.button() == QtCore.Qt.LeftButton):
            self.isDrap = False
            self.startPos = evt.pos()
        	# self.clickRow()

    def mouseMoveEvent(self, evt):
        super(StoryView, self).mouseMoveEvent(evt)
        if(evt.buttons() & QtCore.Qt.LeftButton):
            distance = (evt.pos() - self.startPos).manhattanLength()
            if(distance >= QtGui.QApplication.startDragDistance()):
                if(self.isDrap == False):
                    self.drapStory()
                self.isDrap == True

    def mouseReleaseEvent(self, evt):
        super(StoryView, self).mouseReleaseEvent(evt)
        if(self.isDrap == False and evt.button() == QtCore.Qt.LeftButton):
            self.clickRow()

    def drapStory(self):
        item = self.currentIndex()
        if(item):
            mimeData = QtCore.QMimeData()
            mimeData.setText('1')

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            self.model.setSupportedDragActions(QtCore.Qt.MoveAction)
            if(drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction):
                pass

    def dragEnterEvent(self, evt):
        if(evt.source() and evt.source() == self):
            evt.setDropAction(QtCore.Qt.MoveAction)
            evt.accept()

    def dragMoveEvent(self, evt):
        if(evt.source() and evt.source() == self):
            currIndex = self.indexAt(evt.pos())
            dragIndex = self.selectionModel().currentIndex()
            if(currIndex and dragIndex and currIndex != dragIndex):
                currItem = currIndex.internalPointer()
                dragItem = dragIndex.internalPointer()
                currType = currItem.itemData['type']
                dragType = dragItem.itemData['type']

                if(currType == dragType and currIndex.parent() == dragIndex.parent()):
                    evt.setDropAction(QtCore.Qt.MoveAction)
                    evt.accept()
                else:
                    evt.ignore()
            else:
                evt.ignore()

    def dropEvent(self, evt):
        if(evt.source() and evt.source() == self):
            evt.setDropAction(QtCore.Qt.MoveAction)
            evt.accept()

            currIndex = self.indexAt(evt.pos())
            dragIndex = self.selectionModel().currentIndex()

            if(currIndex and dragIndex and currIndex != dragIndex):
                row = currIndex.row() + 1
                currItem = currIndex.internalPointer()
                dragItem = dragIndex.internalPointer()

                currType = currItem.itemData['type']
                dragType = dragItem.itemData['type']

                parentIndex = currIndex.parent()
                parentRow = self.model.rowCount(parentIndex)
                if not self.model.insertRow(row, parentIndex):
                    return

                newItem = self.model.index(row, 0, parentIndex).internalPointer()
                newItem.itemData = dragItem.itemData
                newItem.childItems = dragItem.childItems
                newItem.storyData = dragItem.storyData

                for item in newItem.childItems:
                    item.setParent(newItem)

                self.selectionModel().setCurrentIndex(self.model.index(row, 0, parentIndex), QtGui.QItemSelectionModel.ClearAndSelect)
                self.updateActions()

                if(row <= dragIndex.row()):
                    self.model.removeRow(dragIndex.row() + 1, dragIndex.parent())
                else:
                    self.model.removeRow(dragIndex.row(), dragIndex.parent())

                self.updateActions()


    def insertRow(self):
        print('insertRow')
        index = self.selectionModel().currentIndex()
        row = index.row() + 1
        parentRow = self.model.rowCount(index.parent())
        typeVal = index.internalPointer().itemData['type']

        if not self.model.insertRow(row, index.parent()):
            return

        self.updateActions()

        for column in range(self.model.columnCount(index.parent())):
            child = self.model.index(row, 0, index.parent())
            self.model.setData(child, QtCore.QVariant(('%s_%d') % (typeVal, parentRow)), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, index.parent()),
                QtGui.QItemSelectionModel.ClearAndSelect)

        self.addDialog(typeVal)


    def removeRow(self):
        ret = QtGui.QMessageBox.warning(self, units._fromUtf8('删除'),
                                        units._fromUtf8('是否删除？'),
                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if(ret == QtGui.QMessageBox.Yes):
            index = self.selectionModel().currentIndex()
            if (self.model.removeRow(index.row(), index.parent())):
                self.updateActions()

    def updateActions(self):
        if self.selectionModel().currentIndex().isValid():
            self.closePersistentEditor(self.selectionModel().currentIndex())

    def insertChild(self):
        print('insertChild')
        index = self.selectionModel().currentIndex()
        item = index.internalPointer()
        row = item.childCount()

        if not self.model.insertRow(row, index):
            return

        val = 'card'
        if(item.itemData['type'] == 'card'):
            val = 'story'

        for column in range(self.model.columnCount(index)):
            child = self.model.index(row, 0, index)
            self.model.setData(child, QtCore.QVariant(('%s_%d') % (val, row)), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, index),
                QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()

        self.addDialog(val)

    def appendRow(self):
        print('appendRow')
        item = self.rootItem
        index = self.model.createIndex(item.childNumber(), 0, item)
        row = item.childCount()

        if not self.model.insertRow(row, index):
            return

        val = 'card'
        if(item.itemData['type'] == 'card'):
            val = 'story'

        for column in range(self.model.columnCount(index)):
            child = self.model.index(row, 0, index)
            self.model.setData(child, QtCore.QVariant(('%s_%d') % (val, row)), QtCore.Qt.EditRole)
            print(('%s_%d') % (val, row))
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, index),
                QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()
        self.addDialog(val)

    def addDialog(self, typeVal):
        if(typeVal == 'story'):
            index = self.selectionModel().currentIndex()
            item = index.internalPointer()
            data = {'type': 'dialog', 'sentence': 'No data', 'attr':{}}
            item.storyData.append(ChapterItem(data, [], self))