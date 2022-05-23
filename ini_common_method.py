# coding = utf-8

import os, time
from time import ctime, sleep
import threading
import xlrd
import xlwt
import multiprocessing as mp

s_str_replace = "检测替换"

dir_cache_path = 'C:\\Users\\Administrator\\Documents\\source\\cache\\'
dir_all_file = dir_cache_path + "all_file.txt"
dir_i_file = dir_cache_path + "i_file.txt"
dir_ignore_file = dir_cache_path + "ignore_excel_keys.txt"

dir_all_alart_lines = dir_cache_path + "alert_lines.txt"
dir_all_check_alart_lines = dir_cache_path + "check_alert_lines.txt"

dir_checked = "C:\\Users\\Administrator\\Documents\\source\\PRISMLiveStudio\\src\\prism"

s_common_key_paths = [{"en-US.ini":"en-US.ini"},{"ko-KR.ini":"ko-KR.ini"},{"id-ID.ini":"id-ID.ini"},{"pt-BR.ini":"pt-BR.ini"},{"ja-JP.ini":"ja-JP.ini"},{"es-ES.ini":"es-ES.ini"}]
s_common_ini_paths_only = ["en-US.ini", "ja-JP.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini","es-ES.ini"]

class iniData:
	s_path = str()
	s_sheet = str()
	keyStr = str()
	s_en_US = str()
	s_ko_KR = str()
	s_id_ID = str()
	s_pt_BR = str()
	s_ja_JP = str()
	s_es_ES = str()
	b_isChanged = False
	i_dupCount = 0

	def printFormateData(x):
		# print("key: %s \t s_en_US: %s \t s_ko_KR: %s \t s_es_ES: %s" %(x.keyStr, x.s_en_US, x.s_ko_KR, x.s_es_ES) )
		print("key: %s \t s_en_US: %s \t s_ko_KR: %s \t s_es_ES: %s  path:%s \t sheet:%s" %(x.keyStr, x.s_en_US, x.s_ko_KR, x.s_es_ES, x.s_path, x.s_sheet) )

		# print("key: %s \t s_en_US: %s \t s_ko_KR: %s \t s_es_ES: %s" %(keyStr, s_en_US, s_ko_KR, s_es_ES) )
	
	def getKeyByPath(_path):
		vStr = str()
		if (_path.endswith("en-US.ini")) :
			vStr = 's_en_US'
		elif (_path.endswith("ko-KR.ini")) :
			vStr = 's_ko_KR'
		elif (_path.endswith("id-ID.ini")) :
			vStr = 's_id_ID'
		elif (_path.endswith("pt-BR.ini")) :
			vStr = 's_pt_BR'
		elif (_path.endswith("es-ES.ini")) :
			vStr = 's_es_ES'
		return vStr

def findAllCheckFile_i() -> list:
	""" 获取所有的 cpp h 之类的文件列表 """
	_allFiles = list()
	if os.path.exists(dir_i_file):
		with open(dir_i_file, 'r', encoding='utf-8') as f:
			allLines = f.readlines()
			for x in allLines:
				x = x.strip('\n')
				_allFiles.append(x)
		return _allFiles

	index = 0
	for root, lists, files in os.walk(dir_checked):
		for file in files:
			if os.path.splitext(file)[1] in ['.i']:
				# print(root + "=====" + file)
				_allFiles.append(root+"\\"+file)

	with open(dir_i_file, 'w', encoding='utf-8') as fp:
		fp.truncate()
		for x in _allFiles:
			fp.write(x)
			fp.write('\n')

	return _allFiles

def findAllCheckFile() -> list:
	""" 获取所有的 .i 之类的文件列表 """
	_allFiles = list()
	if os.path.exists(dir_all_file):
		with open(dir_all_file, 'r', encoding='utf-8') as f:
			allLines = f.readlines()
			for x in allLines:
				x = x.strip('\n')
				_allFiles.append(x)
		return _allFiles

	index = 0
	for root, lists, files in os.walk(dir_checked):
		for file in files:
			if os.path.splitext(file)[1] in ['.h','.hpp','.c','.cpp', '.ui', '.css', '.qss'] and file.startswith('moc') == False and file.startswith('qrc') == False:
				# print(root + "=====" + file)
				_allFiles.append(root+"\\"+file)

	with open(dir_all_file, 'w', encoding='utf-8') as fp:
		fp.truncate()
		for x in _allFiles:
			fp.write(x)
			fp.write('\n')

	return _allFiles

