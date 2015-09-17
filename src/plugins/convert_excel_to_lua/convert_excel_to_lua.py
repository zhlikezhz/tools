import os
import sys
from PyQt4 import QtCore, QtGui

def main():
	app = QtGui.QApplication(sys.argv)
	btn = QtGui.QPushButton("Quit")
	btn.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

