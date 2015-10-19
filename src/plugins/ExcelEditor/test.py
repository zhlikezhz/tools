import re
import os
import sys


def handerString(string):
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

def main():
	string1 = '1,2,3,4,5,6,7,8,9'
	string2 = '1,12,300,,4,5,6,7,8,9'

	print handerString(string1)
	print handerString(string2)


if __name__ == '__main__':
	main()