def getINIKeys(dir) -> list:
	""" 获取所有的  ini 文件的key 列表"""
	if os.path.exists(dir) == False:
		return []
	with open (dir, 'r', encoding='UTF-8') as f:
		lines = f.readlines()
		_list = list()
		for line in lines:
			_ma = line.split("=\"")
			if len(_ma) > 1:
				# origin = "\"" + _ma[1];
				# _dict[_ma[0]] = origin
				_list.append(_ma[0])
		return _list

def getINIKeyValues(dir, _isRemoveN = False) -> list:
	""" 
	获取所有的  ini 文件的key value 的双重数组
	param:_isRemoveN 是否移除结尾的换行和 首尾的 双引号
	"""
	_keys = list()
	_values = list()
	if os.path.exists(dir) == False:
		return [], []
		
	with open (dir, 'r', encoding='UTF-8') as f:
		lines = f.readlines()
		for line in lines:
			_ma = line.split("=\"")
			if len(_ma) > 1:
				_keys.append(_ma[0])
				if _isRemoveN == True:
					_values.append(get_origin_str(_ma[1]))
				else:
					_values.append("\"" + _ma[1])
	return _keys, _values

def getINIKeyValuesDict(dir, _isRemoveN = False) -> dict:
	if os.path.exists(dir) == False:
		return {}

	""" 获取所有的  ini 文件的key value 的 字典"""
	_lists = getINIKeyValues(dir, _isRemoveN=_isRemoveN)
	_keyValueDict = {}
	_keys = _lists[0]
	_values = _lists[1]
	for i in range(0,len(_keys)):
		_value = _values[i]
		# _value = _value.replace(u'\xa0', u' ')
		_keyValueDict[_keys[i]] = _value
	return _keyValueDict

def openAndCheckUsedData_Single(fileList, keyList, isMacro=False, printProgress=False) -> list:
	"""
	fileList = 所有文件的路径
	keyList = 查找的key
	isMacro = key 是否是宏
	return 没有使用的key
	"""
	keyDic = {}
	for x in keyList:
		keyDic[x] = 0
		
	def threadOpen(_file, isMacro, printProgress):
		global _index
		global allCount
		# sem.acquire()
		if printProgress == True:
			print(_file)
		key_channel_header = 'Channels.'
		t0 = time.time()
		print(_file)
		if 'src\\prism\\sub\\cam-effect\\src\\jsonWrapper\\cjson' in _file:
			return
		with open(_file, 'r', encoding='utf-8') as f:
			allLine = f.readlines()
			strLine = ",".join(allLine)
			strLine = strLine.replace('" "', '');
			word_b = set(strLine.split())
			for _key in keyDic:  #800 * 3
				# t0 = time.time()
				if keyDic[_key] > 0:
					continue
				if isMacro:
					if _key in strLine:
						keyDic[_key] = keyDic[_key] + 1
				else:
					_copyKey = _key
					if _copyKey.startswith("key_channel_header") and ('CHANNELS_TR(' + _copyKey.replace(key_channel_header,'') + ')') in strLine:
						keyDic[_key] = keyDic[_key] + 1
						# "key" or  <string>key</string> or \"key\"
					elif _key in strLine:
						if ('"' + _key + '"' in strLine) or ('<string>'+_key+'</string>' in strLine) or ('\"'+_key+'\"' in strLine):
							keyDic[_key] = keyDic[_key] + 1
		# if printProgress == True:
		# 	t1 = time.time()
		# 	print(str((t1-t0)*1000) + " ms")


	_index = 1
	for _file in fileList:
		threadOpen(_file, isMacro, printProgress)

	_fileList = []	
	for _key in keyDic:
		if keyDic[_key] == 0:
			_fileList.append(_key)		
	return _fileList.copy()

