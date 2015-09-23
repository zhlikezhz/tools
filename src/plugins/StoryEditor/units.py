# -*- coding: utf-8 -*-
import os
import sys
import  xml.dom.minidom
from PyQt4 import QtGui, QtCore
import xml.etree.ElementTree as xml
from StoryData import ChapterItem, StoryItem

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


class Story(object):
	mCurrStoryFileName = ''

	def __init__(self):
		print('init story')

	def getCurrStoryFileName(self):
		return self.mCurrStoryFileName

	def saveToLua(self, filename):
		fd = open(filename, 'w')

		luaList = []
		luaList.append("module(\"order_info_data\", package.seeall)\n\n")
		luaList.append("gdStory = {\n")

		for card in self.story:
			for story in card.childItems:
				tmp = ('\t\"%s_%s\" = {\n') % (card.itemData, story.itemData)
				luaList.append(tmp)
				cnt = 1
				for ele in story.storyData:
					luaList.append('\t\t[%d] = {\n' % cnt)
					luaList = luaList + self.decodeSaveToLua(ele, 3)
					luaList.append('\t\t}\n')
					cnt = cnt + 1
				luaList.append("\t}\n")
		luaList.append("}\n")
		luaStr = ''.join(luaList)
		print(luaStr)
		fd.write(luaStr)
		fd.close( )

	def decodeSaveToLua(self, ele, cntTab):
		types = "no"
		sentence = ele.itemData['sentence']
		if(ele.itemData['desc'] == _fromUtf8('分支选择')):
			types = 'choose'
		elif(ele.itemData['desc'] == _fromUtf8('分支')):
			types = 'branch'
		elif(ele.itemData['desc'] == _fromUtf8('对话')):
			types = 'dialog'

		luaList = []
		if(ele.itemData['desc'] == _fromUtf8('分支选择')):
			luaList.append(cntTab * '\t')
			luaList.append('\"type\" = \"%s\"\n' % types)
			luaList.append(cntTab * '\t')
			luaList.append('\"sentence\" = \"%s\"\n' % sentence)
			luaList.append(cntTab * '\t')
			luaList.append('\"branch\" = {\n')
			cnt = 1
			for val in ele.childItems:
				luaList.append(cntTab * '\t' + '\t')
				luaList.append('[%d] = {\n' % cnt)
				luaList = luaList + self.decodeSaveToLua(val, cntTab + 2)
				luaList.append(cntTab * '\t' + '\t')
				luaList.append('}\n')
				cnt = cnt + 1
			luaList.append(cntTab * '\t')
			luaList.append('}\n')
		else:
			luaList.append(cntTab * '\t')
			luaList.append('\"type\" = \"%s\"\n' % types)
			luaList.append(cntTab * '\t')
			luaList.append('\"sentence\" = \"%s\"\n' % sentence)

		return luaList


	def saveStory(self, filename):
		root = xml.Element('story')
		tree = xml.ElementTree(root)

		for card in self.story:
			print(card.itemData)
			cardNode = xml.SubElement(root, 'card')
			cardNode.attrib = {'desc': card.itemData}
			for story in card.childItems:
				print(story.itemData)
				storyNode = xml.SubElement(cardNode, 'story')
				storyNode.attrib =  {'desc': story.itemData}
				for ele in story.storyData:
					self.decodeElement(storyNode, ele)
				# cardNode.append(storyNode)
			# root.append(cardNode)

		tree.write(filename, "utf-8", True)

	def decodeElement(self, parent, ele):
		cardNode = xml.SubElement(parent, 'element')
		dic = {}
		dic['sentence'] = ele.itemData['sentence']
		if(ele.itemData['desc'] == _fromUtf8('分支选择')):
			dic['type'] = 'choose'
			for val in ele.childItems:
				self.decodeElement(cardNode, val)
		elif(ele.itemData['desc'] == _fromUtf8('分支')):
			dic['type'] = 'branch'
		elif(ele.itemData['desc'] == _fromUtf8('对话')):
			dic['type'] = 'dialog'
		else:
			dic['type'] = "no"
		cardNode.attrib = dic
		return cardNode


	def loadStory(self, filename):
		print(filename)

		self.story = []
		self.mCurrStoryFileName = filename

		# dom = xml.dom.minidom.parse(filename)
		# root = dom.documentElement
		root = xml.parse(filename).getroot()
		for cardXml in root.findall('card'):
			card = []
			cardDesc = cardXml.attrib['desc']
			cardItem = StoryItem(cardDesc, card)
			for storyXml in cardXml.findall('story'):
				story = []
				storyDesc = storyXml.attrib['desc']
				storyItem = StoryItem(storyDesc, [], cardItem)
				storyItem.storyData = story
				for eleXml in storyXml.findall('element'):
					story.append(self.encodeElement(eleXml))
				card.append(storyItem)
			self.story.append(cardItem)

	def encodeElement(self, eleXml, parent = None):
		data = {}
		branch = []
		parentItem = ChapterItem(data, branch, parent)

		data['type'] = eleXml.attrib['type']
		data['sentence'] = eleXml.attrib['sentence']

		if(data['type'] == 'choose'):
			data['desc'] = _fromUtf8('分支选择')
			for eXml in eleXml.findall('element'):
				branch.append(self.encodeElement(eXml, parentItem))
		elif(data['type'] == "dialog"):
			data['desc'] = _fromUtf8('对话')
		elif(data['type'] == "branch"):
			data['desc'] = _fromUtf8('分支')
		return parentItem

	def getStory(self, card, story):
		for item1 in self.story:
			if(item1.itemData == card):
				for item2 in item1.childItems:
					if(item2.itemData == story):
						return item2.storyData
		return None

	def getCardStoryData(self, card, story):
		branch = self.getStory(card, story)
		if(branch == None):
			return None

		data = {'desc': '类型', 'sentence': '语句'}
		parentItem = ChapterItem(data, branch)
		for item in branch:
			item.setParent(parentItem)

		return parentItem

	def getStoryData(self):
		if(self.story == None):
			return None

		data = '剧情'
		branch = self.story
		parentItem = StoryItem(data, branch)

		for item in branch:
			item.setParent(parentItem)

		return parentItem