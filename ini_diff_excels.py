from ini_common_method import *
import os,glob


if __name__ == '__main__':


	_list_1 = getAllKeyValueFromExcel("C:\\Users\\Administrator\\Desktop\\xin.xlsx")
	_list_2 = getAllKeyValueFromExcel("C:\\Users\\Administrator\\Desktop\\yuanwejian.xlsx")
	

	def get_subList(_key):
		for _subList in _list_2:
			if _subList[0] == _key:
				return _subList
		return []

	print("以下是 xin 多出来的")
	for _subList in _list_1:
		_getList = get_subList(_subList[0])
		if len(_getList) == 0:
			print(str(_subList[0]) + "       是多余的")
			continue
		# print("\n")
		for i in range(1, len(_subList)):
			if _subList[i] != _getList[i]:
				print(str(_subList[0]) + "    不相同")

		_list_2.remove(_getList)

	print("\n\n以下是 yuanwejian 多出来的")
	for x in _list_2:
		print(x[0])
