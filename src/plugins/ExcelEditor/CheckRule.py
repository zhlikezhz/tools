# -*- coding: utf-8 -*-
import os
import re
from ExcelMgr import ExcelMgr

CheckType = [
	'关联',
	'格式匹配',
	'数据范围',
	'多格式匹配',
	'变长匹配',
	'变长关联',
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
		if(rule.mType == CheckType[0]):
			return self.checkRelate()
		elif(rule.mType == CheckType[1]):
			return self.checkFormat()
		elif(rule.mType == CheckType[2]):
			return self.checkRange()
		elif(rule.mType == CheckType[3]):
			return self.checkMultFormat()
		elif(rule.mType == CheckType[4]):
			return self.newCheckFormat()
		elif(rule.mType == CheckType[5]):
			return self.newCheckRelate()
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

	def handerString1(self, string):
		lists = []
		for i in re.finditer(r'\d+', string):
			lists.append(i.span())

		begin = 0
		formatString = ''
		for i in range(0, len(lists) - 1):
			end = lists[i][0]
			formatString = formatString + string[begin: end] + '|' * (lists[i][1] - lists[i][0])
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
			src = str(src)
			if(len(src) < 1):
				continue

			formatList = self.formatString(src)
			for idx in checkList:
				exist = False
				if(idx >= len(formatList)):
					break
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

		cnt = 1
		accept = True
		for data in srcData:
			cnt = cnt + 1
			data = str(data)
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

	def checkMultFormat(self):
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		if(srcExcel == None):
			self.printError("[%s] not exist!!" % (srcFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		if(srcData == None):
			self.printError("[%s] not exist!!" % (self.mRule.mSrcTitle))
			return -1

		begin = 0
		length = len(self.mRule.mRule)
		baseStringList = []
		while(begin < length):
			bPos = self.mRule.mRule.find('(', begin, length) + 1
			ePos = self.mRule.mRule.find(')', begin, length)
			if(bPos == -1 or ePos == -1):
				break
			sub = self.mRule.mRule[bPos: ePos]
			baseString = self.handerString1(sub)
			baseStringList.append(baseString)
			begin = ePos + 1

		cnt = 1
		accept = True
		for data in srcData:
			cnt = cnt + 1
			data = str(data)
			multformat = False
			formatString = self.handerString1(data)
			for baseString in baseStringList:
				if(formatString == baseString):
					multformat = True
					break

			if(multformat == False):
				self.printError('format error row: %d\n' % (cnt))
				self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
				self.printError('base:\n%s\n' % (self.mRule.mRule))
				self.printError('error:\n%s\n\n' % (data))
				accept = False

		if(accept == False):
			return -1
		return 0

	def checkRange(self):
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
		rangeList = self.formatCheckList(self.mRule.mRule)
		rangeValList = []
		for idx in rangeList:
			base = baseList[idx]
			rangeVal = base[(base.find('(') + 1):(base.find(')'))]
			valList = re.split('[-]', rangeVal)
			rangeValList.append(int(valList[0]))
			rangeValList.append(int(valList[1]))

		cnt = 1
		accept = True
		checkList = self.formatCheckList(self.mRule.mRule)
		for src in srcData:
			cnt = cnt + 1
			src = str(src)
			if(len(src) < 1):
				continue
				
			cntt = 0
			formatList = self.formatString(src)
			for idx in checkList:
				exist = False
				if(idx >= len(formatList)):
					break
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

	def newCheckFormat(self):
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		if(srcExcel == None):
			self.printError("[%s] not exist!!" % (srcFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		if(srcData == None):
			self.printError("[%s] not exist!!" % (self.mRule.mSrcTitle))
			return -1

		# baseString = self.handerString(self.mRule.mRule)
		baseString = self.mRule.mRule
		if(self.checkFormat1(baseString)):
			baseString = self.cvtNumber2Symbol(baseString)
			print baseString
			cnt = 1
			accept = True
			for data in srcData:
				cnt = cnt + 1
				data = str(data)
				if(len(data) < 1):
					continue

				desString = self.cvtNumber2Symbol(data)
				# print desString
				if not (self.matchString(baseString, 0, desString, 0)):
					self.printError('format error row: %d\n' % (cnt))
					self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
					self.printError('base:\n%s\n' % (self.mRule.mRule))
					self.printError('error:\n%s\n\n' % (data))
					accept = False

			if(accept == False):
				return -1
		return 0

	def newCheckRelate(self):
		srcFullPath = os.path.join(self.mDirPath, self.mRule.mSrcName)
		descFullPath = os.path.join(self.mDirPath, self.mRule.mDescName)

		srcExcel = ExcelMgr.loadExcel(srcFullPath)
		descExcel = ExcelMgr.loadExcel(descFullPath)
		if(srcExcel == None or descExcel == None):
			self.printError("[%s] or [%s] not exist!!" % (srcFullPath, descFullPath))
			return -1

		srcData = ExcelMgr.getExcelRowData(srcFullPath, self.mRule.mSrcSheet, self.mRule.mSrcTitle)
		self.descData = ExcelMgr.getExcelRowData(descFullPath, self.mRule.mDescSheet, self.mRule.mDescTitle)
		if(srcData == None or self.descData == None):
			self.printError("[%s] or [%s] not exist!!" % (self.mRule.mSrcTitle, self.mRule.mDescTitle))
			return -1

		self.cnt = 1
		self.accept = True

		baseString = self.cvtNumber2Symbol(self.mRule.mRule)
		self.relateList = self.buildRelate(baseString)
		baseString = self.removeSymbol(baseString, '(')
		baseString = self.removeSymbol(baseString, ')')

		for src in srcData:
			self.cnt = self.cnt + 1
			src = str(src)
			if(len(src) < 1):
				continue
			self.buildRelateValue(src)
			desString = self.cvtNumber2Symbol(src)
			# print baseString
			# print desString
			self.matchString1(baseString, 0, desString, 0)

		if(self.accept == False):
		 	return -1
		return 0


	def error(self):
		return ''.join(self.mErrorLog)

	def printError(self, string):
		self.mErrorLog.append(string)

	def cvtNumber2Symbol(self, string):
		numberPairs = []
		for i in re.finditer(r'\d+', string):
			numberPairs.append(i.span())

		begin = 0
		symbolString = ''
		for i in range(0, len(numberPairs)):
			end = numberPairs[i][0]
			symbolString = symbolString + string[begin: end] + '|'
			begin = numberPairs[i][1]

		length = len(string)
		if(begin < length):
			symbolString = symbolString + string[begin: length]

		return symbolString

	def checkFormat1(self, string):
		stack = []
		for char in string:
			if(char == '['):
				stack.append(1)
			elif(char == ']'):
				if(len(stack) == 0):
					self.printError('format error: []\n')
					return False
				else:
					stack.pop()

		if(len(stack) > 0):
			self.printError('format error: []\n')
			return False

		stack = []
		for char in string:
			if(char == '<'):
				stack.append(1)
			elif(char == '>'):
				if(len(stack) == 0):
					self.printError('format error: <>\n')
					return False
				else:
					stack.pop()
		if(len(stack) > 0):
			self.printError('format error: <>\n')
			return False

		stack = []
		for pos in range(0, len(string)):
			if(string[pos] == ']'):
				if not (string[pos+1] == '<'):
					self.printError('format error: ]<\n')
					return False
		return True

	def findBracketPair(self, string, leftBracket, rightBracket):
		stack = []
		for pos in range(0, len(string)):
			char = string[pos]
			if(char == leftBracket):
				stack.append(1)
			elif(char == rightBracket):
				stack.pop()
			if(len(stack) == 0):
				return pos
		return -1

	def isEnd(self, string):
		stack1 = []
		stack2 = []
		for char in string:
			if(char == '['):
				stack1.append(1)
			elif(char == ']'):
				if(len(stack1) > 0):
					stack1.pop()
			elif(char == '<'):
				stack2.append(1)
			elif(char == '>'):
				if(len(stack2) > 0):
					stack2.pop()
			elif(len(stack1) == 0 and len(stack2) == 0):
				return False
		return True

	def matchString(self, baseString, basePos, desString, desPos):
		desLen = len(desString)
		baseLen = len(baseString)
		if(desPos == desLen): 
			return self.isEnd(baseString[basePos:])
		elif(basePos >= baseLen):
			return False

		if(baseString[basePos] == '['):
			rightBracketPos = self.findBracketPair(baseString[basePos:], '[', ']') + basePos
			rightBracketPos = self.findBracketPair(baseString[rightBracketPos + 1:], '<', '>') + rightBracketPos + 1
			ret = self.matchString(baseString, rightBracketPos + 1, desString, desPos)
			if(ret):
				return True

			ret = self.matchString(baseString, basePos + 1, desString, desPos)
			return ret
		elif(baseString[basePos] == ']'):
			rightBracketPos = self.findBracketPair(baseString[basePos + 1:], '<', '>') + basePos + 1
			ret = self.matchString(baseString, rightBracketPos + 1, desString, desPos)
			if(ret):
				return True

			leftBracketPos = self.findBracketPair(baseString[0:basePos + 1][::-1], ']', '[')
			leftBracketPos = basePos - leftBracketPos

			symbols = baseString[basePos+2:rightBracketPos]
			for symbol in symbols:
				if(desString[desPos] == symbol):
					ret = self.matchString(baseString, leftBracketPos + 1, desString, desPos + 1)
					break
			return ret

		elif(baseString[basePos] == desString[desPos]):
			ret = self.matchString(baseString, basePos + 1, desString, desPos + 1)
			return ret
		else:
			return False

	def matchString1(self, baseString, basePos, desString, desPos):
		desLen = len(desString)
		baseLen = len(baseString)
		if(desPos == desLen): 
			return self.isEnd(baseString[basePos:])
		elif(basePos >= baseLen):
			return False

		if(baseString[basePos] == '['):
			rightBracketPos = self.findBracketPair(baseString[basePos:], '[', ']') + basePos
			rightBracketPos = self.findBracketPair(baseString[rightBracketPos + 1:], '<', '>') + rightBracketPos + 1
			ret = self.matchString1(baseString, rightBracketPos + 1, desString, desPos)
			if(ret):
				return True

			ret = self.matchString1(baseString, basePos + 1, desString, desPos)
			return ret
		elif(baseString[basePos] == ']'):
			rightBracketPos = self.findBracketPair(baseString[basePos + 1:], '<', '>') + basePos + 1
			ret = self.matchString1(baseString, rightBracketPos + 1, desString, desPos)
			if(ret):
				return True

			leftBracketPos = self.findBracketPair(baseString[0:basePos + 1][::-1], ']', '[')
			leftBracketPos = basePos - leftBracketPos

			symbols = baseString[basePos+2:rightBracketPos]
			for symbol in symbols:
				if(desString[desPos] == symbol):
					ret = self.matchString1(baseString, leftBracketPos + 1, desString, desPos + 1)
					break
			return ret

		elif(baseString[basePos] == desString[desPos]):
			ret = self.matchString1(baseString, basePos + 1, desString, desPos + 1)
			if(ret == True and desString[desPos] == '|'):
				if (basePos+1) in self.relateList:
					exist = False
					val = int(self.numberList[desPos])
					for desc in self.descData:
						if(val == int(desc)):
							exist = True
							break

					if(exist == False):
						self.printError('relate error row: %d\nrelate error value: %s\n' % (self.cnt, self.numberList[desPos]))
						self.printError('[%s]  [%s]  [%s]\n' % (self.mRule.mSrcName, self.mRule.mSrcSheet, self.mRule.mSrcTitle))
						self.printError('[%s]  [%s]  [%s]\n\n' % (self.mRule.mDescName, self.mRule.mDescSheet, self.mRule.mDescTitle))
						self.accept = False
			return ret
		else:
			return False

	def buildRelate(self, string):
		relate = []
		cnt = 0
		for pos in range(0, len(string)):
			if(string[pos] ==  '('):
				right = self.findBracketPair(string[pos:], '(', ')') + pos
				if(right - pos == 2):
					relate.append(right - 1 - cnt)
					cnt += 2
		return relate

	def removeSymbol(self, string, symbol):
		strList = []
		for char in string:
			if not (char == symbol):
				strList.append(char)
		return ''.join(strList)

	def buildRelateValue(self, string):
		self.numberList = {}
		tmpArr = re.findall(r'\d+', string)
		newString = self.cvtNumber2Symbol(string)

		cnt = 0
		for pos in range(0, len(newString)):
			if(newString[pos] == '|'):
				self.numberList[pos] = tmpArr[cnt]
				cnt = cnt + 1