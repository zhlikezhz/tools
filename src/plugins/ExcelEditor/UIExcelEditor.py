# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\codes\qt\pyqt\test1\ExcelCheckWin.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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



class Ui_excelCheckWin(object):
    def setupUi(self, excelCheckWin):
        excelCheckWin.setObjectName(_fromUtf8("excelCheckWin"))
        excelCheckWin.setWindowModality(QtCore.Qt.WindowModal)
        excelCheckWin.resize(989, 767)
        self.centralWidget = QtGui.QWidget(excelCheckWin)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listView = QtGui.QListView(self.centralWidget)
        self.listView.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.horizontalLayout_2.addWidget(self.listView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textBrowser = QtGui.QTextBrowser(self.centralWidget)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.horizontalLayout.addWidget(self.textBrowser)
        self.textBrowser_2 = QtGui.QTextBrowser(self.centralWidget)
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.horizontalLayout.addWidget(self.textBrowser_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtGui.QTableView(self.centralWidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        excelCheckWin.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(excelCheckWin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 989, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuDakai = QtGui.QMenu(self.menuBar)
        self.menuDakai.setObjectName(_fromUtf8("menuDakai"))
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName(_fromUtf8("menu"))
        excelCheckWin.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(excelCheckWin)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        excelCheckWin.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(excelCheckWin)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        excelCheckWin.setStatusBar(self.statusBar)
        self.action_2 = QtGui.QAction(excelCheckWin)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action_3 = QtGui.QAction(excelCheckWin)
        self.action_3.setObjectName(_fromUtf8("action_3"))
        self.action_4 = QtGui.QAction(excelCheckWin)
        self.action_4.setObjectName(_fromUtf8("action_4"))
        self.action = QtGui.QAction(excelCheckWin)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_5 = QtGui.QAction(excelCheckWin)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_6 = QtGui.QAction(excelCheckWin)
        self.action_6.setObjectName(_fromUtf8("action_6"))
        self.action_7 = QtGui.QAction(excelCheckWin)
        self.action_7.setObjectName(_fromUtf8("action_7"))
        self.menuDakai.addAction(self.action_3)
        self.menuDakai.addAction(self.action_2)
        self.menuDakai.addAction(self.action_4)
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_5)
        self.menu.addAction(self.action_6)
        self.menu.addAction(self.action_7)
        self.menuBar.addAction(self.menuDakai.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.toolBar.addAction(self.action_3)
        self.toolBar.addAction(self.action_2)

        self.retranslateUi(excelCheckWin)
        QtCore.QObject.connect(self.action, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.addRule)
        QtCore.QObject.connect(self.action_5, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.deleteRule)
        QtCore.QObject.connect(self.action_6, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.runRule)
        QtCore.QObject.connect(self.action_7, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.runRules)
        QtCore.QObject.connect(self.action_2, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.saveRules)
        QtCore.QObject.connect(self.action_3, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.openRules)
        QtCore.QObject.connect(self.action_4, QtCore.SIGNAL(_fromUtf8("triggered()")), excelCheckWin.openFolder)
        QtCore.QMetaObject.connectSlotsByName(excelCheckWin)

    def retranslateUi(self, excelCheckWin):
        excelCheckWin.setWindowTitle(_translate("excelCheckWin", "检查编辑器", None))
        self.menuDakai.setTitle(_translate("excelCheckWin", "文件", None))
        self.menu.setTitle(_translate("excelCheckWin", "工具", None))
        self.toolBar.setWindowTitle(_translate("excelCheckWin", "toolBar", None))
        self.action_2.setText(_translate("excelCheckWin", "保存规则", None))
        self.action_2.setShortcut(_translate("excelCheckWin", "Ctrl+S", None))
        self.action_3.setText(_translate("excelCheckWin", "打开规则", None))
        self.action_3.setShortcut(_translate("excelCheckWin", "Ctrl+O", None))
        self.action_4.setText(_translate("excelCheckWin", "导入文件夹", None))
        self.action.setText(_translate("excelCheckWin", "插入规则", None))
        self.action.setShortcut(_translate("excelCheckWin", "Ctrl+N", None))
        self.action_5.setText(_translate("excelCheckWin", "删除规则", None))
        self.action_5.setShortcut(_translate("excelCheckWin", "Del", None))
        self.action_6.setText(_translate("excelCheckWin", "运行规则", None))
        self.action_6.setShortcut(_translate("excelCheckWin", "F6", None))
        self.action_7.setText(_translate("excelCheckWin", "运行所有规则", None))
        self.action_7.setShortcut(_translate("excelCheckWin", "F5", None))
