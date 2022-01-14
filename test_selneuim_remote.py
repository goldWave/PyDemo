
import os, time, sys, io, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from auto_download_chromedriver_ifneed import download_chromedriver


"""
查看進程的啓動命令行參數
wmic process where caption="obs-browser-page.exe" get caption,commandline /value
"""

def _is_exist_element(e):
	global driver
	flag=True
	try:
		driverfind_element(By.ID, e)
		flag = True
	except Exception as e:
		flag = False
	return flag

def click_login(_id_ui, _pw_ui, _login_btn, driver):
	_id, _pw = "nvqa_prism_cd_003", "naver123!@#"
	if _id == '' or _pw == '':
		print('id or pw is empty')
		return False

	_isSucc = True
	e = driver.find_element(By.ID, _id_ui)
	e.clear()
	e.send_keys(_id)

	e = driver.find_element(By.ID, _pw_ui)
	e.clear()
	e.send_keys(_pw)

	driver.find_element(By.ID, _login_btn).click()

	return _isSucc

def click_login_page(driver):		
	_url = driver.current_url
	while True:
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
			# print('sleep 5')
			# time.sleep(5)
			break

def vliveLogin(driver):
	print(driver.current_url)
	driver.find_element(By.CSS_SELECTOR, "[class='login_btn naver']").click()
	time.sleep(2)
	click_login("id", "pw", "log.login", driver)

if __name__ == '__main__':
	chromedriverPath = download_chromedriver(fulleVersion="75.0.3770.100")
	is_cef = True
	if is_cef == False:
		chromedriverPath = "xxx"
		chrome_port = "9529"
	else:
		chrome_version = "chromedriver_75.0.3770.90.exe"
		chrome_port = "9527"
	print("start... port:" + chrome_port)
	if not os.path.exists(chromedriverPath):
		print("all not found driverPath")
		exit(0)

	s = Service(chromedriverPath)	
	chrome_options =  webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:"+chrome_port);
	driver = webdriver.Chrome(options = chrome_options)
	windowstabs=driver.window_handles
	for x in windowstabs:
		driver.switch_to.window(x)
		print(driver.title, driver.current_url)
		
	driver.switch_to.window(windowstabs[0])
	vliveLogin(driver)


