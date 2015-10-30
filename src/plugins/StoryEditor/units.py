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


class Story(object):
	mCurrStoryFileName = ''

	def __init__(self):
		print('init story')

	def getCurrStoryFileName(self):
		return self.mCurrStoryFileName

	def saveToLua(self, filename):
		fd = open(filename, 'w')

		(path,name)=os.path.split(filename)
		name = name.split('.')[0]
		print name

		luaList = []
		luaList.append("module(\"%s\", package.seeall)\n\n" % (name))
		luaList.append("gdStory = {\n")

		for card in self.story:
			for story in card.childItems:
				tmp = ('\t[\"%s_%s\"] = {\n') % (card.itemData['desc'], story.itemData['desc'])
				luaList.append(tmp)
				cnt = 1
				for ele in story.storyData:
					luaList.append('\t\t[%d] = {\n' % cnt)
					luaList = luaList + self.decodeSaveToLua(ele, 3)
					luaList.append('\t\t},\n')
					cnt = cnt + 1
				luaList.append("\t},\n")
		luaList.append("}\n")
		luaStr = ''.join(luaList)
		fd.write(luaStr)
		fd.close()

	def decodeSaveToLua(self, ele, cntTab):
		types = ele.itemData['type']
		sentence = ele.itemData['sentence']
		attrList = ele.itemData['attr']

		luaList = []
		# if(ele.itemData['type'] == 'choose'):
		luaList.append(cntTab * '\t')
		luaList.append('type = \"%s\",\n' % types)
		luaList.append(cntTab * '\t')
		luaList.append('sentence = \"%s\",\n' % sentence)
		luaList.append(cntTab * '\t')
		luaList.append('branch = {\n')
		cnt = 1
		for val in ele.childItems:
			luaList.append(cntTab * '\t' + '\t')
			luaList.append('[%d] = {\n' % cnt)
			luaList = luaList + self.decodeSaveToLua(val, cntTab + 2)
			luaList.append(cntTab * '\t' + '\t')
			luaList.append('},\n')
			cnt = cnt + 1
		luaList.append(cntTab * '\t')
		luaList.append('},\n')
		# else:
		# 	luaList.append(cntTab * '\t')
		# 	luaList.append('type = \"%s\",\n' % types)
		# 	luaList.append(cntTab * '\t')
		# 	luaList.append('sentence = \"%s\",\n' % sentence)

		for(key, val) in attrList.iteritems():
			luaList.append(cntTab * '\t')
			luaList.append('%s = \"%s\",\n' % (key, val))

		return luaList


	def saveStory(self, filename):
		root = xml.Element('story')
		tree = xml.ElementTree(root)

		for card in self.story:
			print(card.itemData)
			cardNode = xml.SubElement(root, 'card')
			cardNode.attrib = {'desc': card.itemData['desc']}
			for story in card.childItems:
				print(story.itemData)
				storyNode = xml.SubElement(cardNode, 'story')
				storyNode.attrib =  {'desc': story.itemData['desc']}
				for ele in story.storyData:
					self.decodeElement(storyNode, ele)

		tree.write(filename, "utf-8", True)

	def decodeElement(self, parent, ele):
		cardNode = xml.SubElement(parent, 'element')
		dic = {}
		dic['type'] = ele.itemData['type']
		dic['sentence'] = ele.itemData['sentence']
		# if(ele.itemData['type'] == 'choose' or ele.itemData['type'] == 'branch'):
		for val in ele.childItems:
			self.decodeElement(cardNode, val)

		for (key, value) in ele.itemData['attr'].iteritems():
			attrNode = xml.SubElement(cardNode, 'attr')
			attrNode.attrib = {'key': key, 'value': value}

		# for attr in eleXml.findall('attr'):
		# 	key = attr.attrib['key']
		# 	value = attr.attrib['value']
		# 	data['attr'][key] = value

		cardNode.attrib = dic
		return cardNode

	def newStory(self, filename):
		self.mCurrStoryFileName = filename
		self.story = []
		data = {'desc': 'card_0', 'type': 'card'}
		cardItem = StoryItem(data, [])
		self.story.append(cardItem)

	def loadStory(self, filename):
		self.story = []
		self.mCurrStoryFileName = filename

		root = xml.parse(filename).getroot()
		for cardXml in root.findall('card'):
			card = []
			cardDesc = cardXml.attrib['desc']
			data = {'desc': cardDesc, 'type': 'card'}
			cardItem = StoryItem(data, card)
			for storyXml in cardXml.findall('story'):
				story = []
				storyDesc = storyXml.attrib['desc']
				data = {'desc': storyDesc, 'type': 'story'}
				storyItem = StoryItem(data, [], cardItem)
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
		for eXml in eleXml.findall('element'):
			branch.append(self.encodeElement(eXml, parentItem))

		data['attr'] = {}
		for attr in eleXml.findall('attr'):
			key = attr.attrib['key']
			value = attr.attrib['value']
			data['attr'][key] = value

		return parentItem

	def getStory(self, card, story):
		for item1 in self.story:
			if(item1.itemData['desc'] == card):
				for item2 in item1.childItems:
					if(item2.itemData['desc'] == story):
						return item2.storyData
		return None

	def getCardStoryData(self, card, story):
		branch = None
		if(card < 0 or story < 0):
			branch = None
		else:
			branch = self.story[card].childItems[story].storyData

		data = {'type': '类型', 'sentence': '语句', 'attr': {}}
		if(branch == None):
			parentItem = ChapterItem(data, [])
		else:
			parentItem = ChapterItem(data, branch)
			for item in branch:
				print(len(branch))
				item.setParent(parentItem)
		return parentItem

	def getStoryData(self):
		if(self.story == None):
			return None

		data = {'type': 'parent', 'desc': '剧情'}
		branch = self.story
		parentItem = StoryItem(data, branch)

		for item in branch:
			item.setParent(parentItem)

		return parentItem

	def calChpaterWords(self, chapter):
		length = len(chapter.itemData['sentence'])
		return length

	def calStoryWords(self, story):
		length = 0
		for chapter in story.storyData:
			length = length + self.calChpaterWords(chapter)
		return length

	def calCardWords(self, card):
		length = 0
		for story in card.childItems:
			length = length + self.calStoryWords(story)
		return length

	def calTotalWords(self):
		length = 0
		for card in self.story:
			length = length + self.calCardWords(card)
		return length