def openAndCheckUsedData(fileList, keyList, isMacro=False, printProgress=False) -> list:
	"""
	fileList = 所有文件的路径
	keyList = 查找的key
	isMacro = key 是否是宏
	return 没有使用的key
	"""
	keyDic = {}
	for x in keyList:
		keyDic[x] = 0
	
	# allCount = len(fileList)
	
	def threadOpen(_file, isMacro, printProgress):
		global _index
		global allCount
		sem.acquire()
		if printProgress == True:
			print(_file)
		key_channel_header = 'Channels.'

		# print('DONE AT--start:', ctime())
		with open(_file, 'r', encoding='utf-8') as f:
			if printProgress == True:
				print(_file + "\t"+ str(threading.get_ident()))
			allLine = f.readlines()
			strLine = ",".join(allLine)
			strLine = strLine.replace('" "', '');
			# print('DONE AT--join:', ctime())
			for _key in keyDic:
				if keyDic[_key] > 0:
					continue
				if isMacro:
					if _key in strLine:
						lock.acquire()
						keyDic[_key] = keyDic[_key] + 1
						lock.release()
				else:
					_copyKey = _key
					if _copyKey.startswith("key_channel_header") and ('CHANNELS_TR(' + _copyKey.replace(key_channel_header,'') + ')') in strLine:
						lock.acquire()
						keyDic[_key] = keyDic[_key] + 1
						lock.release()
					elif _key in strLine:
						if ('"' + _key + '"' in strLine) or ('<string>'+_key+'</string>' in strLine) or ('\"'+_key+'\"' in strLine):
							lock.acquire()
							keyDic[_key] = keyDic[_key] + 1
							lock.release()
		sem.release() 

	sem=threading.Semaphore(8)
	lock=threading.Lock()   #将锁内的代码串行化
	_index = 1
	l=[]
	for _file in fileList:
		t=threading.Thread(target=threadOpen,args=(_file,isMacro,printProgress,))
		t.start()
		l.append(t)

	for t in l:
		t.join()

	_fileList = []	
	for _key in keyDic:
		if keyDic[_key] == 0:
			_fileList.append(_key)		
	return _fileList.copy()

def threadOpen_1(_file, isMacro, printProgress, keyDic, lock):
		# sem.acquire()
		# if printProgress == True:
		# print(_file)
		key_channel_header = 'Channels.'

		with open(_file, 'r', encoding='utf-8') as f:
			if printProgress == True:
				print(_file + "\t"+ str(threading.get_ident()))
			allLine = f.readlines()
			strLine = ",".join(allLine)
			strLine = strLine.replace('" "', '');
			# print('DONE AT--join:', ctime())
			for _key in keyDic.keys():
				if keyDic[_key] > 0:
					continue
				if isMacro:
					if _key in strLine:
						lock.acquire()
						keyDic[_key] = keyDic[_key] + 1
						lock.release()
				else:
					_copyKey = _key
					if _copyKey.startswith("key_channel_header") and ('CHANNELS_TR(' + _copyKey.replace(key_channel_header,'') + ')') in strLine:
						lock.acquire()
						keyDic[_key] = keyDic[_key] + 1
						lock.release()
					elif _key in strLine:
						if ('"' + _key + '"' in strLine) or ('<string>'+_key+'</string>' in strLine) or ('\"'+_key+'\"' in strLine):
							lock.acquire()
							# print("-------" + _key)
							keyDic[_key] = keyDic[_key] + 1
							lock.release()
		# sem.release()

def openAndCheckUsedData_Process(fileList, keyList, isMacro=False, printProgress=False) -> list:
	"""
	fileList = 所有文件的路径
	keyList = 查找的key
	isMacro = key 是否是宏
	return 没有使用的key
	这里主要的 耗时在 大字符串 搜索 子字符串里面，是cpu 密集型，所有用多进程
	而python 的锁导致多线程 访问cpu需要串行，所有多线程并没有进行时间优化
	"""
	_keyDic = {}
	for x in keyList:
		_keyDic[x] = 0
	
	p = mp.Pool(mp.cpu_count()*2)
	m = mp.Manager()
	dic=m.dict(_keyDic)
	_lock = m.Lock()

	for _file in fileList:
		p.apply_async(threadOpen_1,args=(_file,isMacro,printProgress,dic, _lock,))

	p.close()
	p.join()

	_fileList = []	
	for _key in dic:
		if dic[_key] == 0:
			_fileList.append(_key)
	return _fileList.copy()


