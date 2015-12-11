# -*- coding: utf-8 -*-
import os
import sys
import copy
import xml.dom.minidom as minidom
import xml.etree.ElementTree as xml

class UnitData():
	def __init__(self, name = 'default'):
		self.name = name

		self.desc = ""
		self.type = ""
		self.sentence = ""
		
		self.attrib = {}
		self.children = []

class StoryMgr():
	def __init__(self):
		pass

	def newData(self):
		self.storyData = UnitData('root')
		card = UnitData('card')
		card.desc = "new card"
		self.storyData.children.append(card)

	def setData(self, data):
		self.storyData = data

	def loadData(self, filename):
		self.storyData = UnitData('root')
		root = xml.parse(filename).getroot()
		for cardNode in root.findall('card'):
			card = UnitData('card')
			card.desc = cardNode.attrib['desc']
			for storyNode in cardNode.findall('story'):
				story = UnitData('story')
				story.desc = storyNode.attrib['desc']
				def parseTree(parentNode, parent):
					for eleNode in parentNode.findall('element'):
						element = UnitData('element')
						element.type = eleNode.attrib['type']
						element.sentence = eleNode.attrib['sentence']

						for attribNode in eleNode.findall("attr"):
							key = attribNode.attrib['key']
							value = attribNode.attrib['value']
							element.attrib[key] = value

						parseTree(eleNode, element)
						parent.children.append(element)

				parseTree(storyNode, story)
				card.children.append(story)
			self.storyData.children.append(card)

	def save2Xml(self, filename):
		root = xml.Element('story')
		tree = xml.ElementTree(root)

		for card in self.storyData.children:
			cardNode = xml.SubElement(root, card.name)
			cardNode.attrib['desc'] = card.desc
			for story in card.children:
				storyNode = xml.SubElement(cardNode, story.name)
				storyNode.attrib['desc'] = story.desc
				def writeTree(parentNode, parent):
					for element in parent.children:
						eleNode = xml.SubElement(parentNode, element.name)

						eleNode.attrib['type'] = element.type
						eleNode.attrib['sentence'] = element.sentence

						for (key, value) in element.attrib.iteritems():
							attribNode = xml.SubElement(eleNode, 'attr')
							attribNode.attrib['key'] = key
							attribNode.attrib['value'] = value

						writeTree(eleNode, element)

				writeTree(storyNode, story)

		# 格式化XML
		rough_string = xml.tostring(root, 'utf-8')  
		reparsed = minidom.parseString(rough_string)  
		string = ''.join(reparsed.toprettyxml(indent="  " , encoding="utf-8"))

		fd = open(filename, "w")
		fd.write(string)
		fd.close()	

	def save2Lua(self, filename):
		storyData = self.getStoryData()
		if(storyData):
			(path, name)=os.path.split(filename)
			name = name.split('.')[0]

			self.fd = open(filename, "w")
			self.printTo("module(\"%s\", package.seeall)\n\n" % (name))
			self.printTo("gdStory = {\n")

			depth = 1
			for card in storyData.children:
				for story in card.children:
					self.printTo(("%s[\"%s_%s\"] = {\n") % (depth * '\t', card.desc, story.desc))

					def printTree(depth, parent):
						cnt = 1
						for element in parent.children:
							self.printTo(("%s[%d] = {\n") % (depth * '\t', cnt))

							self.printTo(("%stype = \"%s\",\n") % ((depth + 1)* '\t', element.type))
							self.printTo(("%ssentence = \"%s\",\n") % ((depth + 1) * '\t', element.sentence))

							for (key, value) in element.attrib.iteritems():
								self.printTo("%s%s = \"%s\",\n" % ((depth + 1) * '\t', key, value))

							self.printTo(("%sbranch = {\n") % ((depth + 1) * '\t'))
							printTree(depth + 2, element)
							self.printTo("%s},\n" % ((depth + 1) * '\t'))
							self.printTo("%s},\n" % (depth * '\t'))
							cnt += 1

					printTree(depth + 2, story)
					self.printTo("%s},\n" % (depth * '\t'))
			self.printTo("}\n")

			self.fd.close()

	def printTo(self, string):
		self.fd.write(string)

	def getStoryData(self):
		return self.storyData