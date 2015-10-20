# -*- coding: utf-8 -*-
import os
import sys
import units
import xml.etree.ElementTree as xml
from PyQt4 import QtGui, QtCore

class Attrib(object):
	def __init__(self):
		self.key = ''
		self.type = ''
		self.value = ''
		self.comboList = []

class StoryAttrTable(QtGui.QTableWidget):
	def __init__(self, parent = None):
		super(StoryAttrTable, self).__init__(parent)
		self.mparent = None
		self.mColCnt = 1
		self.mRowCnt = 0
		self.attribList = []
		self.configFileName = 'config.xml'
		self.data = {}
		# self.clear()

	def clear(self):
		self.setRowCount(0)
		self.setColumnCount(0)

		if(self.loadConfig()):
			self.mRowCnt = len(self.attribList)
			self.setRowCount(self.mRowCnt)
			self.setColumnCount(self.mColCnt)

			cnt = 0
			for row in self.attribList:
				string = row.key
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(string))
				self.setVerticalHeaderItem(cnt, item)

				if(row.type == 'combo'):
					combo = QtGui.QComboBox()
					QtCore.QObject.connect(combo, QtCore.SIGNAL(units._fromUtf8("currentIndexChanged(int)")), self.mparent.cellChanged)
					self.setCellWidget(cnt, 0, combo)
					for info in row.comboList:
						combo.addItem(units._fromUtf8(info.key))
				elif(row.type == 'text'):
					self.setItem(cnt, 0, QtGui.QTableWidgetItem())
				cnt = cnt + 1

			cnt = 0
			colValue = ["值"]
			for string in colValue:
				item = QtGui.QTableWidgetItem()
				item.setText(units._fromUtf8(string))
				self.setHorizontalHeaderItem(cnt, item)
			cnt = cnt + 1

			self.setCurrentCell(0, 0)

	def setParent(self, parent):
		self.mparent = parent

	def getData(self):
		data = {}
		if(os.path.exists(self.configFileName) == False):
			return self.data

		for row in range(0, self.mRowCnt):
			info = self.attribList[row]
			if(info.type == 'combo'):
				string = unicode(self.cellWidget(row, 0).currentText().toUtf8(), 'utf-8', 'ignore')
				for combo in info.comboList:
					if(string == combo.key):
						string = combo.value
						break
				data[info.value] = string
			elif(info.type == 'text'):
				string = unicode(self.item(row, 0).text().toUtf8(), 'utf-8', 'ignore')
				data[info.value] = string

		return data


	def setData(self, data):
		self.data = data
		if(os.path.exists(self.configFileName) == False):
			return 

		for (key, val) in data.iteritems():
			# print("key = %s value = %s" % (key, val))
			row = 0
			for attrib in self.attribList:
				if(attrib.value == key):
					if(attrib.type == 'combo'):
						for combo in attrib.comboList:
							if(combo.value == val):
								comboBox = self.cellWidget(row, 0)
								idx = comboBox.findText(units._fromUtf8(combo.key))
								if(idx != -1):
									comboBox.setCurrentIndex(idx)
					elif(attrib.type == 'text'):
						item = self.item(row, 0)
						item.setText(units._fromUtf8(val))
				row = row + 1


	def loadConfig(self):
		if(os.path.exists(self.configFileName) == False):
			return False

		self.attribList = []
		storyAttr = xml.parse(self.configFileName).getroot()
		for attr in storyAttr.findall('attr'):
			attrib = Attrib()
			attrib.type = attr.attrib['type']
			attrib.key = attr.attrib['key']
			attrib.value = attr.attrib['value']
			if(attrib.type == 'combo'):
				for combo in attr.findall('combo'):
					comboAttr = Attrib()
					comboAttr.key = combo.attrib['key']
					comboAttr.value = combo.attrib['value']
					attrib.comboList.append(comboAttr)
			self.attribList.append(attrib)
		return True


# def main():
# 	app = QtGui.QApplication(sys.argv)
# 	table = StoryAttrTable()
# 	table.show()
# 	sys.exit(app.exec_())

# if __name__ == '__main__':
# 	main()