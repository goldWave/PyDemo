# coding = utf-8

import os,glob
from ini_common_method import *

# s_ini_paths_only = ["en-US.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini", "ja-JP.ini"]
dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
# s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

def check_dup():
	""" 
	检查 ini 文件是否存在相同的 Value
	"""

	def _isCoantain_key(_lists, _key):
		for x in _lists:
			for _sub in x:
				if _sub == _key:
					return True
		return False

	_dupKeys = []
	_originValue = []

	for x in s_ini_paths:
		# print("\n\n\n\n\n" +x + "\n -----\n")
		_lists = getINIKeyValues(x, _isRemoveN=True)
		_originValue.append(_lists)
		if x.endswith('en-US.ini') == False:
			continue
		_isEnEntered = True
		_keys = _lists[0]
		_values = _lists[1]

		
		for i in range(0,len(_values)):
			if _isCoantain_key(_dupKeys, _keys[i]):
				continue
			_i_value = _values[i].replace("\n", '').replace(' ', '')
			_addSet = set()
			for j in range(i+1,len(_values)):
				_j_value = _values[j].replace("\n", '').replace(' ', '')
				if _i_value == _j_value:
					_addSet.add(_keys[i])
					_addSet.add(_keys[j])
			if len(_addSet) != 0:
				_dupKeys.append(sorted(_addSet))
	# for x in _dupKeys:
	# 	print(x)
		# print("\n")

	_names = ["KEYS"]
	for x in s_ini_paths:
		_names.append(x.split("\\")[-1])

	if len(_dupKeys) == 0:
		print("没有 重复的 value， 不需要修改")
		return
	writeDuplicateValuesToExcel('D:\\py_T\\duplicate_values.xls', _names, _dupKeys, _originValue)
	# print(_originValue[0][1])


if __name__ == '__main__':
	# check_Double_quotes()
	check_dup()