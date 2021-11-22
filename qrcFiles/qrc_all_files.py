# coding = utf-8

import os
import xml.dom.minidom as parse

dir_cache_path = 'D:\\PyTestCache\\'
dir_all_file = dir_cache_path + "all_qrc.txt"

dir_checked = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism"

def findAllQRCFile() -> list:
	""" 获取所有的 .qrc 之类的文件列表 """
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
			if os.path.splitext(file)[1] in ['.qrc'] and file.startswith('moc') == False and "QtApng" not in root:
				_allFiles.append(root+"\\"+file)


	with open(dir_all_file, 'a', encoding='utf-8') as fp:
		fp.truncate()
		for x in _allFiles:
			fp.write(x)
			fp.write('\n')

	return _allFiles

def get_qrc_keys(_file, _allKeys):
	_login_icons = ['/images/img-google-profile.svg','/images/img-line-profile.svg','/images/img-naver-profile.svg','/images/img-facebook-profile.svg','/images/img-kakaotv-profile.svg','/images/img-now-profile.svg','/images/img-twitch-profile.svg','/images/img-twitter-profile.svg']
	def is_ignored(_name):
		if _name.endswith('css'):
			return True
		# if '/images/login-begin/apngframe' in _name:
		# 	return True
		# if '/images/login-loop/apngframe' in _name:
		# 	return True
		if '/images/chat/btn-tab-' in _name:
			return True
		if _name in _login_icons:
			return True
		if '/images/bgm/BGM_equalizer-' in _name:
			return True
		# if '/images/add-source-view/ic-addsource-' in _name:
		# 	return True
		return False

	DOMTree  = parse.parse(_file)
	collection  = DOMTree .documentElement

	_resources = collection.getElementsByTagName('qresource')
	for x in _resources:
		_preTitle = ''
		if x.hasAttribute('prefix'):
			_preTitle = x.getAttribute('prefix')

		if _preTitle == '/':
			_preTitle = ''
		# print(_preTitle)
		_allFiles =  x.getElementsByTagName('file')

		for _name in _allFiles:
			_key = _name.childNodes[0].data
			_fullName = _preTitle + '/' + _key
			if is_ignored(_fullName) == False:
				_allKeys.append(_fullName)

	# return _allKeys


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
		# key_channel_header = 'Channels.'
		# t0 = time.time()
		# print(_file)
		# if 'libs\\QtApng' in _file or 'sub\\cam-effect\\src\\jsonWrapper\\cjson\\repeat.hpp' in _file:
		# 	return
		with open(_file, 'r', encoding='utf-8') as f:
			try:
				allLine = f.readlines()
			except Exception as e:
				print('----------------error encode file:' + _file)
			else:
				allLine = f.readlines()
				strLine = ",".join(allLine)
				strLine = strLine.replace('" "', '');
				for _key in keyDic:  #800 * 3
					# t0 = time.time()
					if keyDic[_key] > 0:
						continue
					
					if _key in strLine:
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