
import os, time, sys, io, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from auto_download_chromedriver_ifneed import download_chromedriver
from auto_download_chromedriver_ifneed import download_chromedriver as autoDC

"""
查看進程的啓動命令行參數
wmic process where caption="obs-browser-page.exe" get caption,commandline /value
wmic process where caption="chrome.exe" get caption,commandline /value | find remote
"""
# 

if __name__ == '__main__':

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
		if 'is_popout' in driver.current_url:
			break

	while True:
		v = driver.find_element(By.ID, 'input')
		print(v)
		a = driver.find_element(By.XPATH, '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/iron-pages/div[1]/yt-live-chat-message-input-renderer/div[2]/div[1]/div/yt-live-chat-text-input-field-renderer/div[1]')
		t5 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		a.send_keys(t5)
		print(t5)
		driver.find_element(By.XPATH, '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/iron-pages/div[1]/yt-live-chat-message-input-renderer/div[2]/div[3]/div[2]/div[2]/yt-button-renderer/a/yt-icon-button').click()
		time.sleep(60)

