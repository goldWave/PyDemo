import os, sys, json, tempfile
import requests
import zipfile
import datetime, time
from urllib.parse import urlparse, parse_qs
from sys import exit
sys.path.insert(0, "../")
from auto_download_chromedriver_ifneed import download_chromedriver as autoDC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from contextlib import closing

# pyinstaller -F  sub_process.py -p auto_download_chromedriver_ifneed.py

jsonName =  "nelo_json_time_config.json"
id_ps_name =  "id_pw.json"
#pyinstaller -F C:\Users\Administrator\Desktop\44\nelo_json_time_sort.py

_dict = dict()
_IdpwDict = dict()


_suffixName = str()
# {
# "account": "",
# "password": ""
# }

query_params = (
    ("from", ""),
    ("to", ""),
    ("limit", "2000"),
    ("format", "json"),
    ("count", ""),
    ("fields", "logLevel,NeloSDK.raw,CrashOperation.raw,host,logSource.raw,projectName,PeerIP.raw,projectVersion"),
)

query_data = {
}

def print(*objects, sep=' ', end='\n', file=sys.stdout, flush=True):
	__builtins__.print(*objects, sep=sep, end=end, file=file, flush=flush)

def getConfigjsonPath(_name = jsonName):
	_path = os.path.join(os.path.dirname(__file__), _name)
	if not os.path.exists(_path):
		_path = os.path.join(os.path.dirname(sys.executable), _name)
	return _path

def writeJson():
	_path = getConfigjsonPath()
	with open(_path, 'w') as f:
		json.dump(_dict, f)

def readJson():
	global _dict
	_path = getConfigjsonPath()
	if not os.path.exists(_path):
		print('not found json path')
		exit()
	with open(_path, 'r') as f:
		_dict = json.load(f)

def getPW():
	global _IdpwDict
	_path = getConfigjsonPath(id_ps_name)
	if not os.path.exists(_path):
		print('not found %s path' % (id_ps_name))
		exit()
	with open(_path, 'r') as f:
		_IdpwDict = json.load(f)

def runChrom():
	_path = getConfigjsonPath(id_ps_name)
	if len(_IdpwDict["account"]) == 0 or len(_IdpwDict["password"]) == 0:
		print("token 信息过期，需要手动在 %s \t  里面的'account' 和 'password'输入账号密码" %(_path))
		exit()
	chromedriverPath = autoDC(os.path.split(_path)[0])
	print(chromedriverPath)
	print("登陆中...")
	s = Service(chromedriverPath)
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	isHeadless = True
	if isHeadless == True:
		browser = webdriver.Chrome(service=s, options=options)
	else:
		browser = webdriver.Chrome(service=s)

	browser.set_page_load_timeout(15)
	browser.maximize_window()

	browser.get("https://nelo2.navercorp.com/nelo/")
	browser.implicitly_wait(5)
	browser.find_element(by=By.CSS_SELECTOR, value="[class='btn btn-success']").click() 

	e = browser.find_element(By.ID, 'username')
	e.clear()
	e.send_keys(_IdpwDict["account"])

	e = browser.find_element(By.ID, "password")
	e.clear()
	e.send_keys(_IdpwDict["password"])

	e = browser.find_element(by=By.CSS_SELECTOR, value="[class='btn btn-primary btn-block']").click() 
	
	profile = browser.find_element(By.ID, "user-profile")
	profile.click()
	cookie_list = browser.get_cookies()
	print("登录完成，重新进入下载流程。")
	return cookie_list

def getjsonPath(_path, logPath, num=10):
	# 将nelo的json 写入本地txt文件
	def file_name(file_dir):
		_pathList = []
		for root, dirs, files in os.walk(file_dir):
			for v in files:
				if not v.endswith('json'):
					files.remove(v)
			files = files[0:num]
			files.sort()
			# print(files)
			for v in files[::-1]:
				_pathList.append(os.path.join(root, v))
		return _pathList

	def jsonApply(path):
		if not os.path.exists(path):
			print('not found json contents')
			return []
		with open(path, 'r', encoding='utf-8') as f:
			_list = json.load(f)
		return _list

	_paths = file_name(_path)
	if (len(_paths) == 0):
		print("no file exists")
		exit()
	_allDatas = []
	for path in _paths:
		_list = jsonApply(path)
		for _item in _list:
			a = _item["body"]
			_allDatas.append(a)
	_allDatas.sort()

	with open(logPath, 'w', encoding='utf-8') as f:
		f.seek(0)
		f.truncate()
		f.write("0000 remoteUrl: " + _dict['userUrl'])
		f.write('\n\n')
		for line in _allDatas:
			f.write(line)
			f.write('\n')
	print("succeed, out path: %s" % (logPath))
	os.startfile(logPath)