def removeMacroFileNotUsedKey(_path, keyList):
	"""传入宏文件路径，和 需要删除的宏key"""

	def _isCoantainKey(line, key) -> bool:
		if line.startswith("#define "):
			_ma = line.replace("#define ","")
			_ma = _ma.split(" ")
			if len(_ma) > 1:
				if _ma[0] == key:
					return True
		return False

	with open (_path, 'r+', encoding='UTF-8') as f:
		lines = f.readlines()
		_list = list()
		f.seek(0)
		f.truncate()

		for line in lines:
			_isContain = False
			for key in keyList:
				if _isCoantainKey(line, key):
					_isContain = True
					break
			if _isContain == True:
				continue

			f.write(line)	

def deleteKeysInINIFiles(fileList, keyList):
	"""
	fileList = 所有文件的路径
	keyList = 删除的key
	"""

	def _isCoantainKey(line, key) -> bool:
		_ma = line.split("=\"")
		if len(_ma) > 1:
			if _ma[0] == key:
				return True
		return False

	for file in fileList:
		with open(file, 'r+', encoding='utf-8') as f:
			lines = f.readlines()
			f.seek(0)
			f.truncate()

			for line in lines:
				_isContain = False
				for key in keyList:
					if _isCoantainKey(line, key):
						_isContain = True
						break
				if _isContain == True:
					continue

				f.write(line)


def getKeyValueFromExcel(_ex_path, _sheetName, _ValueKey, _keyName="KEY") -> dict:
	""" 
	获取 excel  表的键值对
	_ex_path： excel 路径
	_sheetName： sheet naame
	_ValueKey： 需要取值的value 的第一行名字
	_keyName： key 的第一行名字
	"""
	# print(_ex_path)
	workbook = xlrd.open_workbook(_ex_path)
	sheet1_object = workbook.sheet_by_name(sheet_name=_sheetName)
	
	# 获取sheet1中的有效行数
	nrows = sheet1_object.nrows
	_backDic = dict()
	# 获取sheet1中的有效列数
	ncols = sheet1_object.ncols
	_keyIndex = -1
	_valueIndex = -1
	for _clos in range(0,ncols):
		cell_info = sheet1_object.cell_value(rowx=0, colx=_clos)
		if cell_info == _keyName:
			_keyIndex = _clos
		elif cell_info == _ValueKey:
			_valueIndex = _clos


	if _keyIndex == -1 or _valueIndex == -1:
		print("-------------error  index not found--------------")
		return _backDic

	for _index in range(1,nrows):
		_key = sheet1_object.cell_value(rowx=_index, colx=_keyIndex)
		_value = sheet1_object.cell_value(rowx=_index, colx=_valueIndex)
		if _key == "" or _value == "":
			continue
		_backDic[_key] = _value
	return _backDic


def convertListToModels(_list, exPath="excel", sheet="sheet1") -> list:
	if len(_list) <= 0:
		return []

	_first = _list[0]
	del(_list[0])
	_datas = list()

	for x in _list:
		model = iniData()
		model.s_path = exPath.split("\\")[-1]
		model.s_sheet = sheet
		_datas.append(model)
	# for x in _datas:
	# 	print(x.s_path)
	for index,value in enumerate(_first): #各个语言的列
		vStr = ""
		if value.lower().find('key') >= 0:
			vStr = "keyStr"
		elif value.lower().find('en') >= 0:
			vStr = "s_en_US"
		elif value.lower().find('kr') >= 0:
			vStr = "s_ko_KR"
		elif value.lower().find('스페인어') >= 0:
			vStr = "s_es_ES"

		# print(value + "\t" + vStr)
		if len(vStr) <= 0:
			continue

		tmp = iniData()
		if not hasattr(tmp, vStr):
			continue
		
		for i,v in enumerate(_list):
			setattr(_datas[i], vStr, v[index])

	# for _x in _datas:
	# 	iniData.printFormateData(_x)
	# for x in _datas:
	# 	print(x.s_path)
	return _datas


