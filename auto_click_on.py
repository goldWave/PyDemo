
import os, time, sys, io, json
import datetime
from ctypes import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from auto_download_chromedriver_ifneed import download_chromedriver
from auto_download_chromedriver_ifneed import download_chromedriver as autoDC

"""
查看進程的啓動命令行參數
wmic process where caption="obs-browser-page.exe" get caption,commandline /value
wmic process where caption="chrome.exe" get caption,commandline /value | findstr remote
"""
# 

def isValidTime() -> bool:
	_now = datetime.datetime.now().strftime('%Y-%m-%d')
	_now +=  " 18:41:00"
	# print(_now)
	timeArray = time.strptime(_now, "%Y-%m-%d %H:%M:%S")
	 
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

def clickOutBtn():
	os.system("taskkill /f /im chromedriver.exe /T")
	chromedriverPath = autoDC()
	print(chromedriverPath)
	chrome_options =  webdriver.ChromeOptions()
	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9533")
	s = Service(chromedriverPath)
	driver = webdriver.Chrome(service=s, options = chrome_options)
	print(driver.current_url)

	windowstabs=driver.window_handles
	for tab in windowstabs:
		driver.switch_to.window(tab)
		print("switch_to: ", driver.current_url)
		if driver.current_url.startswith("https://connect.navercorp.com/home"):
			break

	print(driver.current_url)
	driver.switch_to.frame('hrIframe')
	_outBtn = driver.find_element(By.CLASS_NAME, 'btn_check.on')
	print(_outBtn)
	_outBtn.click()
	closewindows(10)

if __name__ == '__main__':
	while True:
		if isValidTime():
			clickOutBtn()
			break
		else:
			print(datetime.datetime.now(), "  ...")
			time.sleep(60)