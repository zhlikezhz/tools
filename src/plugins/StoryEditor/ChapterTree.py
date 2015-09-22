# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import StoryData, ChapterItem, ChapterModel

class ChapterView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(ChapterView, self).__init__(parent)
        story = StoryData()
        chapter = story.getChapterData('chapter_1')
        self.model = ChapterModel(chapter)
        super(ChapterView, self).setModel(self.model)

    def menuRequested(self):
        item = self.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()
            menu = QtGui.QMenu()
            menu.addAction(units._fromUtf8('新建'), self.newRound)
            menu.addAction(units._fromUtf8('新建分支'), self.insertRound)
            menu.addAction(units._fromUtf8('编辑'), self.editorRound)
            menu.addAction(units._fromUtf8('删除'), self.deleteRound)
            menu.addAction(units._fromUtf8('复制'), self.copyRound)
            menu.addAction(units._fromUtf8('粘贴'), self.pasteRound)
            menu.addAction(units._fromUtf8('剪切'), self.cutRound)
            menu.exec_(QtGui.QCursor.pos())

    def editorRound(self):
        item = self.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()
        print("editor")

    def newRound(self):
        index = self.selectionModel().currentIndex()
        if not self.model.insertRow(index.row()+1, index.parent()):
            return

        for column in range(self.model.columnCount(index.parent())):
            child = self.model.index(index.row()+1, column, index.parent())
            self.model.setData(child, QtCore.QVariant("[No data]"), QtCore.Qt.EditRole)

    def copyRound(self):
        print("copy")

    def deleteRound(self):
        index = self.selectionModel().currentIndex()
        self.model.removeRow(index.row(), index.parent())

    def insertRound(self):
        index = self.selectionModel().currentIndex()

        if self.model.columnCount(index) == 0:
            if not self.model.insertColumn(0, index):
                return

        if not self.model.insertRow(0, index):
            return

        for column in range(self.model.columnCount(index)):
            child = self.model.index(0, column, index)
            self.model.setData(child, QtCore.QVariant("[No data]"), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        QtCore.QVariant("[No header]"), QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(0, 0, index),
                QtGui.QItemSelectionModel.ClearAndSelect)


    def cutRound(self):
        print("cut")

    def pasteRound(self):
        print("paster")

    def mousePressEvent(self, evt):
        super(ChapterView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()

    def mouseDoubleClickEvent(self, evt):
        super(ChapterView, self).mouseDoubleClickEvent(evt)
        if(evt.button() == QtCore.Qt.LeftButton):
            self.editorRound()

