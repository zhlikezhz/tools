# -*- coding: utf-8 -*-
import os
import sys
import xlrd
from PyQt4 import QtCore, QtGui

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

def buildImage(string, pngName):
	size = QtCore.QSize(300, 300)
	image = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
	image.fill(QtGui.QColor(0, 0, 0, 100))

	painter = QtGui.QPainter(image)
	painter.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationOver)

	pen = painter.pen()
	pen.setColor(QtCore.Qt.red)
	font = painter.font()
	font.setBold(True)
	font.setPixelSize(20)

	painter.setPen(pen)
	painter.setFont(font)

	painter.drawText(image.rect(), QtCore.Qt.AlignCenter, _fromUtf8(string))

	image.save(pngName, 'PNG')
	painter.end()

def buildImages():
	excelPath = 'cards.xlsx'
	sheetName = 'Sheet1'

	excel = xlrd.open_workbook(excelPath) 
	if(excel == None):
		return None

	sheet = excel.sheet_by_name(sheetName) 
	cardList = sheet.col_values(0)[1:]
	stringList = sheet.col_values(1)[1:]

	for i in range(0, len(cardList)):
		card = cardList[i]
		string = stringList[i]
		pngName = 'image/%d.png' % int(card)
		buildImage(string, pngName)


def main():
	app = QtGui.QApplication(sys.argv)
	buildImages()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()