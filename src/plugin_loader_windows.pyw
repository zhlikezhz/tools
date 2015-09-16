import sys
import xlrd
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

def test2():
	app = gui.QApplication(sys.argv)
	btn = gui.QPushButton("Quit")
	core.QObject.connect(btn, core.SIGNAL("clicked()"), app, core.SLOT("quit()"))
	btn.show()
	sys.exit(app.exec_())


def test1():
	app = gui.QApplication(sys.argv)
	label = gui.QLabel("hello Qt!")
	label.show()
	sys.exit(app.exec_())

def main():
	test2()


if __name__ == '__main__':
	main()



