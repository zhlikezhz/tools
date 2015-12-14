# -*- coding: utf-8 -*-
import os
import sys
import StoryData
from PyQt4 import QtGui, QtCore

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

def _toUtf8(qstring):
	return unicode(qstring.toUtf8(), 'utf-8', 'ignore')

def getTypelist():
	typeList = [
		{'val': '对话', 'key': 'dialog'},
		{'val': '分支', 'key': 'branch'},
		{'val': '分支选择', 'key': 'choose'},
	]
	return typeList

def typeMapping(types):
	val = "类型"
	if(types == 'choose'):
		val = '分支选择'
	elif(types == 'dialog'):
		val = '对话'
	elif(types == 'branch'):
		val = '分支'
	return val
