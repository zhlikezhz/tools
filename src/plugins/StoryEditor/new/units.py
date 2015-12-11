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