def getAllKeyValueFromExcel(_ex_paths : list, _sheetNames : list = []) -> list:
	""" 
	获取 excel 所有的值，以 list 包含元祖返回
	_ex_paths excel 路径
	_sheetNames sheet naame
	
	return initData 组成的数组
	"""
	_total = 0
	_list = []
	for _file in _ex_paths:
		# _subList = []
		workbook = xlrd.open_workbook(_file)
		_allSheetNames = workbook.sheet_names()

		for containSheetName in _allSheetNames:
			# containSheetName = str()
			# for x in _allSheetNames:
			# 	for v in _sheetNames:
			# 		if x == v:
			# 			containSheetName = v
			# 			break
			# if len(containSheetName) <= 0:
			# 	#说明这个文件不包含需要的sheet
			# 	continue

			sheet1_object = workbook.sheet_by_name(sheet_name=containSheetName)
			# 获取sheet1中的有效行数
			nrows = sheet1_object.nrows
			# 获取sheet1中的有效列数
			n_xs = sheet1_object.ncols
			_subOriginLists = []
			for _index in range(0,nrows):
				_subList = []
				for x in range(0, n_xs):
					_key = sheet1_object.cell_value(rowx=_index, colx=x)
					# print(_key)
					_subList.append(_key)
				_subOriginLists.append(_subList)
			_total = _total + len(_subOriginLists)
			_models = convertListToModels(_subOriginLists, exPath=_file, sheet=containSheetName)
			# print(" ncols:%d \t sheet:%s\texcel: %s" % (len(_subOriginLists), containSheetName, _file))
			
			for x in _models:
				_list.append(x)

			# if len(_subOriginLists) != len(_models):
			# 	print(" ncols:%d\t sheet:%s\texcel: %s" % (len(_subOriginLists), containSheetName, _file))

	# print("all origin data counts: %d   %d" % (len(_list), _total))
	return _list


def writeINIKeyToExistFile(dir, _dic):
	""" 
	将 key value 写进已经存在的 ini 文件中
	dir： ini 路径
	_dic： 需要写入的 key value 的字典
	"""
	with open (dir, 'r+', encoding='UTF-8') as f:
		lines = f.readlines()
		f.seek(0)
		f.truncate()
		for line in lines:
			_ma = line.split("=\"")
			# print(_ma)
			# print(len(_ma))
			if len(_ma) > 1:
				_key = _ma[0]
				_replaceValue = ""
				if _dic.__contains__(_key):
					_replaceValue = _dic[_key]
				
				if _replaceValue != "":
					# print(_key)
					line = _key + '="' + _replaceValue + '"\n'
					_dic.pop(_key)
				if _replaceValue.count('"') != _replaceValue.count('\\"'):
					print("value的双引号转义存在问题：" + _key + "=" + _replaceValuev)
			f.write(line)

		for k,v in _dic.items():
			line = k + '="' + v + '"\n'
			f.write(line)

			if v.count('"') != v.count('\\"'):
				print("value的双引号转义存在问题：" + k + "=" + v)


def writeINIKeyToIniWithModel(dir, _models, isOverwrite=False):
	""" 
	将 key value 写进已经存在的 ini 文件中, 如果不存在，会自动创建
	dir： ini 路径
	_models 需要写入的  ini model
	"""

	_runKey = iniData.getKeyByPath(dir)

	with open (dir, 'w+', encoding='UTF-8') as f:
		lines = f.readlines()
		f.seek(0)
		f.truncate()
		if isOverwrite == True:
			for item in _models:
				if len(item.keyStr) <= 0:
					continue

				_value = getattr(item, _runKey)
				if _value.count('"') != _value.count('\\"'):
					_value = _value.replace('\\"', '"')
					_value = _value.replace('"', '\\"')
					# print("value的双引号转义存在问题已修改：" + _value)
				if len(_value) == 0:
					_value = s_str_replace

				# if '##NICKNAME##' in _value:
				# 	iniData.printFormateData(item)
				# 	print("--------\n\n")

				line = item.keyStr + '="' + _value + '"\n'
				f.write(line)

