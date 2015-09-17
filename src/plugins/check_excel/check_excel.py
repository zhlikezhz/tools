import os
import sys
import check_dialog
from PyQt4 import QtCore, QtGui

def main():
	app = QtGui.QApplication(sys.argv)
	dialog = check_dialog.CheckDialog()
	dialog.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()