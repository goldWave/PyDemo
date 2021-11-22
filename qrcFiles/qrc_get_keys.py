# coding = utf-8

import sys
sys.path.append("../")

import os
from qrc_all_files import *

from ini_common_method import findAllCheckFile


def get_subfix(_keys):
	_sub = set()
	for x in _keys:
		_sub.add(x.split('.')[-1])
		if x.split('.')[-1] == '6':
			print(x)
			break
	print(_sub)

if __name__ == '__main__':
	_files = findAllQRCFile()
	for f in _files:
		# print(f)
		pass

	_allKeys = []
	for x in _files:
		get_qrc_keys(x, _allKeys)
	# print(_allKeys)
	# for f in _allKeys:
	# 	print(f)

	get_subfix(_allKeys)
	_checkFiels = findAllCheckFile()
	_notused = openAndCheckUsedData_Single(_checkFiels, _allKeys)
	for x in _notused:
		print(x)
	# print(_checkFiels)





