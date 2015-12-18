# -*- coding: utf-8 -*-
import os
import sys
import copy
import xml.dom.minidom as minidom
import xml.etree.ElementTree as xml

class Attribute():
	def __init__(self):
		self.key = ''
		self.type = ''
		self.value = ''
		self.comboList = []

		self.row = -1
		self.parentRow = -1

		self.parentName = ''
		self.hasParent = False

		self.children = []
		self.hasChild = False

	def getConnectName(self, comboValue):
		for child in self.comboList:
			if(child.value == comboValue):
				return child.parentName
		return ''

	def getShowValue(self):
		return self.key

	def getSaveValue(self):
		return self.value

	def getChildSaveValue(self, value, parentName = ""):
		for child in self.comboList:
			if(child.key == value):
				if(child.hasParent == True):
					if(parentName == child.parentName):
						return child.value
				else:
					return child.value
		return ""

	def getChildShowValue(self, value):
		for child in self.comboList:
			if(child.value == value):
				return child.key
		return ""

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  
 
@singleton  
class MatchMgr():
	def __init__(self):
		self.attributeList = []
		self.loadConfig('config.xml')

	def loadConfig(self, filename):
		if(os.path.exists(filename) == False):
			return False

		self.attributeList = []
		root = xml.parse(filename).getroot()
		for attrNode in root.findall("attr"):
			attr = Attribute()
			attr.type = attrNode.attrib['type']
			attr.key = attrNode.attrib['key']
			attr.value = attrNode.attrib['value']
			if(attr.type == "combo"):
				if(attrNode.attrib.has_key('connect') == True):
					attr.parentName = attrNode.attrib['connect']
					attr.hasParent = True

				for comboNode in attrNode.findall('combo'):
					combo = Attribute()
					combo.key = comboNode.attrib['key']
					combo.value = comboNode.attrib['value']
					if(comboNode.attrib.has_key('connect') == True):
						combo.parentName = comboNode.attrib['connect']
						combo.hasParent = True
					attr.comboList.append(combo)

			self.attributeList.append(attr)

		self.parseConfig(self.attributeList)
		return True

	def parseConfig(self, attributeList):
		row = 0
		for attr in attributeList:
			attr.row = row
			if(attr.hasParent == True):
				parentRow = 0
				for parentAttr in attributeList:
					if(parentAttr.key == attr.parentName):
						parentAttr.children.append(attr)
						parentAttr.hasChild = True
						attr.parentRow = parentRow
						break
					parentRow += 1
			row += 1

	def getShowValue(self, saveKey, saveValue):
		for attr in self.attributeList:
			if(saveKey == attr.getSaveValue()):
				return attr.getChildShowValue(saveValue)
		return ""

	def filterAttribute(self, data):
		tmpStack = []
		updateStack = []
		updateStackBackup = []
		for (saveKey, saveValue) in data.iteritems():
			item = []
			item.append(saveKey)
			item.append(saveValue)
			for attr in self.attributeList:
				if(attr.getSaveValue() == saveKey):
					item.append(attr.row)
					if(attr.hasParent == True):
						if attr.parentRow in tmpStack:
							index = tmpStack.index(attr.parentRow)
							tmpStack.insert(index, attr.row)
							updateStack.insert(index, item)
							updateStackBackup.insert(index, item)
						else:
							updateStack.append(item)
							updateStackBackup.append(item)
							tmpStack.append(attr.row)
					else:
						updateStack.append(item)
						updateStackBackup.append(item)
						tmpStack.append(attr.row)
					break

		newData = {}
		while(len(updateStack) > 0):
			item = updateStack.pop()
			saveKey = item[0]
			saveValue = item[1]
			attr = self.attributeList[item[2]]
			if(attr.hasParent == True):
				if (attr.parentRow in tmpStack):
					index = tmpStack.index(attr.parentRow)
					parentItem = updateStackBackup[index]
					parent = self.attributeList[attr.parentRow]
					currParentName = parent.getChildShowValue(parentItem[1])
					parentName = attr.getConnectName(saveValue)
					if(currParentName == parentName):
						newData[saveKey] = saveValue
			else:
				newData[saveKey] = saveValue
		return newData
