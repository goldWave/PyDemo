# coding = utf-8

import os, time, sys
import urllib.parse as up
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

chrome_93 = "chromedriver93.0.4577.15.exe"
client_secret = ''

def getConfigjsonPath(_name = 'id_ps.json'):
	_path = os.path.join(os.path.dirname(__file__), _name)
	if not os.path.exists(_path):
		_path = os.path.join(os.path.dirname(sys.executable), _name)
	return _path

def readJson():
	global client_secret
	_path = getConfigjsonPath()
	if not os.path.exists(_path):
		print('not found json path')
		exit()
	with open(_path, 'r') as f:
		_dict = json.load(f)
		client_secret = _dict['youtube_client_secret']


class youtube(object):
	"""docstring for youtube"""
	def __init__(self):
		super(youtube, self).__init__()
		self.isHeadless = True
		fullPath = sys.executable
		fullPath = os.path.split(fullPath)[0]
		fullPath = os.path.join(fullPath, chrome_93)
		if os.path.exists(fullPath):
			self.driverPath = fullPath
		else:
			self.driverPath = "D:\\pythonDemo\\driver\\chromedriver_win32\\" + chrome_93

		if os.path.exists(self.driverPath) == False:
			sys.stderr("chromedriver.exe not found")
			exit()
		print(self.driverPath)
		self.domain = 'https://accounts.google.com'
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		if self.isHeadless == True:
			self.browser = webdriver.Chrome(self.driverPath, options=options)
		else:
			self.browser = webdriver.Chrome(self.driverPath)

		self.browser.maximize_window()
		self.browser.implicitly_wait(5)
		self.yCode = ""

		parser = argparse.ArgumentParser(description='manual to this script')
		parser.add_argument("-E", type=str, default="", help='input email')
		parser.add_argument("-P", type=str, default='',help='input password')
		args = parser.parse_args()
		self.userName = args.E
		self.userPassword = args.P
		if self.userName == "" or self.userPassword == "":
			sys.stderr("----not input email or password--------")
			self.browser.quit()
			exit()

	def write_page(self, _name):
		with open(_name ,'wb') as f:
			f.write(self.browser.page_source.encode("gbk", "ignore")) # 忽略非法字符


	def open_youtube_headless(self):
		self.browser.get('https://accounts.google.com/o/oauth2/v2/auth?client_id=775513731180-rc0mrf2dno2bumtf7f6chfs3uh44ur0a.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/youtube&email&response_type=code&redirect_uri=http://localhost')

		self.browser.save_screenshot('C:\\Users\\Administrator\\Desktop\\test.png')
		# self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys(self.userName)
		element = self.browser.find_element_by_id('Email').send_keys(self.userName)

		element = self.browser.find_element_by_id('next').click()
	
		self.browser.find_element_by_id('password').send_keys(self.userPassword)
		#点击密码用户下一步
		element = self.browser.find_element("id","submit").click()
		#选择channel
		element = self.browser.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/ol/li[1]/a').click()
		# 点击信任账户 允许
		time.sleep(2)
		element = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/form/button[1]').click()
		time.sleep(2)
		print(self.browser.current_url)
		current_url = self.browser.current_url
		if current_url.startswith('http://localhost'):
			self.yCode = current_url.split("code=")[1].split('&')[0].replace('#','')
			print(self.yCode)

	def open_youtube(self):
		if self.isHeadless == True:
			self.open_youtube_headless()
			return
		self.browser.get('https://accounts.google.com/o/oauth2/v2/auth?client_id=775513731180-rc0mrf2dno2bumtf7f6chfs3uh44ur0a.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/youtube&email&response_type=code&redirect_uri=http://localhost')
		time.sleep(2)
		self.write_page()
		self.browser.save_screenshot('C:\\Users\\Administrator\\Desktop\\test.png')
		# self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys(self.userName)
		element = self.browser.find_element_by_id('identifierId').send_keys(self.userName)
		# return
		#点击email用户下一步
		element = self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
		self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(self.userPassword)
		#点击密码用户下一步
		element = self.browser.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
		#选择channel
		element = self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div').click()
		# 点击信任账户 允许
		element = self.browser.find_element_by_class_name('VfPpkd-RLmnJb').click()
		time.sleep(2)
		print(self.browser.current_url)
		current_url = self.browser.current_url
		if current_url.startswith('http://localhost'):
			self.yCode = current_url.split("code=")[1].split('&')[0].replace('#','')
			print(self.yCode)
			
	def request_token(self):
		self.yCode = up.unquote(self.yCode)
		# self.yCode = "4/0AY0e-g6iXLfL0fKhGpOePKjBpmUMMhrQU5dIyFCkILXpCrNLRjJRxFUNQDMsqQZ9m_Csvg"
		if self.yCode == "":
			print("code is empty")
			return

		import requests

		headers = {
		    'Host': 'www.googleapis.com',
		    'Accept-Language': 'zh-CN,en,*',
		    'User-Agent': 'Mozilla/5.0',
		}
		readJson()
		params = (
		    ('client_id', '775513731180-rc0mrf2dno2bumtf7f6chfs3uh44ur0a.apps.googleusercontent.com'),
		    ('client_secret', client_secret),
		    ('code', self.yCode),
		    ('grant_type', 'authorization_code'),
		    ('redirect_uri', 'http://localhost'),
		)
		print(params)
		response = requests.post('https://www.googleapis.com/oauth2/v4/token', headers=headers, params=params)
		# print(response.status_code)
		print(response.text)
		if response.status_code == 200:
			pass
		else:
			print("error with request token")

if __name__ == '__main__':
	yb = youtube()
	# yb.open_youtube()
	# yb.browser.quit()
	yb.request_token()