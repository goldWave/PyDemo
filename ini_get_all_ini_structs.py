r"""
将所有ini文件 的key value 混合比对 写进 excel 文件

"""

import os,glob
from ini_common_method import *

s_ini_paths_only = ["en-US.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini","es-ES.ini"]
dir_common_pre = "C:\\Users\\Administrator\\Documents\\source\\PRISMLiveStudio\\src\\"
# dir_common_pre = "C:\\Users\\Administrator\\Documents\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale\\"

s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
# s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

#获取所有文件夹的所有 ini

def getSubDirInis(_path =s_ini_paths) -> list:

	_models = list()
	for _subPath in _path: #子文件夹的所有ini文件
		_dic = getINIKeyValuesDict(_subPath)
		for (k,v) in _dic.items(): #单ini文件的所有key value
			_runKey = iniData.getKeyByPath(_subPath)  #key
			_isFound = False
			for _subModel in _models:
				if _subModel.keyStr == k:
					_subModel.keyStr = k
					setattr(_subModel, _runKey, v)
					_isFound = True
					break
			if _isFound == False:
				_subModel = iniData()
				_subModel.keyStr = k
				setattr(_subModel, _runKey, v)
				_models.append(_subModel)
	return _models


def getAllDirInis(_path =s_ini_paths) -> list:
	_list =  findAllCheckFile_inis(dir_common_pre)
	_set = set()
	_iniDatas = list()
	for name, path in _list:
		_paths = [path+"\\" + x for x in s_ini_paths_only]
		# print(_paths)
		_subs = getSubDirInis(_paths)
		for x in _subs:
			_iniDatas.append(x)
			
	print("iniKeys:", len(_iniDatas))
	return _iniDatas

if __name__ == '__main__':

	getAllDirInis()