# coding = utf-8

import os, time
import shutil


"""
将 子文件夹内的所有视频 加上文件夹的 前缀，
然后拷贝到 out 目录
"""

def findAllCheckFile_inis(_dir_all_pre="/Users/jimbo/Documents/洗片/小马哥音视频"):
	""" 获取所有的 ini 文件的上级目录 """
	_allFiles = set()
	_li = list()

	for root, lists, files in os.walk(_dir_all_pre):
		# print(files)
		for file in files:
			# print(root, "\t" , file)
			if file.endswith('mp4') or file.endswith('ts'):
				_li.append((root, file))
			# if file == 'locale.ini':
			# 	continue
			# if os.path.splitext(file)[1] in ['.ini']:
			# 	_allFiles.add(root)
	return _li


def onlyMove(a: list):
	targetPath = '/Users/jimbo/Documents/洗片/output'

	index = 0
	for (_dir, name) in a:
		pre = _dir.split('/')[-1][:2]
		_desPath = targetPath + '/' + name
		print(_desPath)
		shutil.copy(_dir + '/' + name, _desPath)
		os.unlink(_dir + '/' + name) #删除文件

def moveAndRename(a):
	targetPath = '/Users/jimbo/Documents/洗片/output'

	index = 0
	for (_dir, name) in a:
		pre = _dir.split('/')[-1][:2]
		_desPath = targetPath + '/' + pre + '_' + name
		print(_desPath)
		shutil.copy(_dir + '/' + name, _desPath)
		os.unlink(_dir + '/' + name) #删除文件

if __name__ == '__main__':
	a = findAllCheckFile_inis()
	# moveAndRename(a)
	onlyMove(a)

