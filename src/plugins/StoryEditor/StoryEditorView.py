# -*- coding: utf-8 -*-

import res.res
from PyQt4 import QtCore, QtGui
from StoryTree import StoryView
from ChapterTree import ChapterView
from StoryAttrTable import StoryAttrTable

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

class Ui_storyWindow(object):
    def setupUi(self, storyWindow):
        storyWindow.setObjectName(_fromUtf8("storyWindow"))
        storyWindow.resize(1096, 809)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(storyWindow.sizePolicy().hasHeightForWidth())
        storyWindow.setSizePolicy(sizePolicy)
        storyWindow.setMinimumSize(QtCore.QSize(90, 0))
        self.centralWidget = QtGui.QWidget(storyWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.scriptTree = StoryView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptTree.sizePolicy().hasHeightForWidth())
        self.scriptTree.setSizePolicy(sizePolicy)
        self.scriptTree.setDragEnabled(True)
        self.scriptTree.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.scriptTree.setObjectName(_fromUtf8("scriptTree"))
        self.horizontalLayout_2.addWidget(self.scriptTree)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chapterView = ChapterView(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chapterView.sizePolicy().hasHeightForWidth())
        self.chapterView.setSizePolicy(sizePolicy)
        self.chapterView.setMinimumSize(QtCore.QSize(0, 500))
        self.chapterView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.chapterView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.chapterView.setDragEnabled(True)
        self.chapterView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.chapterView.setObjectName(_fromUtf8("chapterView"))
        self.verticalLayout_2.addWidget(self.chapterView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.typeCombo = QtGui.QComboBox(self.centralWidget)
        self.typeCombo.setObjectName(_fromUtf8("typeCombo"))
        self.verticalLayout.addWidget(self.typeCombo)
        self.dialogEdit = QtGui.QTextEdit(self.centralWidget)
        self.dialogEdit.setObjectName(_fromUtf8("dialogEdit"))
        self.verticalLayout.addWidget(self.dialogEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.attrTable = StoryAttrTable(self.centralWidget)
        self.attrTable.setObjectName(_fromUtf8("attrTable"))
        self.attrTable.setColumnCount(0)
        self.attrTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.attrTable)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        storyWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtGui.QToolBar(storyWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        storyWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(storyWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        storyWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(storyWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1096, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName(_fromUtf8("menu"))
        storyWindow.setMenuBar(self.menuBar)
        self.openAction = QtGui.QAction(storyWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/menu/open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openAction.setIcon(icon)
        self.openAction.setObjectName(_fromUtf8("openAction"))
        self.saveAction = QtGui.QAction(storyWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/menu/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveAction.setIcon(icon1)
        self.saveAction.setObjectName(_fromUtf8("saveAction"))
        self.newAction = QtGui.QAction(storyWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/menu/new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newAction.setIcon(icon2)
        self.newAction.setObjectName(_fromUtf8("newAction"))
        self.addAction = QtGui.QAction(storyWindow)
        self.addAction.setObjectName(_fromUtf8("addAction"))
        self.deleteAction = QtGui.QAction(storyWindow)
        self.deleteAction.setObjectName(_fromUtf8("deleteAction"))
        self.saveLuaAction = QtGui.QAction(storyWindow)
        self.saveLuaAction.setObjectName(_fromUtf8("saveLuaAction"))
        self.calWords = QtGui.QAction(storyWindow)
        self.calWords.setObjectName(_fromUtf8("calWords"))
        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.openAction)
        self.toolBar.addAction(self.saveAction)
        self.menu.addAction(self.newAction)
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.addAction)
        self.menu.addAction(self.deleteAction)
        self.menu.addAction(self.saveLuaAction)
        self.menu.addAction(self.calWords)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(storyWindow)
        QtCore.QObject.connect(self.newAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.newStory)
        QtCore.QObject.connect(self.openAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.openStory)
        QtCore.QObject.connect(self.saveAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.saveStory)
        QtCore.QObject.connect(self.scriptTree, QtCore.SIGNAL(_fromUtf8("clickStory(int,int)")), storyWindow.clickStory)
        QtCore.QObject.connect(self.addAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.chapterView.addItem)
        QtCore.QObject.connect(self.saveLuaAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.saveToLua)
        QtCore.QObject.connect(self.addAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.scriptTree.addItem)
        QtCore.QObject.connect(self.deleteAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.scriptTree.deleteItem)
        QtCore.QObject.connect(self.attrTable, QtCore.SIGNAL(_fromUtf8("cellChanged(int,int)")), storyWindow.cellChanged)
        QtCore.QObject.connect(self.typeCombo, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), storyWindow.cellChanged)
        QtCore.QObject.connect(self.dialogEdit, QtCore.SIGNAL(_fromUtf8("textChanged()")), storyWindow.cellChanged)
        QtCore.QObject.connect(self.deleteAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.chapterView.deleteItem)
        QtCore.QObject.connect(self.calWords, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.showWords)
        QtCore.QMetaObject.connectSlotsByName(storyWindow)

    def retranslateUi(self, storyWindow):
        storyWindow.setWindowTitle(_translate("storyWindow", "MainWindow", None))
        self.toolBar.setWindowTitle(_translate("storyWindow", "toolBar", None))
        self.menu.setTitle(_translate("storyWindow", "文件", None))
        self.openAction.setText(_translate("storyWindow", "打开剧本", None))
        self.openAction.setShortcut(_translate("storyWindow", "Ctrl+O", None))
        self.saveAction.setText(_translate("storyWindow", "保存剧本", None))
        self.saveAction.setShortcut(_translate("storyWindow", "Ctrl+S", None))
        self.newAction.setText(_translate("storyWindow", "新建剧本", None))
        self.newAction.setShortcut(_translate("storyWindow", "Ctrl+N", None))
        self.addAction.setText(_translate("storyWindow", "增加", None))
        self.addAction.setShortcut(_translate("storyWindow", "+", None))
        self.deleteAction.setText(_translate("storyWindow", "删除", None))
        self.deleteAction.setShortcut(_translate("storyWindow", "Del", None))
        self.saveLuaAction.setText(_translate("storyWindow", "导出到Lua", None))
        self.saveLuaAction.setShortcut(_translate("storyWindow", "Ctrl+P", None))
        self.calWords.setText(_translate("storyWindow", "计算字数", None))
        self.calWords.setShortcut(_translate("storyWindow", "F5", None))