# -*- coding: utf-8 -*-

import requests, os, re, glob
import ffmpy3
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

search_keywords = "大神猴"
search_url = "http://www.jisudhw.com/index.php"
search_param = {
	'm': 'vod-search'
}
serach_headers = {
	'Host': 'www.jisudhw.com',
	'Origin': 'http://www.jisudhw.com',
	'Referer': 'http://www.jisudhw.com/?m=vod-detail-id-56780.html',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
headers_agent = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
search_data = {
	'wd': search_keywords,
	'submit': 'search'
}
class DMovie(object):
	"""docstring for DMovie"""
	def __init__(self):
		super(DMovie, self).__init__()
		self.search_res = {}
		self.detail_url = ""

	def SearchData(self):
		r = requests.post(url = search_url, params = search_param, verify = False, headers = serach_headers, data = search_data)
		r.encoding = r.apparent_encoding
		bf = BeautifulSoup(r.text, 'html.parser')
		search_spans = bf.find_all(class_ = 'xing_vb4')
		# print(search_spans.text)
		server = 'http://www.jisudhw.com'
		for data in search_spans:
			if data.text == '大神猴完结':
				url = server + data.a.get('href')
				# print(data.a.string + url)
		self.detail_url = url

	def ParserDetailUrl(self, url):
		r = requests.get(url = url, verify = False, headers = serach_headers)
		r.encoding = r.apparent_encoding
		bf = BeautifulSoup(r.text, 'html.parser')
		search_inputs = bf.find_all('input')
		num = 1
		for data in search_inputs:
			if 'm3u8' in data.get('value'):
				mUrl = data.get('value')
				if mUrl not in self.search_res.keys():
					self.search_res[mUrl] = num
				print('第%03d集:  ' % num + mUrl)
				num+=1

	def moveFolder(self,folderName):
			if not os.path.exists(folderName):
				os.mkdir(folderName)
			os.chdir(folderName)

	def download_movie_by_ffmpeg(self, url):
		mName = ''
		for k in self.search_res:
			if k == url:
				index = self.search_res[k]
				mName = str("第%d集.mp4" % index)
				break
	
		print(mName + "-----" + url)
		ff = ffmpy3.FFmpeg(inputs={url: None}, outputs={os.getcwd() + "\\" + mName: None})
		ff.run()

	def download_m3u8_file(self, url, saveName):
		r = requests.get(url, headers = headers_agent)
		r.encoding = r.apparent_encoding
		if r.status_code == 200:
			con = r.text
			if con.split('\n')[-1] == '':
				hls_mask = con.split('\n')[-2]
			else:
				hls_mask = con.split('\n')[-1]
			url_m3u8_hls = url.replace('index.m3u8', hls_mask)
		self.download_m3u8_hls_file(url_m3u8_hls, saveName)

	def download_m3u8_hls_file(self, url, saveName):
		r = requests.get(url, headers = headers_agent)
		r.encoding = r.apparent_encoding
		if r.status_code == 200:
			with open(saveName, 'wb') as f:
				f.write(r.content)
		allLists = r.text.split('\n')
		names = [i for i in allLists if i.endswith('.ts')]
		times = [float(re.findall('[.\\d]+', i)[0]) for i in allLists if i.startswith('#EXTINF:')]
		all_time = 0
		for i in times:
			all_time+=i
		print('文件名：{} 总数量：{} 总时间:{}'.format(saveName,len(times),all_time))

		full_urls = [url.replace('index.m3u8', i) for i in names]
		# self.save_file(url.replace('index.m3u8', names[0]), os.path.join(os.getcwd(), names[0]))
		poolD = ThreadPool(8)
		res = poolD.map(self.save_file, full_urls)
		poolD.close()
		poolD.join()


	def save_file(self, url):
		saveName = os.path.join(os.getcwd(), url.split('/')[-1])
		print('start download to:' , saveName)
		r = requests.get(url, headers = headers_agent)
		r.encoding = r.apparent_encoding
		if r.status_code != 200:
			return
		with open(saveName, 'wb') as f:
			f.write(r.content)
		print('----complect: ', saveName)

	def combine_ts(self):
		c_ts = 'combine_ts.ts'
		os.remove(c_ts)
		file_list = glob.glob('*.ts')
		file_list.sort()
		with open(c_ts, 'wb') as f:
			for i in file_list:
				f.write(open(i, 'rb').read())
		ffmpy3.FFmpeg(inputs={c_ts: None}, outputs={"combine.mp4": None}).run()


if __name__ == '__main__':

	class_movie = DMovie()
	class_movie.SearchData()
	class_movie.ParserDetailUrl(class_movie.detail_url)
	class_movie.moveFolder('moviesHand')

	def thread_ffmpeg():
		poolD = ThreadPool(8)
		results = poolD.map(class_movie.download_movie_by_ffmpeg, class_movie.search_res.keys())
		poolD.close()
		poolD.join()
	
	def thread_download_hand():
		class_movie.moveFolder('moviesHand')
		class_movie.combine_ts()

	thread_ffmpeg()
	
	
