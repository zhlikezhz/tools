# -*- coding: utf-8 -*-
import os
import sys
import units
from PyQt4 import QtGui, QtCore
from StoryData import ChapterItem, ChapterModel

class ChapterView(QtGui.QTreeView):
    def __init__(self, parent = None):
        super(ChapterView, self).__init__(parent)
        # story = StoryData()
        # chapter = story.getChapterData('chapter_1')
        # self.model = ChapterModel(chapter)
        # super(ChapterView, self).setModel(self.model)
    def setData(self, story):
        self.reset()
        self.story = story
        self.model = ChapterModel(story)
        super(ChapterView, self).setModel(self.model)

    def menuRequested(self):
        item = self.currentIndex()
        if item.isValid():
            chapterItem = item.internalPointer()
            menu = QtGui.QMenu()
            menu.addAction(units._fromUtf8('新建'), self.insertRow)
            menu.addAction(units._fromUtf8('新建分支'), self.insertChild)
            menu.addAction(units._fromUtf8('删除'), self.removeRow)
            menu.addAction(units._fromUtf8('编辑'), self.editRow)
            menu.addAction(units._fromUtf8('复制'), self.copyRow)
            menu.addAction(units._fromUtf8('粘贴'), self.pasteRow)
            menu.addAction(units._fromUtf8('剪切'), self.cutRow)
            menu.exec_(QtGui.QCursor.pos())

    def copyRow(self):
        print("copy")

    def cutRow(self):
        print("cut")

    def pasteRow(self):
        print('paste')

    def editRow(self):
        from StoryAttrEdit import StoryAttrEdit

        index = self.selectionModel().currentIndex()
        item = self.model.getItem(index)

        edit = StoryAttrEdit(self)
        edit.setData(item)
        edit.exec_()

    def setAttr(self, data):
        print("chapter getAttr")
        index = self.selectionModel().currentIndex()
        parent = index.parent()
        row = index.row()
        child = self.model.index(row, 0, parent)
        self.model.setData(child, QtCore.QVariant(data['type']), QtCore.Qt.EditRole)
        child = self.model.index(row, 1, parent)
        self.model.setData(child, QtCore.QVariant(data['sentence']), QtCore.Qt.EditRole)

    def mousePressEvent(self, evt):
        super(ChapterView, self).mousePressEvent(evt)
        if(evt.button() == QtCore.Qt.RightButton):
            self.menuRequested()

    def insertChild(self):
        index = self.selectionModel().currentIndex()
        item = index.internalPointer()
        row = item.childCount()

        if not self.model.insertRow(row, index):
            return

        for column in range(self.model.columnCount(index)):
            child = self.model.index(row, column, index)
            self.model.setData(child, QtCore.QVariant("[No data]"), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, index),
                QtGui.QItemSelectionModel.ClearAndSelect)
        self.updateActions()

        self.editRow()

    def insertRow(self):
        print("chapter insert row")
        index = self.selectionModel().currentIndex()

        row = index.row() + 1
        if not self.model.insertRow(row, index.parent()):
            return

        self.updateActions()

        for column in range(self.model.columnCount(index.parent())):
            child = self.model.index(row, column, index.parent())
            self.model.setData(child, QtCore.QVariant("[No data]"), QtCore.Qt.EditRole)
            if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
                self.model.setHeaderData(column, QtCore.Qt.Horizontal,
                        "[No header]", QtCore.Qt.EditRole)

        self.selectionModel().setCurrentIndex(self.model.index(row, 0, index.parent()),
                QtGui.QItemSelectionModel.ClearAndSelect)
        self.editRow()

    def removeRow(self):
        index = self.selectionModel().currentIndex()

        if (self.model.removeRow(index.row(), index.parent())):
            self.updateActions()

    def updateActions(self):
        if self.selectionModel().currentIndex().isValid():
            self.closePersistentEditor(self.selectionModel().currentIndex())

    # def appendRow(self):
    #     print('appendRow')
    #     item = self.rootItem
    #     index = self.model.createIndex(item.childNumber(), 0, item)
    #     row = item.childCount()

    #     if not self.model.insertRow(row, index):
    #         return

    #     val = 'card'
    #     if(item.itemData['type'] == 'card'):
    #         val = 'story'

    #     for column in range(self.model.columnCount(index)):
    #         child = self.model.index(row, 0, index)
    #         self.model.setData(child, QtCore.QVariant(('%s_%d') % (val, row)), QtCore.Qt.EditRole)
    #         print(('%s_%d') % (val, row))
    #         if self.model.headerData(column, QtCore.Qt.Horizontal) is None:
    #             self.model.setHeaderData(column, QtCore.Qt.Horizontal,
    #                     "[No header]", QtCore.Qt.EditRole)

    #     self.selectionModel().setCurrentIndex(self.model.index(row, 0, index),
    #             QtGui.QItemSelectionModel.ClearAndSelect)
    #     self.updateActions()
    #     self.clickRow()