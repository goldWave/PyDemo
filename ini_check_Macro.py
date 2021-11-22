# coding = utf-8

import os
from ini_common_method import findAllCheckFile
from ini_common_method import openAndCheckUsedData
from ini_common_method import removeMacroFileNotUsedKey

s_macro_file = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\pls-common-language.hpp"

def get_macro_key(dir) -> list:
	"""传入路径，获取key所定义的宏的列表"""
	with open (dir, 'r', encoding='UTF-8') as f:
		lines = f.readlines()
		_list = list()
		for line in lines:
			if not line.startswith("#define "):
				continue
			_ma = line.replace("#define ","")
			_ma = _ma.split(" ")
			if len(_ma) > 1:
				_list.append(_ma[0])
		return _list

			

class CheckMacro(object):
	"""docstring for CheckMacro"""
	def __init__(self, arg):
		super(CheckMacro, self).__init__()
		self.arg = arg

		self._allList = get_macro_key(self.arg)


if __name__ == '__main__':
	c_check = CheckMacro(s_macro_file)
	_li = findAllCheckFile()
	_li.remove(s_macro_file)

	_notUsed_key = openAndCheckUsedData(_li, c_check._allList, True)
	removeMacroFileNotUsedKey(s_macro_file, _notUsed_key)

