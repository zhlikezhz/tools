import xlrd

class ExcelMgr(object):
	excelList = {}

	def __init__(self): 
		print ''

	@staticmethod
	def loadExcel(filename): 
		if(ExcelMgr.excelList.get(filename)):
			return ExcelMgr.excelList[filename]
		else:
			try: 
				excel = xlrd.open_workbook(filename) 
				ExcelMgr.excelList[filename] = excel
				return excel
			except Exception, e: 
				return None

	@staticmethod
	def getExcelRowData(filename, sheetName, sheetColomn): 
		excel = ExcelMgr.loadExcel(filename) 
		if(excel == None):
			return None

		sheet = excel.sheet_by_name(sheetName) 

		count = 0 
		first_row_data = sheet.row_values(0) 
		for i in first_row_data: 
			if(i == sheetColomn): 
				return sheet.col_values(count)[1:] 
			count = count + 1 
		# self.ui.textBrowser.append("\n\n[error: sheet not exist]: \n[sheet: %s][column: %s]\n\n" % (sheetName, sheetColomn))
		return None

	@staticmethod
	def getExcelSheets(filename):
		excel = ExcelMgr.loadExcel(filename) 
		if(excel == None):
			return None

		return excel.sheet_names()

	@staticmethod
	def getExcelTitles(filename, sheetName):
		excel = ExcelMgr.loadExcel(filename) 
		if(excel == None):
			return None

		print sheetName
		sheet = excel.sheet_by_name(sheetName) 
		if(sheet.nrows > 0):
			return sheet.row_values(0)
		else:
			return []