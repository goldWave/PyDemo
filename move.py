# -*- coding: utf-8 -*-

import shutil
import os, io
import exifread
from PIL import Image, ImageDraw, ImageFont, ExifTags
import re
import datetime
import time
import whatimage
import pyheif
import piexif

Src_path="/Users/jimbo/Documents/waterPhoto"
wanttopath="/Users/jimbo/Documents/wanttoFlash"
time_key="EXIF DateTimeOriginal"

def exifread_infos(photo):
	f = open(photo, 'rb')
	tags = exifread.process_file(f)
	# print(tags)
	dateStr=""
	if time_key in tags:
		dateStr = tags[time_key].printable
		# print(photo + "           " + tags["Image Orientation"].printable)
		orien = tags["Image Orientation"].printable
		rotateData = "0"
		if "Rotated 90 CW" in orien:
			rotateData = "6"
		elif "Rotated 180" in orien:
			rotateData = "3"
		else:
			rotateData = "0"
		dateStr = dateStr + "," + rotateData;
	else:
		iName = os.path.basename(photo).split('.')[0]
		if "mmexport" in iName:
			timeStamp = re.sub('mmexport([0-9]+)$', r'\1', iName)
			iTime = int(timeStamp)
			timeArray = time.localtime(iTime/1000)
			dateStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		elif "微信图片_" in iName:
			d = re.sub('微信图片_([0-9]+)$', r'\1', iName)
			dateStr = datetime.datetime.strptime(d, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
		else:
			try:
				# print(iName)
				#2020-11-09 214158
				dateStr = datetime.datetime.strptime(iName, '%Y-%m-%d %H%M%S').strftime('%Y-%m-%d %H:%M:%S')
			except:
				dateStr = "2021-01-30 15:00:00"
				# print(photo)
	f.close()
	return dateStr


def in5_100(item):
	listDir = os.listdir(wanttopath+"/"+"5_100")	
	for _item in listDir:
		if item == _item:
			return True

	return False

def in6_64(item):
	listDir = os.listdir(wanttopath+"/"+"6_64")	
	for _item in listDir:
		if item == _item:
			return True

	return False

def in8(item):
	listDir = os.listdir(wanttopath+"/"+"8")	
	for _item in listDir:
		if item == _item:
			return True

	return False

def moveImg(srcPath, outPath, index):


	shutil.copy(srcPath, outPath)

def main():
	listDir = os.listdir(Src_path)
	out_ = Src_path + "/../output"
	# out_ = Src_path + "/output"

	if (not os.path.exists(out_)):
		os.mkdir(out_)

	i = 0
	for item in listDir:
		# src=Src_path+"/"+item
		# convertHECIToJpg(src)
		i = i+1
		src=Src_path+"/"+item
		is_64 = False
		is_8 = False
		is_100 = False
		time = exifread_infos(src)
		detail = str(i) + "?" + time + "." + item.split(".")[1]
		# print(detail)
		# continue
		if in5_100(item) == True:
			# print(item)
			is_100 = True
			moveImg(src, wanttopath+"/new/" + "5_100/" + detail, i)

		if in6_64(item) == True:
			# print(item)
			is_64 = True
			moveImg(src, wanttopath+"/new/" + "6_64/" + detail, i)
		if in8(item) == True:
			# print(item)
			is_8 = True
			moveImg(src, wanttopath+"/new/" + "8/" + detail, i)

		if is_64 == False and is_100 == False and is_8 == False:
			moveImg(src, wanttopath+"/new/" + "other/" + detail, i)




if __name__ == '__main__':
	main()