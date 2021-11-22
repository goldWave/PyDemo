# coding = utf-8

import xlrd, os, xlwt
import ini_common_method
from ini_common_method import iniData 

import sys
import io
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='utf8')

# dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
# dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale\\"
# s_key_paths = [{"en-US.ini":"en-US.ini"},{"ko-KR.ini":"ko-KR.ini"},{"id-ID.ini":"id-ID.ini"},{"pt-BR.ini":"pt-BR.ini"},{"ja-JP.ini":"ja-JP.ini"}]
s_ini_paths_only = ["en-US.ini", "ko-KR.ini","es-ES.ini"]

# s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]


def getDicKey(_dic) -> str:
	for k in _dic:
		return k
	return ""


def addValueToModel(model:iniData, _key, _value, _path):
	vStr = iniData.getKeyByPath(_path)
	if not hasattr(model, vStr):
		return
	setattr(model, vStr, _value)



def getIniFileModels(path):
	_dics = list()
	for x in s_ini_paths_only:
		_l  = ini_common_method.getINIKeyValuesDict(path + x, _isRemoveN=True)
		# print(len(_l))
		for _key in _l:
			_isContain = False
			for _d in _dics :
				if _d.keyStr == _key:
					_isContain = True
					#添加已有的数据
					addValueToModel(_d, _key, _l[_key], x)
					break

			if _isContain == False:
				#创建新数据
				_data = iniData()
				_data.s_path = path
				_data.keyStr = _key
				addValueToModel(_data, _key, _l[_key], x)
				_dics.append(_data)
	return _dics

def copyDataToIni(ini, ex):
	# if '##NICKNAME##' in ex.s_es_ES:
	# 	iniData.printFormateData(ini)
	# 	iniData.printFormateData(ex)
	# 	print("--------\n\n")
	# if '미성년자 구매불가' in ex.s_es_ES:
	# 	iniData.printFormateData(ini)
	# 	iniData.printFormateData(ex)
	# 	print("--------\n\n")
	ini.s_es_ES = ex.s_es_ES
	ex.b_isChanged = True
	ini.s_path = ex.s_path
	ini.s_sheet = ex.s_sheet

def combineTwoModels():
	global _inis
	global _models
	#将excel 生成的数组 匹配到  ini 生成的数据模型中
	for ini in _inis:
		for ex in _models:
			if len(ex.keyStr) > 0 and ini.keyStr == ex.keyStr:
				copyDataToIni(ini, ex)
			elif (ini.s_en_US == ex.s_en_US and ini.s_ko_KR == ex.s_ko_KR) and (len(ini.s_en_US.strip()) > 0 and len(ini.s_ko_KR.strip()) > 0):
				copyDataToIni(ini, ex)
			elif ini.s_en_US == ex.s_en_US and len(ini.s_en_US.strip()) > 0:
				copyDataToIni(ini, ex)
			elif ini.s_ko_KR == ex.s_ko_KR and len(ini.s_ko_KR.strip()) > 0:
				copyDataToIni(ini, ex)

def writeDuplicateKeyTo_excel(_dir, _list):

	if os.path.exists(_dir):
		os.remove(_dir)

	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('Error')

	st_orange_center = xlwt.easyxf('pattern: pattern solid;')
	st_orange_center.pattern.pattern_fore_colour = 51 #51 是橘黄色
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_orange_center.alignment = alignment
	_allIndex = 0

	worksheet.write(_allIndex, 0, "key")
	worksheet.write(_allIndex, 1, "en")
	worksheet.write(_allIndex, 2, "kr")
	worksheet.write(_allIndex, 3, "es")
	worksheet.write(_allIndex, 4, "path")
	worksheet.write(_allIndex, 5, "sheet")


	for x in _list:
		for y in x:
			_allIndex = _allIndex+1
			worksheet.write(_allIndex, 0, y.keyStr)
			worksheet.write(_allIndex, 1, y.s_en_US)
			worksheet.write(_allIndex, 2, y.s_ko_KR)
			worksheet.write(_allIndex, 3, y.s_es_ES)
			worksheet.write(_allIndex, 4, y.s_path)
			worksheet.write(_allIndex, 5, y.s_sheet)
		_allIndex = _allIndex+1
		for i in range(0, 6):
			worksheet.write(_allIndex, i, "", st_orange_center)

	workbook.save(_dir)

def logDiffModelInExcel():
	global _models
	_list = []
	t = 0
	for i in range(0, len(_models)):
		item1 = _models[i]
		for y in range(i, len(_models)):
			item2 = _models[y]
			if len(item2.s_en_US) > 0 or len(item2.s_ko_KR) > 0:
				if item2.s_en_US == item1.s_en_US and item2.s_ko_KR == item2.s_ko_KR:
					if item2.s_es_ES != item1.s_es_ES:
						# iniData.printFormateData(item1)
						# iniData.printFormateData(item2)
						_list.append([item1, item2])
						# t = t + 1
						# print("------\n\n\n\n")

	# print(len(_list))
	# print(t)
	writeDuplicateKeyTo_excel(R"C:\Users\Administrator\Desktop\error.xls", _list)


def logTotalCount():
	global _inis
	global _models
	total1 = 0
	totalex = 0
	for ini in _inis:
		if len(ini.s_es_ES) <= 0 or ini.s_es_ES == ini_common_method.s_str_replace:
			total1 = total1 + 1

	for ex in _models:
		# if len(ex.s_es_ES) > 0:
		if ex.b_isChanged == False:
			totalex = totalex + 1

	print("init all count: %d \t not found count:%d" %(len(_inis), total1))
	print("ex all count: %d \t found count:%d" %(len(_models), totalex))

if __name__ == '__main__':
	
	paths = ["C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-background-template-source\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-bgm-plugins\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-filter\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-mobile-source\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-mobile-source-api\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-monitor-capture\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-spectralizer\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-sticker-source\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-timer-source\\data\\locale\\",
	"C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\plugins\\prism-x265\\data\\locale\\"]

	for path in paths:
		engIni = path+ "en-US.ini"
		if not os.path.exists(path):

			continue
		if not os.path.exists(engIni):
			print(engIni)
			continue

		_inis = getIniFileModels(path)

		#或者excel 生成的数据模型
		excelsFiles = [R'D:\Download\102_[PRISM PC] 2.8.0 西班牙语翻译文档分享 _211019\프리즘pc 스페인어 번역_{0}.xlsx'.format(x) for x in range(1, 13)]
		_models = ini_common_method.getAllKeyValueFromExcel(excelsFiles)
		# ini_common_method.writeModelValuesToExcel(R"C:\Users\Administrator\Desktop\allkeys.xls", _models)
		# break
		combineTwoModels()

		_es_path = path + "es-ES.ini"
		ini_common_method.writeINIKeyToIniWithModel(_es_path, _inis,isOverwrite = True)
		logTotalCount()

	# logDiffModelInExcel()


