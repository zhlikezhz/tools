import sys
import xlrd

def openExcelFile(file):
	try:
		excel = xlrd.open_workbook(file);
		return excel
	except Exception, e:
		print str(e)

def formatExcelData(excel):
        dic = {}
        for sheetIndex in range(0, len(excel.sheet_names()) - 1):
                sheetName = excel.sheet_names()[sheetIndex]
                sheetData = excel.sheet_by_name(sheetName)
                firstRowData = sheetData.row_values(0)
                dic[sheetName] = {}
                for firstIndex in range(0, len(firstRowData) - 1):
                        rowName = firstRowData[firstIndex]
                        dic[sheetName][rowName] = sheetData.col_values(firstIndex)[1]
        return dic


if __name__ == "__main__":
        excel = openExcelFile("1.xlsx")
        data = formatExcelData(excel)
        print data
