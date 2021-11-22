# coding = utf-8

r"""
将所有ini文件 的key 的差异性 写进 excel 文件

"""

from ini_common_method import *
import os,glob

s_ini_paths_only = ["en-US.ini", "ja-JP.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini"]
# s_ini_paths_only = ["en-US.ini","ja-JP.ini"]

dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
# s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
# s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

def compare(_base, _list) -> list:
	_more = list()
	if len(_list) < 0:
		print("count is incorrect, exit")
		return []

	_allCount = len(_list)
	for _baseKey in _base:
		_count = 0;
		for _subList in _list:
			for _subKey in _subList:
				if _baseKey == _subKey:
					_count = _count + 1
					break
		if _count != _allCount:
			_more.append(_baseKey)
	return _more

	
def CheckDiff(_paths) -> list:
	_allKeys = list()
	for x in _paths:
		_allKeys.append(getINIKeys(x))

	_mores = list()
	for x in _allKeys:
		_mores.append(compare(x, _allKeys))

	return _mores

def writeDiffToExcel(_paths, _name):
	#多个ini 互相比较，将 差异 的地方输出到 excel
	_mores = CheckDiff(_paths)
	_names = ["KEYS"]
	for x in _paths:
		_names.append(x.split("\\")[-1])
	_dics = list()

	for x in _paths:
		_dics.append(getINIKeyValuesDict(x))
		# print(_dics)
		# print(x)

	writeCompareKeyToExcel("D:\\py_T\\compare_language_" +  _name + ".xls", _names, _mores, _dics, _isContainIgnore=True)

def checkMoreParam(_paths, _name):
	#多个ini 互相比较，检查 %1 %2 数量是否相同
	_names = []
	for x in _paths:
		_names.append(x.split("\\")[-1])

	_dics = list()
	for x in _paths:
		_dics.append(getINIKeyValuesDict(x))

	_isPrintFile = False
	_checkString = ['%1', '%2', '%3','%4','%5']
	_fromIndex = 0
	_i_keys = _dics[_fromIndex].keys()
	for j in range(0,len(_dics)):	
		_isCo = False
		for i_key in _i_keys:	
			if i_key in _dics[j].keys():
				for _subStr in _checkString:
					if not _subStr in _dics[_fromIndex][i_key]:
						continue
					if not _subStr  in _dics[j][i_key]:
						if _isPrintFile == False:
							print("\n\n\n" + _paths[0].replace(_names[0],''))
							_isPrintFile = True
						if _isCo == False:
							print("\n" + _names[_fromIndex]+ "   compare " + _names[j])
							_isCo = True
						print(_subStr + " missing---------- "+ i_key)
		

def removeMoreEnglishKey():
	#和english 比较，将多出的字符串删除掉
	_mores = CheckDiff(s_ini_paths)
	# print(_mores[1])
	_del = s_ini_paths[1]
	deleteKeysInINIFiles([_del], _mores[1])

if __name__ == '__main__':

	# writeDiffToExcel()
	# removeMoreEnglishKey()

	_list =  findAllCheckFile_inis("C:\\Users\\Administrator\\source\\PRISMLiveStudio\\")
	# _list =  findAllCheckFile_inis(dir_common_pre)
	_set = set()
	# print(_list)
	for name, path in _list:
		_paths = [path+"\\" + x for x in s_ini_paths_only]
		# writeDiffToExcel(_paths, name)
		
		checkMoreParam(_paths, name)

