# -*- coding: utf-8 -*-
import os
import re
from ExcelMgr import ExcelMgr

CheckType = [
	'关联',
	'格式匹配',
	'数据范围',
]


class CheckUnit(object):
	def __init__(self):
		self.mType = ''
		self.mRule = ''
		self.mSrcName = ''
		self.mSrcSheet = ''
		self.mSrcTitle = ''
		self.mDescName = ''
		self.mDescSheet = ''
		self.mDescTitle = ''


class CheckRule(object):
	def __init__(self):
		self.mErrorLog = []

	def check(self, rule, dirPath):
		self.mRule = rule
		self.mDirPath = dirPath
		print rule.mType
		if(rule.mType == CheckType[0]):
			return self.checkRelate()
		elif(rule.mType == CheckType[1]):
			return self.checkFormat()
		elif(rule.mType == CheckType[2]):
			return self.checkRange()
		return 0

	def formatString(self, data):
		formatList = []
		reList = re.split("[#$@&,.;: \n]", str(data))
		for val in reList:
			if(len(val) > 0):
				formatList.append(val)
		return formatList

	def handerString(self, string):
		lists = []
		for i in re.finditer(r'\d+', string):
			lists.append(i.span())

		begin = 0
		formatString = ''
		for i in range(0, len(lists) - 1):
			end = lists[i][0]
			formatString = formatString + string[begin: end] + '|'
			begin = lists[i][1]

		return formatString

	def formatCheckList(self, data):
		checkList = []
		formatList = self.formatString(str(data))
		for i in range(0, len(formatList)):
			if(formatList[i].find('(') >= 0 and formatList[i].find(')') >= 0):
				checkList.append(i)
		return checkList

	def checkRelate(self):
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)
		descFullPath = os.path.join(self.mDirPath, self.mRule.mDescName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		descExcel = ExcelMgr.loadExcel(descFullPath)
		if(srcExcel == None or descExcel == None):
			self.printError("[%s] or [%s] not exist!!" % (srcFullPath, descFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		descData = ExcelMgr.getExcelRowData(descFullPath, self.mRule.mDescSheet, self.mRule.mDescTitle)
		if(srcData == None or descData == None):
			self.printError("[%s] or [%s] not exist!!" % (self.mRule.mSrcTitle, self.mRule.mDescTitle))
			return -1

		cnt = 1
		accept = True
		checkList = self.formatCheckList(self.mRule.mRule)
		for src in srcData:
			cnt = cnt + 1
			formatList = self.formatString(src)
			for idx in checkList:
				exist = False
				val = formatList[idx]
				for desc in descData:
					if(int(val) == int(desc)):
						exist = True
				if(exist == False):
					self.printError('relate error row: %d\nrelate error value: %s\n' % (cnt, val))
					self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
					self.printError('[%s]  [%s]  [%s]\n\n' % (self.mRule.mDescName, self.mRule.mDescSheet, self.mRule.mDescTitle))
					accept = False

		if(accept == False):
			return -1
		return 0

	def checkFormat(self):
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		if(srcExcel == None):
			self.printError("[%s] not exist!!" % (srcFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		if(srcData == None):
			self.printError("[%s] not exist!!" % (self.mRule.mSrcTitle))
			return -1

		baseString = self.handerString(self.mRule.mRule)

		cnt = 0
		accept = True
		for data in srcData:
			cnt = cnt + 1
			if(len(data) < 1):
				continue

			formatString = self.handerString(data)
			if(formatString != baseString):
				self.printError('format error row: %d\n' % (cnt))
				self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
				self.printError('base:\n%s\n' % (self.mRule.mRule))
				self.printError('error:\n%s\n\n' % (data))
				accept = False

		if(accept == False):
			return -1
		return 0

	def checkRange(self):
		print '-----------------------------'
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		if(srcExcel == None):
			self.printError("[%s] not exist!!" % (srcFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		if(srcData == None):
			self.printError("[%s] not exist!!" % (self.mRule.mSrcTitle))
			return -1

		baseList = self.formatString(self.mRule.mRule)
		print baseList
		rangeList = self.formatCheckList(self.mRule.mRule)
		print rangeList
		rangeValList = []
		for idx in rangeList:
			base = baseList[idx]
			rangeVal = base[(base.find('(') + 1):(base.find(')'))]
			# valList = self.formatString(rangeVal)
			valList = re.split('[-]', rangeVal)
			rangeValList.append(int(valList[0]))
			rangeValList.append(int(valList[1]))

		for val in rangeValList:
			print val

		cnt = 1
		accept = True
		checkList = self.formatCheckList(self.mRule.mRule)
		for src in srcData:
			cnt = cnt + 1
			formatList = self.formatString(src)
			cntt = 0
			for idx in checkList:
				exist = False
				val = formatList[idx]
				tmp = cntt * 2
				if(int(val) < rangeValList[tmp] or rangeValList[tmp + 1] < int(val)):
					self.printError('range error row: %d\n %d not in range %d-%d\n' % (cnt, int(val), rangeValList[tmp], rangeValList[tmp + 1]))
					self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
					accept = False
				cntt = cntt + 1

		if(accept == False):
			return -1
		return 0

	def error(self):
		return ''.join(self.mErrorLog)

	def printError(self, string):
		self.mErrorLog.append(string)


