# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import StoryItem, StoryModel

class StoryView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(StoryView, self).__init__(parent)
        self.clickStory = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
        # self.story = StoryData()
        # self.model = StoryModel(self.story.getStoryData())
        # super(StoryView, self).setModel(self.model)

    def setData(self, story):
        self.reset()
        self.rootItem = story
        self.model = StoryModel(story)
        super(StoryView, self).setModel(self.model)

    def menuRequested(self):
        item = self.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()
            menu = QtGui.QMenu()
            # menu.addAction(units._fromUtf8('新建卡牌'), self.insertRow)
            menu.addAction(units._fromUtf8('新建剧情'), self.insertChild)
            menu.addAction(units._fromUtf8('删除'), self.removeRow)
            menu.addAction(units._fromUtf8('剪切'), self.cutRow)
            menu.addAction(units._fromUtf8('复制'), self.copyRow)
            menu.addAction(units._fromUtf8('粘贴'), self.pasteRow)
            menu.exec_(QtGui.QCursor.pos())

    def copyRow(self):
        print("copy")

    def cutRow(self):
        print("cut")

    def pasteRow(self):
        print("paste")

    def clickRow(self):
        item = self.currentIndex()
        if(item == None):
            return 

        childItem = item.internalPointer()
        if(childItem == None):
            return

        fatherItem = childItem.getParent()
        if(fatherItem == None or fatherItem == self.rootItem):
            return

        self.emit(QtCore.SIGNAL("clickStory(QString,QString)") , fatherItem.itemData, childItem.itemData)

    def mousePressEvent(self, evt):
        super(StoryView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()
        elif(evt.button() == QtCore.Qt.LeftButton):
        	self.clickRow()

    # def mouseDoubleClickEvent(self, evt):
    #     super(StoryView, self).mouseDoubleClickEvent(evt)
    #     if(evt.button() == QtCore.Qt.LeftButton):
    #         self.editChapter()

    def insertRow(self):
        index = self.selectionModel().currentIndex()

        if not self.model.insertRow(index.row()+1, index.parent()):
            return

        self.updateActions()

        for column in range(self.model.columnCount(index.parent())):
            child = self.model.index(index.row()+1, column, index.parent())
            self.model.setData(child, "[No data]", QtCore.Qt.EditRole)

    def removeRow(self):
        index = self.selectionModel().currentIndex()

        if (self.model.removeRow(index.row(), index.parent())):
            self.updateActions()

    def updateActions(self):
        if self.selectionModel().currentIndex().isValid():
            self.closePersistentEditor(self.selectionModel().currentIndex())

    def insertChild(self):
        index = self.selectionModel().currentIndex()

        if self.model.columnCount(index) == 0:
            if not self.model.insertColumn(0, index):
                return

        if not self.model.insertRow(0, index):
            return

        for column in range(self.model.columnCount(index)):
            child = self.model.index(0, column, index)
            self.model.setData(child, "[No data]", QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(0, 0, index),
                QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()
