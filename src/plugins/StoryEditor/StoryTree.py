# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import StoryData, StoryItem, StoryModel

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