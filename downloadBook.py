# -*- coding: utf-8 -*-

import requests, sys
from bs4 import BeautifulSoup


class downloader(object):
	"""docstring for downloader"""
	def __init__(self):
		super(downloader, self).__init__()
		self.server = 'https://www.biqukan.com'
		self.target = 'https://www.biqukan.com/1_1094/'
		self.names = []
		self.urls = []
		self.nums = 0 
		self.contents = []
		

	def get_download_url(self):
		req = requests.get(url = self.target)
		req.encoding = req.apparent_encoding
		html = req.text
		div_bf = BeautifulSoup(html, 'html.parser')
		div = div_bf.find('div', class_ = 'listmain')
		a_bf = BeautifulSoup(str(div), 'html.parser')
		a = a_bf.find_all('a')
		# self.nums = len(a[15]) #not look pages
		self.nums = 0
		for each in a[13:]:
			if '章' in each.string:
				self.names.append(each.string)
				# print(each.string)
				self.nums += 1
				self.urls.append(self.server + each.get('href'))
				# print(each.string, self.url)
		
		# print(self.names, end='\n')

	def  get_contents(self, target):
		req = requests.get(url = target)
		req.encoding = req.apparent_encoding
		bf = BeautifulSoup(req.text, 'html.parser')
		texts = bf.find('div', class_ = 'showtxt')
		# print(bf.text)
		# print(texts)
		texts = texts.text.replace('\xa0'*8, '')
		return texts

	def writer(self, name, path, text):
		write_Flag = True
		with open(path, 'a', encoding='utf-8') as f:
			f.write(name + '\n')
			f.writelines(text)
			f.write('\n\n')




if __name__ == '__main__':

	# print('进度 %.3f%%' % float(1/5) + '\n')

	d = downloader()
	d.get_download_url()

	# for i in range(d.nums):
	# 	print(d.names[i], d.urls[i])
	# 	d.writer(d.names[i], '一念永恒.txt', d.get_contents(d.urls[i]))
	# 	sys.stdout.write('下载进度 %0.3f%%' % float(i/d.nums) + '\r')
	# 	sys.stdout.flush()

	for i in range(d.nums):
		# print(d.names[i], d.urls[i])
		d.writer(d.names[i], '一念永恒.txt', d.get_contents(d.urls[i]))
		sys.stdout.write('下载进度 %0.3f%%' % float(i/d.nums) + '\r')
		sys.stdout.flush()