def getExcelIgnoreKeys(_dir=dir_ignore_file) -> set:
	_list = set()
	if not os.path.exists(dir_ignore_file):
		return _list
	with open (_dir, 'r', encoding='UTF-8') as f:
		lines = f.readlines()
		for line in lines:
			if line.startswith('#') == False:
				_list.add(line.replace('\n',''))
	return _list

def writeCompareKeyToExcel(_dir, _names, _keys, _templateDics = [], _isWriteAll = False, _isContainIgnore=True):
	_ignoreKey = []
	if _isContainIgnore == False:
		_ignoreKey = getExcelIgnoreKeys()
	_subNames = _names[1:]
	# print(_subNames)
	if _isWriteAll == False:
		for i in _subNames:
			_names.append(i)

	_set = set()
	for x in _keys:
		for _subKey in x:
			_set.add(_subKey)
	if _isWriteAll == False:
		for x in _ignoreKey:
			if x in _set:
				_set.remove(x)

	_set = sorted(_set)
	print(len(_set))
	if len(_set) == 0:
		return
	# for x in _set:
	# 	print(x)
	if os.path.exists(_dir):
		os.remove(_dir)
	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('First')

	# 设置冻结窗口
	# 设置冻结为真
	worksheet.set_panes_frozen('1')
	# 水平冻结
	worksheet.set_horz_split_pos(1)
	# 垂直冻结
	worksheet.set_vert_split_pos(1)
	worksheet.col(0).width = 12000 

	# 写入excel
	# 参数对应 Y, X, 值
	_allIndex  = 0
	#写入所有 key
	_wirteDic = {}
	for x in _set:
		_allIndex = _allIndex+1
		worksheet.write(_allIndex,0, label = x)
		_wirteDic[str(_allIndex)] = str(x)
		
	st_white_center = xlwt.easyxf('pattern: pattern solid;')
	alignment = xlwt.Alignment()
	st_white_center.pattern.pattern_fore_colour = 1 #1 白色
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_white_center.alignment = alignment

	#写入 每列的 名字
	for i  in range(0,len(_names)):
		worksheet.write(0,i, _names[i], st_white_center)

		_width = 3000;
		if i == 0:
			_width = 10000

		if _isWriteAll == True and i != 0:
			_width = 12000
		else:
			if i >= len(_names) - len(_templateDics) :
				_width = 12000

		worksheet.col(i).width = _width

	def is_contain_key(_list, _key) -> bool:
		for x in _list:
			if x == _key:
				return True
		return False

	st_white_left = xlwt.easyxf()
	alignment = xlwt.Alignment()
	st_white_left.pattern.pattern_fore_colour = 1 #1 白色
	alignment.horz = xlwt.Alignment.HORZ_LEFT
	# alignment.wrap = 1 #自动换行
	st_white_left.alignment = alignment

	st_orange_center = xlwt.easyxf('pattern: pattern solid;')
	st_orange_center.pattern.pattern_fore_colour = 51 #51 是橘黄色
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_orange_center.alignment = alignment

	# Y轴
	for _index in range(1,_allIndex+1):
		#key 的字符串
		_key = _wirteDic[str(_index)]

		if _isWriteAll == True:
			# X轴
			for i in range(0,len(_templateDics)):
				_templateDic = _templateDics[i]
				if _key in _templateDic.keys():
					worksheet.write(_index, i + 1, get_origin_str(_templateDic[_key]), st_white_left)
				else:
					worksheet.write(_index, i + 1, "", st_orange_center)
			continue

		#取对应行数的key是否存在
		for i in range(0,len(_keys)):
			if is_contain_key(_keys[i], _key) == False:
				worksheet.write(_index,i+1, "X", st_orange_center)

		#添加英文和其他文字的的实际参考字符串
		for i in range(0,len(_templateDics)):
			_templateDic = _templateDics[i]
			if _key in _templateDic.keys():
				worksheet.write(_index, len(_keys) + i + 1, get_origin_str(_templateDic[_key]), st_white_left)

	badBG = xlwt.Pattern()
	badBG.pattern = badBG.SOLID_PATTERN
	badBG.pattern_fore_colour = 3

	badFontStyle = xlwt.XFStyle()
	badFontStyle.pattern = badBG
	# 保存Excel_test
	workbook.save(_dir)