def zip_and_un_zip(data, path, unzipPath):
	# with open(path, 'wb') as s:
	# 	s.write(data)
	zFile = zipfile.ZipFile(path, "r")
	print(zFile.namelist())
	for fileM in zFile.namelist(): 
		# print(fileM)
		zFile.extract(fileM, unzipPath)
	zFile.close()
	print("unzip succeed.")


 
def get_FileSize(filePath):
	fsize = os.path.getsize(filePath)
	fsize = fsize/float(1024 * 1024)
	return round(fsize, 2)

def requetAndWriteLog():
	# print(config.host)
	# print('\n')
	print("url: " + _dict['headers']["Referer"])
	# print('\n')
	# print(query_params)
	# print('\n')
	# # print(config.cookies)
	# # print('\n')
	# print(query_data)
	# print('\n')
	# response = requests.post(_dict['host'], headers=_dict['headers'], params=query_params, data=query_data, cookies=_dict['cookies'])
	
	now = datetime.datetime.now()
	timeName = now.strftime("%m_%d_%Y_%H_%M_%S_") + str(now.microsecond)

	wirteCount = 0

	with tempfile.TemporaryDirectory() as tmpdir:
		zipPath = os.path.join(tmpdir, timeName + '.zip')
		unzipPath = os.path.join(tmpdir, timeName)


		with closing(requests.post(_dict['host'], headers=_dict['headers'], params=query_params, data=query_data, cookies=_dict['cookies'], stream=True)) as response:
			chunk_size = 40960 # 单次请求最大值
			print("status_code: %d" % (response.status_code))
			if response.status_code != 200:
				if response.status_code == 401:
					return 401
				exit()
			total_down = 0;
			content_size = '--'
			if 'content-length' in response.headers:
				content_size = str(int(response.headers['content-length']) // 1024)
			with open(zipPath, "wb") as file:
				for data in response.iter_content(chunk_size=chunk_size):
					file.write(data)
					total_down += len(data)
					if wirteCount % 10 == 0:
						print("downlad process: %dkb / %skb" % (total_down // 1024, content_size))
					wirteCount += 1


			print("下载完成：文件大小：%.2f MB"%(get_FileSize(zipPath)))
			zip_and_un_zip(data, zipPath, unzipPath)
			des = _dict['savePath']
			if des == "":
				des = os.path.expanduser('~/Documents')
			logPath = os.path.join(des, timeName + _suffixName +'.txt')
			maxFile = int(_dict['maxcount']) // 500
			getjsonPath(unzipPath, logPath = logPath,  num= maxFile)

	# data = response.content


	return 200

def changeRequestParmater():
	url = _dict['userUrl']
	if len(url) == 0:
		print("url is empty")
		exit()

	_dict['headers']['Referer'] = url
	queryDict = parse_qs(urlparse(url).query)
	if "query" in  queryDict:
		query_data['query'] = queryDict['query']

	fromStr = 0
	toStr = 0
	if 'period' in queryDict:
		ti = queryDict['period'][0]
		toStr = int(round(time.time() * 1000))
		if not ti.startswith('-'):
			print("url 里面的时间区间类型不支持")
			exit()
		offset = 0
		timeType = ti[-1]
		ti = ti[1:-1]
		if 's' == timeType:
			offset = 1
		elif 'm' == timeType:
			offset = 60
		elif 'h' == timeType:
			offset = 60*60
		elif 'd' == timeType:
			offset = 60*60*24
		fromStr = toStr - offset*1000*int(ti)
	elif 'from' in queryDict:
			fromStr = queryDict['from'][0]
			if 'to' in queryDict:
				toStr = queryDict['to'][0]
	else:
		print("url 里面未包含 时间区间，不支持，请换url")
		exit()
	global query_params
	tmpList = [list(v) for v in query_params]
	for v in tmpList:
		if v[0] == 'from':
			v[1] = str(fromStr)
		elif v[0] == 'to':
			v[1] = str(toStr)
		elif v[0] == 'count':
			v[1] = _dict['maxcount']
	query_params = tuple([tuple(x) for x in tmpList])

def wirteSpiderData(_data: list):
	global _dict
	for x in _data:
		_name = x['name']
		_v = x['value']
		_dict['cookies'][_name] = _v
		if 'NELO-CSRF-TOKEN' in _name:
			_dict['headers']['X-CSRF-Token'] = _v

if __name__ == '__main__':
	readJson()
	getPW()
	if len(sys.argv) > 1:
		_url = sys.argv[1]
		_dict['userUrl'] = _url
		print("接收到参数:" + _url)
	if len(sys.argv) > 2:
		_suffixName = sys.argv[2]
	changeRequestParmater()
	_code = requetAndWriteLog()
	if _code == 401:
		wirteSpiderData(runChrom())
		requetAndWriteLog()
	writeJson()
