# -*- coding: utf-8 -*-

import res.res
from PyQt4 import QtCore, QtGui
from StoryTree import StoryView
from ChapterTree import ChapterView

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
        storyWindow.resize(1046, 759)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(storyWindow.sizePolicy().hasHeightForWidth())
        storyWindow.setSizePolicy(sizePolicy)
        storyWindow.setMinimumSize(QtCore.QSize(90, 0))
        self.centralWidget = QtGui.QWidget(storyWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scriptTree = StoryView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptTree.sizePolicy().hasHeightForWidth())
        self.scriptTree.setSizePolicy(sizePolicy)
        self.scriptTree.setObjectName(_fromUtf8("scriptTree"))
        self.horizontalLayout.addWidget(self.scriptTree)
        self.chapterView = ChapterView(self.centralWidget)
        self.chapterView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.chapterView.setObjectName(_fromUtf8("chapterView"))
        self.horizontalLayout.addWidget(self.chapterView)
        storyWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtGui.QToolBar(storyWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        storyWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(storyWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        storyWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(storyWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1046, 23))
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
        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.openAction)
        self.toolBar.addAction(self.saveAction)
        self.menu.addAction(self.newAction)
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.addAction)
        self.menu.addAction(self.deleteAction)
        self.menu.addAction(self.saveLuaAction)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(storyWindow)
        QtCore.QObject.connect(self.newAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.newStory)
        QtCore.QObject.connect(self.openAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.openStory)
        QtCore.QObject.connect(self.saveAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.saveStory)
        QtCore.QObject.connect(self.scriptTree, QtCore.SIGNAL(_fromUtf8("clickStory(int,int)")), storyWindow.clickStory)
        QtCore.QObject.connect(self.addAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.chapterView.addItem)
        QtCore.QObject.connect(self.deleteAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.chapterView.deleteItem)
        QtCore.QObject.connect(self.saveLuaAction, QtCore.SIGNAL(_fromUtf8("triggered()")), storyWindow.saveToLua)
        QtCore.QObject.connect(self.addAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.scriptTree.addItem)
        QtCore.QObject.connect(self.deleteAction, QtCore.SIGNAL(_fromUtf8("triggered()")), self.scriptTree.deleteItem)
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
