
import os, time, sys, io, json
import datetime
from ctypes import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from auto_download_chromedriver_ifneed import download_chromedriver
from auto_download_chromedriver_ifneed import download_chromedriver as autoDC
from ini_common_method import *

"""
查看進程的啓動命令行參數
wmic process where caption="obs-browser-page.exe" get caption,commandline /value
wmic process where caption="chrome.exe" get caption,commandline /value | findstr remote
"""
# 

_k_decodeStr = '1101000 1110100 1110100 1110000 1110011 111010 101111 101111 1100011 1101111 1101110 1101110 1100101 1100011 1110100 101110 1101110 1100001 1110110 1100101 1110010 1100011 1101111 1110010 1110000 101110 1100011 1101111 1101101 101111 1101000 1101111 1101101 1100101'

def getScheduleTime():
	_now = datetime.datetime.now().strftime('%Y-%m-%d')
	_now +=  " 18:40:10"
	
	return _now

def isValidTime() -> bool:
	timeArray = time.strptime(getScheduleTime(), "%Y-%m-%d %H:%M:%S")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))

	if time.time() > timeStamp:
		return True
	return False


def closewindows(closetime):
  while closetime>0:
    print(closetime)
    time.sleep(1)
    closetime-=1
  user32 = windll.LoadLibrary('user32.dll')
  user32.LockWorkStation()

def check_login_btn(driver):
    try:
        l = driver.find_element(By.ID, 'loginBtnAct')
        l.click()
    except:
        pass

    try:
        driver.switch_to.frame('hrIframe')
        driver.find_element(By.ID, 'loginBtnAct').click()
    except:
        pass

def clickOutBtn():
	os.system("taskkill /f /im chromedriver.exe /T")
	chromedriverPath = autoDC()
	print(chromedriverPath)
	chrome_options =  webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9533")
	s = Service(chromedriverPath)
	driver = webdriver.Chrome(service=s, options = chrome_options)
	print(driver.current_url)

	is_found = False
	windowstabs=driver.window_handles
	for tab in windowstabs:
		driver.switch_to.window(tab)
		# print("switch_to: ", driver.current_url)
		if driver.current_url.startswith(decodeStr(_k_decodeStr)):
			is_found = True
			break
	if not is_found:
		driver.get(decodeStr(_k_decodeStr))
	check_login_btn(driver)
	sleep(5)
	_outBtn = driver.find_element(By.CLASS_NAME, 'btn_check.on')
	print(_outBtn)
	_outBtn.click()
	closewindows(10)

def startSchedule():
	print("scheudleTiem:" , getScheduleTime())
	while True:
		if isValidTime():
			clickOutBtn()
			break
		else:
			print(datetime.datetime.now(), "  ...")
			time.sleep(30)

if __name__ == '__main__':
	startSchedule()