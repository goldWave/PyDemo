# coding = utf-8

import os
from googletrans import Translator
import xlwt 

dir = "D:\\languageCache\\en-US.ini"
dir2 = "D:\\languageCache\\en-US_1.txt"
dir_trans_key = "D:\\languageCache\\translate_f.txt"
dir_trans_all = "D:\\languageCache\\translate_all.txt"
dir_excel = "D:\\languageCache\\Excel_test.xls"

def wirteToFile(_dir2, _list):
	with open(_dir2, 'w', encoding='utf-8') as fp:
		fp.truncate()
		fp.writelines(_list)


class JBTrans(object):
	"""docstring for JBTrans"""
	def __init__(self):
		super(JBTrans, self).__init__()
		
		self._list=[]
		self._allOriginal=""

	def getValue(self):
		with open (dir, 'r', encoding='UTF-8') as f:
			lines = f.readlines()
			self._allOriginal = lines
			for line in lines:
				# a = line.decode()
				_ma = line.split("=\"")
				if len(_ma) > 1:
					origin = "\"" + _ma[1];
					self._list.append(origin)

	def replaceKey(self):
		if not os.path.exists(dir_trans_key):
			print("not contain transltate key file return")
			return

		with open(dir_trans_key, 'r', encoding='UTF-8') as f:
			_keyLines = f.readlines()
			with open(dir_trans_all, 'w', encoding='utf-8') as fAll:
				i = 0
				for v in self._allOriginal:
					_ma = v.split('="')
					if len(_ma) > 1:
						lineString = _ma[0] + "=" + _keyLines[i]
						fAll.write(lineString)
						print(lineString)
						i=i+1
					else:
						fAll.write(v)

#not complect method, becaues this third libiary have bugs.
	def transKeys(self):
		translator = Translator()
		# tr = translator.translate((['The quick brown fox', 'jumpsover', 'the lazy dog'], dest='zh')
		# translations = translator.translate("jimbo", dest='zh-cn')
		# translations = translator.translate(_keyLines, dest='zh-cn')
		_a = ""
		with open(dir2, 'r', encoding='UTF-8') as f:
			_keyLines = f.readlines()
			for x in _keyLines:
				x = x.strip("\n")
				_a = _a + x;
		# _a = ",".join(_keyLines)
		# print(_a)
		_a = _a.replace("\n", "")
		_a = '"Encoding overloaded! Consider turning down video settings or using a faster encoding preset.""Encoding"'
		translations = translator.translate(_a, dest='zh-cn')
		print(translations.text)

	def createExcel(self):
		if os.path.exists(dir_excel):
			os.remove(dir_excel)

		# 创建一个workbook 设置编码
		workbook = xlwt.Workbook(encoding = 'utf-8')
		# 创建一个worksheet
		worksheet = workbook.add_sheet('My Worksheet')

		# 写入excel
		# 参数对应 行, 列, 值
		index = 0;
		for line in self._allOriginal:
			# a = line.decode()
			_ma = line.split("=\"")
			if len(_ma) > 1:
				origin = "\"" + _ma[1];
				worksheet.write(index,0, label = _ma[0])
				worksheet.write(index,1, label = origin)
				index = index + 1

		worksheet.col(0).width = 256 * 20
		worksheet.col(1).width = 256 * 200

		# 保存
		workbook.save(dir_excel)

if __name__ == '__main__':
	classTr = JBTrans()
	classTr.getValue()
	# wirteToFile(classTr.dir2, classTr._list)
	# classTr.transKeys()
	classTr.createExcel()


