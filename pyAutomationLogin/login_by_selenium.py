#!/usr/local/bin/python -u
# coding = utf-8

import os, time, sys, io, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# is_cef = False
is_cef = True

_dict = {}

def print(*objects, sep=' ', end='\n', file=sys.stdout, flush=True):
	__builtins__.print(*objects, sep=sep, end=end, file=file, flush=flush)

def _is_exist_element(e):
	global driver
	flag=True
	try:
		driver.find_element_by_id(e)
		flag = True
	except Exception as e:
		flag = False
	return flag

def _is_exist_element_calss(e):
	global driver
	flag=True
	try:
		driver.find_element_by_class_name(e)
		flag = True
	except Exception as e:
		flag = False
	return flag

def jsonApply():
    global _dict
    _path = os.path.join(os.path.dirname(__file__), "id_pw_user.json")
    if not os.path.exists(_path):
        _path = os.path.join(os.path.dirname(__file__), "id_pw.json")
    if not os.path.exists(_path):
        print('not found any id password local cache path')
        return

    with open(_path, 'r') as f:
        try:
            _dict = json.load(f)
        except Exception as e:
            print("id passord json parase failed! %s" % e.args)

def getPlatform(urlStr) -> str:
    if 'band.us' in urlStr:
        return 'band'
    elif 'vlive.tv' in urlStr:
        return 'vlive'
    elif 'shoppinglive' in urlStr:
        return 'navershopping'
    elif urlStr.endswith('nidlogin.login'):
        return 'navertv'
    elif 'afreecatv' in urlStr:
        return 'afreecatv'
    elif 'facebook' in urlStr:
        return 'facebook'
    return 'empty'

def getusername(_pls):
     if not _pls in _dict.keys():
        return '',''
     _id = _dict[_pls]['acc']
     _pw = _dict[_pls]['pw']
     return _id, _pw

def click_login(_id_ui, _pw_ui, _login_btn, driver):
	_plat = getPlatform(driver.current_url)
	print('found %s login page' % _plat)
	_id, _pw = getusername(_plat)
	if _id == '' or _pw == '':
		print('id or pw is empty')
		return False
	_isSucc = True
	if _is_exist_element(_id_ui) == False:
		print("found element id failed.")
		return 

	try:
		e = driver.find_element_by_id(_id_ui)
		e.clear()
		e.send_keys(_id)

		e = driver.find_element_by_id(_pw_ui)
		e.clear()
		e.send_keys(_pw)
		if _plat == 'afreecatv':
			driver.find_element_by_class_name(_login_btn).click()
		else:
			driver.find_element_by_id(_login_btn).click()
	except Exception as e:
		_isSucc = False
		print("found element failed.")
		print(e.args)

	return _isSucc

def click_login_page(driver):
	_chandel = driver.current_window_handle
	while True:
		windowstabs=driver.window_handles
		if _chandel not in driver.window_handles:
			_chandel = ""

		if len(driver.window_handles) > 0 and windowstabs[-1] != _chandel:
			driver.switch_to.window(windowstabs[-1]) #切换至最前面的页面
			_chandel = driver.current_window_handle 
			print("切换到最新的页面")
		if _chandel == "":
			print("view is empty")
			time.sleep(5)
			continue

		try:
			_url = driver.current_url
		except Exception as e:
			print("url is not found.")
			print(e.args)
			time.sleep(5)
			continue
		
		print("current_url: %s" % _url)
		if 'www.vlive.tv/auth/page/login' in _url:
			#vlive 选择登陆平台
			e = driver.find_element_by_css_selector("[class='login_btn naver']").click() 
			time.sleep(2)
		elif "://nid.naver.com/oauth2.0/authorize?" in _url or "nid.naver.com/nidlogin.login" in  _url:
			#naver 登陆密码
			click_login("id", "pw", "log.login", driver)
			time.sleep(2)
		elif 'login.afreecatv.com/afreeca/login.php' in _url:
			#afreecatv 登陆密码
			if click_login("uid", "password", "btn_st1", driver) == False and _is_exist_element_calss('login_btn') == True:
				print("try to other way to found login_btn")
				driver.find_element_by_class_name('login_btn').find_element_by_xpath("button").click()

			time.sleep(2)
		elif 'afreecatv.com/app/campaign_pw.php' in _url:
			#afreecatv 修改密码，选择否
			driver.find_element_by_id('btnNextTime').click()
			time.sleep(2)
		elif 'shoppinglive.naver.com/' in _url:
			#shoppinglive 选择登陆平台
			driver.find_element_by_class_name('Login_link_naver_1_Ux2').click()
			time.sleep(2)
		elif 'auth.band.us/login' in _url:
			#band 选择登陆平台 
			driver.find_element_by_xpath('/html/body/div/section/ul/li[3]/a/span').click()
			time.sleep(2)
		elif '//www.facebook.com/login' in _url:
			#facebook 登陆密码
			e =  driver.find_element_by_id("email")
			print(e)
			click_login("email", "pass", "loginbutton", driver)
			time.sleep(2)
		else:
			print('sleep 5')
			time.sleep(5)

if __name__ == '__main__':
	jsonApply()
	chrome_options = Options()

	if is_cef == False:
		chrome_version = "chromedriver93.0.4577.15.exe"
		chrome_port = "9529"
	else:
		chrome_version = "chromedriver_75.0.3770.90.exe"
		chrome_port = "9527"

	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+chrome_port)

	print("start... port:" + chrome_port)
	driverPath = os.path.join(os.path.dirname(__file__), chrome_version)
	if not os.path.exists(driverPath):
		driverPath = os.path.join(os.path.dirname(__file__),'dist', 'plslogin', chrome_version)
	print(driverPath)
	if not os.path.exists(driverPath):
		print("all not found driverPath")
		exit(0)

	driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)
	print(driver.current_url)
	windowstabs=driver.window_handles

	print(windowstabs)
	print(driver.title + driver.current_window_handle)
	click_login_page(driver)
	driver.quit()