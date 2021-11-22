# coding = utf-8

import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class taobao(object):
	"""docstring for taobao"""
	def __init__(self):
		super(taobao, self).__init__()
		self.driverPath = 'D:\\pythonDemo\\driver\\chromedriver_win32\\chromedriver.exe'
		self.domain = 'http://www.taobao.com'
		self.browser = webdriver.Chrome(self.driverPath)
		self.browser.maximize_window()
		self.browser.implicitly_wait(5)
		self.userName = '任金波91'
		self.userPassword = '123Bu.'
		self.actionChain = ActionChains(self.browser)

	# def open_python_org(self):
	# 	# browser = webdriver.Chrome(driverPath)
	# 	browser.get('https://python.org')
	# 	print(browser.title)
	# 	elem = browser.find_element_by_id('id-search-field')
	# 	elem.send_keys('pycon')
	# 	elem.send_keys(Keys.RETURN)
	# 	print(elem, elem.text)

	# def open_baidu(self):
	# 	browser.get('https://www.baidu.com')
	# 	elem = browser.find_element_by_id("kw")
	# 	elem.send_keys('任金波')
	# 	elem.send_keys(Keys.RETURN)
	# 	time.sleep(1)
	# 	e1 = browser.find_element_by_class_name('n').click()

	def open_taobao(self):
		self.browser.get('https://www.taobao.com')
		element = self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]')
		element.click()
		self.browser.find_element_by_id('fm-login-id').send_keys(self.userName)
		self.browser.find_element_by_id('fm-login-password').send_keys(self.userPassword)
		# self.browser.find_element_by_class_name('fm-button fm-submit password-login').click()
		time.sleep(1.5)
		try:
			slider = self.browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
			if slider.is_displayed():
				self.actionChain.drag_and_drop_by_offset(slider, xoffset=258, yoffset=0).perform()
				self.actionChain.release().perform()
			# time.sleep(0.5)
			# slider = self.browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
			# if slider.is_displayed():
			# 	self.actionChain.drag_and_drop_by_offset(slider, xoffset=258, yoffset=0).perform()

		except Exception as e:
			print("error:   " + str(e))
		# self.browser.quit()
			# raise e
		time.sleep(1.5)
		self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
		nickName = self.get_nickname()
		print(nickName)
		if nickName:
			print('login succeed!')
		else:
			print('login failed!')
			exit()

		self.browser.find_element_by_xpath('//*[@id="mc-menu-hd"]').click()
		time.sleep(0.5)
		self.browser.find_element_by_id('J_SelectAll1').click()
		time.sleep(0.5)
		self.browser.find_element_by_class_name('J_DeleteSelected').click()
		time.sleep(0.5)
		self.browser.find_element_by_class_name('dialog-btn.J_DialogConfirmBtn').click()
		print('删除成功')



	def get_nickname(self):
		# time.sleep(5)
		# self.browser.get(self.domain)
		time.sleep(1)
		try:
			n = self.browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div/div[1]/span/strong').text
			return n
		except Exception as e:
			print(str(e))
			return ''

if __name__ == '__main__':
	
	tb = taobao()
	tb.open_taobao()
	# open_baidu()
	# open_python_org()
	# bigs()
