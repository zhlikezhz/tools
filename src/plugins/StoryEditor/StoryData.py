# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, QtCore

class StoryData(object):
    def __init__(self, filename = ""):
        self.storyData = {
            'chapter_1': [
                { 
                'type': 'dialog',
                'dialog': '你好么！',
                'sound': '1.mp3',
                'branch': [],
                },

                {
                'type': 'choose',
                'dialog': '...........',
                'sound': '4.mp3',
                'branch': 
                        [
                            {
                            'type': 'dialog',
                            'dialog': '我不好！',
                            'sound': '2.mp3',
                            'branch': [],
                            },
                            {
                            'type': 'dialog',
                            'dialog': "我很好！",
                            'sound': "3.mp3",
                            'branch': [],
                            },
                        ],
                },
            ],
            'chapter_2': [
                { 
                'type': 'dialog',
                'dialog': '你好么！',
                'sound': '1.mp3',
                'branch': [],
                },

                {
                'type': 'choose',
                'dialog': '...........',
                'sound': '4.mp3',
                'branch': 
                        [
                            {
                            'type': 'dialog',
                            'dialog': '我不好！',
                            'sound': '2.mp3',
                            'branch': [],
                            },
                            {
                            'type': 'dialog',
                            'dialog': "我很好！",
                            'sound': "3.mp3",
                            'branch': [],
                            },
                        ],
                },
            ],
        }

    def getChapterData(self, chapter):
        if(self.storyData[chapter] == None):
            return None

        stack = []
        chapterData = []
        for item in self.storyData[chapter]:
            chapterItem = ChapterItem(item, None)
            chapterData.append(chapterItem)
            stack.append(chapterItem)

        while(len(stack) > 0):
            parentItem = stack.pop()
            for child in parentItem.itemData['branch']:
                chapterItem = ChapterItem(child, parentItem)
                parentItem.appendChild(chapterItem)
                stack.append(chapterItem)

        return chapterData


    def getStoryData(self):
        storyData = []
        for item in self.storyData.keys():
            storyItem = StoryItem(item)
            storyData.append(storyItem)
        return storyData

class StoryItem(object):
    def __init__(self, data, parent = None):
        self.parentItem = parent
        self.itemData = data
        self.childrenItem = []

    def appendChild(self, child):
        self.childrenItem.append(child)

    def child(self, row):
        return self.childrenItem[row]

    def childCount(self):
        return len(self.childrenItem)

    def columnCount(self):
        return 1

    def data(self, column):
        val = None
        if(column == 0):
            val = QtCore.QString.fromUtf8(self.itemData)
        return val

    def parent(self):
        return self.parentItem

    def row(self):
        return self.parentItem.childrenItem.index(self)

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData = value.toString()

        return True

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childrenItem):
            return False

        for row in range(count):
            data = 'No data'
            item = StoryItem(data, self)
            self.childrenItem.insert(position, item)

        return True

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childrenItem):
            return False

        for row in range(count):
            self.childrenItem.pop(position)

        return True



class ChapterItem(object):
    def __init__(self, data, parent = None):
        self.parentItem = parent
        self.itemData = data
        self.childrenItem = []

    def appendChild(self, child):
        self.childrenItem.append(child)

    def child(self, row):
        return self.childrenItem[row]

    def childCount(self):
        return len(self.childrenItem)

    def columnCount(self):
        return 2

    def data(self, column):
        val = None
        if(column == 0):
            val = QtCore.QString.fromUtf8(self.itemData['type'])
        elif(column == 1):
            val = QtCore.QString.fromUtf8(self.itemData['dialog'])
        return val

    def parent(self):
        return self.parentItem

    def row(self):
        return self.parentItem.childrenItem.index(self)


    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        if(column == 0):
            self.itemData['type'] = value.toString()
        elif(column == 1):
            self.itemData['dialog'] = value.toString()

        return True

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childrenItem):
            return False

        for row in range(count):
            data = 'No data'
            item = StoryItem(data, self)
            self.childrenItem.insert(position, item)

        return True

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childrenItem):
            return False

        for row in range(count):
            self.childrenItem.pop(position)

        return True