def writeModelValuesToExcel(_dir, _list = [iniData]):
	if os.path.exists(_dir):
		os.remove(_dir)
	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('main')

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


	for y in _list:
		_allIndex = _allIndex+1
		worksheet.write(_allIndex, 0, y.keyStr)
		worksheet.write(_allIndex, 1, y.s_en_US)
		worksheet.write(_allIndex, 2, y.s_ko_KR)
		worksheet.write(_allIndex, 3, y.s_es_ES)
		worksheet.write(_allIndex, 4, y.s_path)
		worksheet.write(_allIndex, 5, y.s_sheet)
	workbook.save(_dir)

def writeDuplicateValuesToExcel(_dir, _names, _keys, _templateDics = []):

	for i in range(0,len(_templateDics)):
		_str = "str" + str(i)
		_names.append(_str)

	# for x in _set:
	# 	print(x)
	if os.path.exists(_dir):
		os.remove(_dir)
	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('First')

	# 设置冻结窗口
	# 设置冻结为真
	worksheet.set_panes_frozen('1')
	# 水平冻结
	worksheet.set_horz_split_pos(1)
	# 垂直冻结
	worksheet.set_vert_split_pos(1)
	_spaceStr = '----seprate------'

	st_green_center = xlwt.easyxf('pattern: pattern solid;')
	st_green_center.pattern.pattern_fore_colour = 30 #绿色
	# 写入excel
	# 参数对应 Y, X, 值
	_allIndex  = 0
	#写入所有 key
	_wirteDic = {}
	for x in _keys:
		for _key in x:
			_allIndex = _allIndex+1
			worksheet.write(_allIndex,0, label = _key)
			_wirteDic[str(_allIndex)] = str(_key)
		_allIndex += 1
		_wirteDic[str(_allIndex)] = _spaceStr
		worksheet.write(_allIndex, 0, "", st_green_center)
		worksheet.row(_allIndex).height_mismatch = True
		worksheet.row(_allIndex).height = 256*4

	st_white_center = xlwt.easyxf('pattern: pattern solid;')
	alignment = xlwt.Alignment()
	st_white_center.pattern.pattern_fore_colour = 1 #1 白色
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_white_center.alignment = alignment

	#写入 X轴第一排 的 名字
	for i  in range(0,len(_names)):
		worksheet.write(0,i, _names[i], st_white_center)
		if i == 0:
			_width = 8000
		else:
			_width = 10000

		worksheet.col(i).width = _width

	st_white_left = xlwt.easyxf()
	alignment = xlwt.Alignment()
	st_white_left.pattern.pattern_fore_colour = 1 #1 白色
	alignment.horz = xlwt.Alignment.HORZ_LEFT
	# alignment.wrap = 1 #自动换行
	st_white_left.alignment = alignment

	st_orange_center = xlwt.easyxf('pattern: pattern solid;')
	st_orange_center.pattern.pattern_fore_colour = 51 #51 是橘黄色
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_orange_center.alignment = alignment

	def getIndex(_lists, _key):
		for i in range(0,len(_lists)):
			if _lists[i] == _key:
				return i
		return -1

	# Y轴
	for _index in range(1, _allIndex+1):
		#key 的字符串
		_key = _wirteDic[str(_index)]
		# X轴
		for i in range(0,len(_templateDics)):
			_templateKeys = _templateDics[i][0]
			_templateValues = _templateDics[i][1]
			if _key in _templateKeys:
				worksheet.write(_index, i + 1, get_origin_str(_templateValues[getIndex(_templateKeys, _key)]), st_white_left)
			elif _key == _spaceStr:
				worksheet.write(_index, i + 1, "", st_green_center)
			else:
				worksheet.write(_index, i + 1, "", st_orange_center)

	badBG = xlwt.Pattern()
	badBG.pattern = badBG.SOLID_PATTERN
	badBG.pattern_fore_colour = 3

	badFontStyle = xlwt.XFStyle()
	badFontStyle.pattern = badBG
	# 保存Excel_test
	workbook.save(_dir)


