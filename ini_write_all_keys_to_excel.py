r"""
将所有ini文件 的key value 混合比对 写进 excel 文件

"""

import os,glob
from ini_common_method import *


s_ini_paths_only = ["en-US.ini", "ja-JP.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini"]
# dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale\\"
s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
# s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

def writeDiffToExcel(_path =s_ini_paths , _excel_name = "language"):
	#多个ini 互相比较，将 差异 的地方输出到 excel
	global _set
	_name = ["KEYS"]
	for x in _path:
		_name.append(x.split("\\")[-1])
		_set.add(x.split("\\")[-1])	_dics = []

	for x in _path:
		_dics.append(getINIKeyValuesDict(x))
	_mores = [_dic.keys() for _dic in _dics]
	writeCompareKeyToExcel("D:\\py_T\\" + _excel_name + ".xls", _name, _mores, _dics, _isWriteAll=True)

if __name__ == '__main__':

	# _list =  findAllCheckFile_inis("C:\\Users\\Administrator\\source\\PRISMLiveStudio\\")
	_list =  findAllCheckFile_inis("C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale\\")
	_set = set()
	for name, path in _list:
		_paths = [path+"\\" + x for x in s_ini_paths_only]
		writeDiffToExcel(_paths, name)
	# print(_set)