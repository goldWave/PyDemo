import xlrd, os
from ini_common_method import getKeyValueFromExcel
from ini_common_method import writeINIKeyToExistFile

dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale"
# dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale"
# s_key_paths = [{"EN":"en-US.ini"},{"KR":"ko-KR.ini"},{"ID":"id-ID.ini"},{"PT":"pt-BR.ini"},{"JP":"ja-JP.ini"}]
s_key_paths = [{"en-US.ini":"en-US.ini"},{"ko-KR.ini":"ko-KR.ini"},{"id-ID.ini":"id-ID.ini"},{"pt-BR.ini":"pt-BR.ini"},{"ja-JP.ini":"ja-JP.ini"}]
# s_key_paths = [{"일본어":"ja-JP.ini"}]
s_excelPath = "D:\\Download\\works\\2.7.0 번역_0702.xlsx"

def getDicKey(_dic) -> str:
	for k in _dic:
		return k
	return ""

if __name__ == '__main__':
	for _index in range(len(s_key_paths)):
		print(_index)
		_name = getDicKey(s_key_paths[_index])
		# _dic = getKeyValueFromExcel(s_excelPath, "2.7.0 번역", _name)
		_dic = getKeyValueFromExcel(s_excelPath, "Sheet1", _name)

		# print(_dic)
		print("\n\n\n\n")
		_path = dir_common_pre + '\\' + s_key_paths[_index][getDicKey(s_key_paths[_index])]
		# print(_path)
		writeINIKeyToExistFile(_path, _dic)

