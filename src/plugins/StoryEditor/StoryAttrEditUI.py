# -*- coding: utf-8 -*-
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

class Ui_storyAttrEditor(object):
    def setupUi(self, storyAttrEditor):
        storyAttrEditor.setObjectName(_fromUtf8("storyAttrEditor"))
        storyAttrEditor.resize(523, 584)
        storyAttrEditor.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(storyAttrEditor)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.typeCombo = QtGui.QComboBox(storyAttrEditor)
        self.typeCombo.setObjectName(_fromUtf8("typeCombo"))
        self.verticalLayout.addWidget(self.typeCombo)
        self.dialogEdit = QtGui.QTextEdit(storyAttrEditor)
        self.dialogEdit.setObjectName(_fromUtf8("dialogEdit"))
        self.verticalLayout.addWidget(self.dialogEdit)
        self.attrTable = QtGui.QTableWidget(storyAttrEditor)
        self.attrTable.setObjectName(_fromUtf8("attrTable"))
        self.attrTable.setColumnCount(0)
        self.attrTable.setRowCount(0)
        self.verticalLayout.addWidget(self.attrTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveBtn = QtGui.QPushButton(storyAttrEditor)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.calBtn = QtGui.QPushButton(storyAttrEditor)
        self.calBtn.setObjectName(_fromUtf8("calBtn"))
        self.horizontalLayout.addWidget(self.calBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(storyAttrEditor)
        QtCore.QObject.connect(self.saveBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), storyAttrEditor.onSaveBtn)
        QtCore.QObject.connect(self.calBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), storyAttrEditor.onCalBtn)
        QtCore.QMetaObject.connectSlotsByName(storyAttrEditor)

    def retranslateUi(self, storyAttrEditor):
        storyAttrEditor.setWindowTitle(_translate("storyAttrEditor", "属性编辑", None))
        self.saveBtn.setText(_translate("storyAttrEditor", "保存", None))
        self.calBtn.setText(_translate("storyAttrEditor", "取消", None))
