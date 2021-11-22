# coding = utf-8

import os, time, glob, sys
from ini_common_method import *
from time import ctime, sleep
import  multiprocessing as mp

# s_ini_paths = ["C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\en-US.ini", "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\id-ID.ini","C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\ko-KR.ini","C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\pt-BR.ini"]
dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

def get_testKeys(_list) -> list:
	""" 获取所有的 cpp h 之类的文件列表 """
	s_path_test = "D:\\languageCache\\test_keys.txt"
	_allKeys = list()
	if os.path.exists(s_path_test):
		with open(s_path_test, 'r', encoding='utf-8') as f:
			allLines = f.readlines()
			for x in allLines:
				x = x.strip('\n')
				_allKeys.append(x)
		return _allKeys
	print("1")
	with open(s_path_test, 'w', encoding='utf-8') as fp:
		fp.truncate()
		for x in _list:
			fp.write(x)
			fp.write('\n')

	return _list

def get_all_compare_keys():
	_dir = 'D:\\languageCache\\cache.txt'
	_allFiles = list()
	if os.path.exists(_dir):
		with open(_dir, 'r', encoding='utf-8') as f:
			allLines = f.readlines()
			for x in allLines:
				x = x.strip('\n')
				_allFiles.append(x)
		return _allFiles

if __name__ == '__main__':
	# _allKeys = getINIKeys(s_ini_paths[3])

	# for i in range(len(_allKeys) - 1, -1, -1):
	# 	_key = _allKeys[i]
	# 	if _key.startswith('Channels.'):
	# 		_allKeys.remove(_key)

	_li = findAllCheckFile()

	_list_i = findAllCheckFile_i()
	_allKeys = get_all_compare_keys()
	print(len(_allKeys))
	# sys.exit(0)
	# _allKeys = _allKeys[0: 92]
	_notUsed_key = openAndCheckUsedData_Single(_li, _allKeys, False)
	# _notUsed_key = []
	# _notUsed_key = get_testKeys(_notUsed_key)
	# _notUsed_key = _allKeys[0: 922]
	print("\n-------------------------\n\n")
	_atartCount = len(_notUsed_key)
	# _list_i = _list_i[0:20]
	print(_atartCount +  len(_list_i))
	_notUsed_key = openAndCheckUsedData_Process(_list_i, _notUsed_key, False, printProgress=True)
	print("\n-------------------------\n\n")
	print(len(_notUsed_key))
	for x in _notUsed_key:
		print(x)
	# print(_notUsed_key)
	# _notUsed_key = ['setting.channel.tabMyChannel', 'broadcast.create.set_photo_open']
	#删除 未使用的key
	# deleteKeysInINIFiles(s_ini_paths, _notUsed_key)
