import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import sys


class InputDialog(gui.QDialog):
	def __init__(self, parent=None):
		super(InputDialog, self).__init__(parent)
		self.outputBox = gui.QTextBrowser()
		self.inputBox = gui.QLineEdit("")
		self.inputBox.selectAll()
		self.inputBox.setFocus()

		self.layout = gui.QVBoxLayout()
		self.layout.addWidget(self.outputBox)
		self.layout.addWidget(self.inputBox)
		self.setLayout(self.layout)

		self.connect(self.inputBox, core.SIGNAL("returnPressed()"), self.updateInput)
		self.setWindowTitle("Input")
		self.setFixedHeight(800)
		self.setFixedWidth(1000)
		
	def updateInput(self):
		try: 
			text = unicode(self.inputBox.text()) 
			self.outputBox.append("%s = <b>%s</b>" % (text, eval(text))) 
		except: 
			self.outputBox.append( 
				"<font color=red>%s is invalid!</font>" % text)




def main():
	app = gui.QApplication(sys.argv)
	dialog = InputDialog()
	dialog.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
