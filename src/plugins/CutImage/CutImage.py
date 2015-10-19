import os
import sys
import ConfigParser
import PythonMagick as Magick

def cutPng():
	cf = ConfigParser.ConfigParser()
	cf.read("setting.conf")
	cutw = int(cf.get("position", "cut_width"))
	cuth = int(cf.get("position", "cut_height"))
	startx = int(cf.get("position", "cut_start_position_x"))
	starty = int(cf.get("position", "cut_start_position_y"))
	srcPath = cf.get("document", "cut_srcouce_document")
	desPath = cf.get("document", "cut_destination_document")

	if(os.path.exists(srcPath)):
		pngNameList = os.listdir(srcPath)
	else:
		print ('document %s not exists' % os.path.abspath(srcPath))
		sys.exit(0)

	for pngName in pngNameList:
		if(pngName[-4:] == '.png'):
			srcFullPath = os.path.abspath(os.path.join(srcPath, pngName))
			desFullPath = os.path.abspath(os.path.join(desPath, pngName))
			if(os.path.exists(srcFullPath)):
				image = Magick.Image(srcFullPath)
				image.crop(Magick.Geometry(cutw, cuth, startx, starty))
				image.write(desFullPath)
			else:
				print ('file %s not exists!!' % srcFullPath)


if __name__ == '__main__':
	cutPng()