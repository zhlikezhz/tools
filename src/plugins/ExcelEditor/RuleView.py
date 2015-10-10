# -*- coding: utf-8 -*-
import os
import sys
import units
from RuleEdit import RuleEdit
from CheckRule import CheckUnit
from PyQt4 import QtGui, QtCore

class RuleView(QtGui.QTableView):
	def __init__(self, parent = None):
		super(RuleView, self).__init__(parent)

		self.model = QtGui.QStandardItemModel()
		self.model.setColumnCount(8)
		self.model.setHeaderData(0, QtCore.Qt.Horizontal, units._fromUtf8('类型'))
		self.model.setHeaderData(1, QtCore.Qt.Horizontal, units._fromUtf8('源excel'))
		self.model.setHeaderData(2, QtCore.Qt.Horizontal, units._fromUtf8('源sheet'))
		self.model.setHeaderData(3, QtCore.Qt.Horizontal, units._fromUtf8('源title'))
		self.model.setHeaderData(4, QtCore.Qt.Horizontal, units._fromUtf8('目标excel'))
		self.model.setHeaderData(5, QtCore.Qt.Horizontal, units._fromUtf8('目标sheet'))
		self.model.setHeaderData(6, QtCore.Qt.Horizontal, units._fromUtf8('目标title'))
		self.model.setHeaderData(7, QtCore.Qt.Horizontal, units._fromUtf8('格式'))
		self.setModel(self.model)
		self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

	def setRules(self, rules):
		cnt = 0
		self.model.clear()
		for rule in rules:
			self.addRule(cnt, rule)
			cnt = cnt + 1

	def addRule(self, row, rule):
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mType))
		self.model.setItem(row, 0, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mSrcName))
		self.model.setItem(row, 1, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mSrcSheet))
		self.model.setItem(row, 2, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mSrcTitle))
		self.model.setItem(row, 3, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mDescName))
		self.model.setItem(row, 4, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mDescSheet))
		self.model.setItem(row, 5, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mDescTitle))
		self.model.setItem(row, 6, item)
		item =  QtGui.QStandardItem(units._fromUtf8(rule.mRule))
		self.model.setItem(row, 7, item)

	def setRule(self, row, unit):
		item = self.model.index(row, 0)
		self.model.setData(item, units._fromUtf8(unit.mType), QtCore.Qt.EditRole)
		item = self.model.index(row, 1)
		self.model.setData(item, units._fromUtf8(unit.mSrcName), QtCore.Qt.EditRole)
		item = self.model.index(row, 2)
		self.model.setData(item, units._fromUtf8(unit.mSrcSheet), QtCore.Qt.EditRole)
		item = self.model.index(row, 3)
		self.model.setData(item, units._fromUtf8(unit.mSrcTitle), QtCore.Qt.EditRole)
		item = self.model.index(row, 4)
		self.model.setData(item, units._fromUtf8(unit.mDescName), QtCore.Qt.EditRole)
		item = self.model.index(row, 5)
		self.model.setData(item, units._fromUtf8(unit.mDescSheet), QtCore.Qt.EditRole)
		item = self.model.index(row, 6)
		self.model.setData(item, units._fromUtf8(unit.mDescTitle), QtCore.Qt.EditRole)
		item = self.model.index(row, 7)
		self.model.setData(item, units._fromUtf8(unit.mRule), QtCore.Qt.EditRole)

	def setParent(self, parent):
		self.mParent = parent

	def getRule(self, row):
		unit = CheckUnit()
		item = self.model.index(row, 0)
		unit.mType = unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 1)
		unit.mSrcName =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 2)
		unit.mSrcSheet =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 3)
		unit.mSrcTitle =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 4)
		unit.mDescName =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 5)
		unit.mDescSheet =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 6)
		unit.mDescTitle =  unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		item = self.model.index(row, 7)
		unit.mRule = unicode(self.model.data(item).toString().toUtf8(), 'utf-8', 'ignore')
		return unit

	def getRules(self):
		rules = []
		row = self.model.rowCount()
		for i in range(0, row):
			rule = self.getRule(i)
			rules.append(rule)
		return rules

	def addItem(self):
		row = self.model.rowCount()
		self.model.insertRow(row)
		rule = CheckUnit()
		self.addRule(row, rule)

	def removeItem(self):
		item = self.currentIndex()
		self.model.removeRow(item.row())

	def mouseDoubleClickEvent(self, evt):
		super(RuleView, self).mouseDoubleClickEvent(evt)
		if(evt.button() == QtCore.Qt.LeftButton):
			row = self.currentIndex().row()
			rule = RuleEdit(self)
			rule.setDirPath(self.mParent.mDirPath)
			rule.setFileList(self.mParent.mFileList)
			unit = self.getRule(row)
			rule.setCheckUnit(unit)
			re = rule.exec_()
			if(re == QtGui.QDialog.Accepted):
				unit = rule.getCheckUnit()
				self.setRule(row, unit)