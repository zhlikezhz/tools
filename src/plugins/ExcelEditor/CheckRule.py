# -*- coding: utf-8 -*-
import os
import re
from ExcelMgr import ExcelMgr

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
		if(rule.mType == '关联'):
			return self.checkRelate()
		elif(rule.mType == '格式匹配'):
			return self.checkFormat()
		elif(rule.mType == '数据范围'):
			return self.checkRange()
		return 0

	def formatString(self, data):
		formatList = []
		reList = re.split("[#$@&,.;: \n]", str(data))
		for val in reList:
			if(len(val) > 0):
				formatList.append(val)
		return formatList

	def formatCheckList(self, data):
		checkList = []
		formatList = self.formatString(str(data))
		for i in range(0, len(formatList)):
			if(formatList[i][0] == '('):
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

		accept = True
		checkList = self.formatCheckList(self.mRule.mRule)
		for src in srcData:
			formatList = self.formatString(src)
			for idx in checkList:
				exist = False
				val = formatList[idx]
				for desc in descData:
					if(int(val) == int(desc)):
						exist = True
				if(exist == False):
					self.printError('relate error : %s\n' % (val))
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

		baseString = ''.join(re.findall("[#$@&,.;:]", self.mRule.mRule))

		accept = True
		cnt = 0
		for data in srcData:
			cnt = cnt + 1
			formatString = ''.join(re.findall("[#$@&,.;:]", data))
			if(baseString != formatString):
				self.printError('format error: %d\n' % (cnt))
				self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
				self.printError('base:\n%s\n' % (self.mRule.mRule))
				self.printError('error:\n%s\n\n' % (data))
				accept = False

		if(accept == False):
			return -1
		return 0

	def checkRange(self):
		pass

	def error(self):
		return ''.join(self.mErrorLog)

	def printError(self, string):
		self.mErrorLog.append(string)