def writeKeyNotUsed_excel(_dir, _allKeys, _notUsedKeys):
	if os.path.exists(_dir):
		os.remove(_dir)
	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('First')

	st_orange_center = xlwt.easyxf('pattern: pattern solid;')
	st_orange_center.pattern.pattern_fore_colour = 51 #51 是橘黄色
	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
	st_orange_center.alignment = alignment
	_allIndex = 0
	for _key in _allKeys:
		# for _key in x:
		_allIndex = _allIndex+1
		worksheet.write(_allIndex,0, label = _key)
		if _key in _notUsedKeys:
			worksheet.write(_allIndex, 1, "X", st_orange_center)

	# 保存Excel_test
	workbook.save(_dir)

def get_origin_str(_str):
	""" 去除首位双引号  和  末尾的\n"""
	if _str.startswith('"'):
		_str = _str[1:]
	if _str.endswith('\n'):
		_str = _str[:-1]
	if _str.endswith('"'):
		_str = _str[:-1]
	return _str
	
def findAllCheckFile_inis(_dir_all_pre="C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"):
	""" 获取所有的 ini 文件的上级目录 """
	_allFiles = set()
	_li = list()

	for root, lists, files in os.walk(_dir_all_pre):
		if 'build\\' in root or 'bin\\Debug\\' in root:
			continue
		for file in files:
			if file == 'locale.ini':
				continue
			if os.path.splitext(file)[1] in ['.ini']:
				_allFiles.add(root)

	_li = [(x.replace(_dir_all_pre, "xls_").replace('\\', '_'), x)  for x in _allFiles]
	return _li
	
def encodeStr(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
 
def decodeStr(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
    
"""
#不添加到 比对文本里面去。
Auth.AuthFailure.Text
Auth.AuthFailure.Title
Auth.Authing.Text
Auth.Authing.Title
Auth.ChannelFailure.Text
Auth.ChannelFailure.Title
Auth.Chat
Auth.InvalidScope.Text
Auth.InvalidScope.Title
Auth.LoadingChannel.Text
Auth.LoadingChannel.Title
Auth.StreamInfo
Basic.AutoConfig.StreamPage.GetStreamKey
Basic.Settings.Advanced.Network.TCPPacing.Tooltip
Basic.Settings.Stream.TTVAddon
Basic.Settings.Stream.TTVAddon.BTTV
Basic.Settings.Stream.TTVAddon.Both
Basic.Settings.Stream.TTVAddon.FFZ
Basic.Settings.Stream.TTVAddon.None
Bitrate
Channels.afreeca_tv
Channels.band
Channels.custom_rtmp
Channels.facebook
Channels.naver_shopping_live
Channels.naver_tv
Channels.now
Channels.twitch
Channels.vlive
Channels.wav
Channels.whale_space
Channels.youtube
RestreamAuth.Channels
Source.ErrorTips.PrismMobile.Error
TwitchAuth.Feed
TwitchAuth.Stats
TwitchAuth.TwoFactorFail.Text
TwitchAuth.TwoFactorFail.Title
blacklist.crashed.device.enumerating
blacklist.crashed.notfound
login.sign.endStr
navershopping.liveinfo.notify.fail.alert
navershopping.liveinfo.notify.fail.directStart
navershopping.login.fail
navershopping.no.live.right
prism.engine.alert.initcrash
prism.engine.alert.outofmemory
youtube.privacy.private.only.en
youtube.privacy.public.only.en
youtube.privacy.unlisted.only.en
"""