# -*- coding:UTF-8 -*- 

import requests, urllib3, json, time, os
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

s_Image_type = "thumb" 
#raw full regular small thumb

class GetPhoto(object):
	"""docstring for GetPhoto"""
	def __init__(self):
		super(GetPhoto, self).__init__()
		self.photoUrls = []
		self.doCount = 0

	def getUrls(self, target):
		urllib3.disable_warnings()
		req = requests.get(url=target, verify=False)
		html = json.loads(req.text)
		for item in html[0:]:
			urlsItem = item["urls"]
			if s_Image_type in urlsItem:
				self.photoUrls.append(urlsItem[s_Image_type])
			else:
				print("-----无数据")

	def downloadImage(self, imageUrl, fileName):
		# print('下载url:   ' + imageUrl)
		# print('下载位置：  '+fileName)
		self.doCount += 1
		response = requests.get(imageUrl, verify=False, stream=True)
		if response.status_code == 200:
			# print('下载第 %d 张图片成功' % self.doCount)
			with open(fileName, 'wb') as file:
				for chunk in response.iter_content(chunk_size = 1024):
					if chunk:
						file.write(chunk)
						file.flush()
				# print('写入第 %d 张图片成功' % self.doCount)


	def moveFolder(self, folderName):
		print(os.getcwd())
		if not os.path.isdir(folderName):
			os.mkdir(folderName)
		os.chdir(folderName)

	def run(self):
		target = 'https://unsplash.com/napi/photos?page=%d&per_page=20'
		for i in range(11,20):
			print('--------------------------  %d  -----------------------------' % i)
			url = str(target % i)
			gPhoto.getUrls(url)
			time.sleep(0.3)

		print('获取url数量：%d' % len(gPhoto.photoUrls))

		gPhoto.moveFolder(s_Image_type)
		print('开始下载----')
		print(os.getcwd())

		po = ThreadPool(8)
		po.map(self.download, gPhoto.photoUrls)
		po.close()
		po.join()

	def download(self, url):
		for i, val in enumerate(self.photoUrls):
			if val in url:
				index = i
				break
		path = os.getcwd() + '\\%d.jpg' % index
		print('-----start: ' + path, end="\n")
		self.downloadImage(url, path)

if __name__ == '__main__':
	
	gPhoto = GetPhoto()
	gPhoto.run()