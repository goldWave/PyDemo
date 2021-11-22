#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import glob, os

destion = "C:\\Users\\jimbo\\source\\PRISMLiveStudio\\src\\prism\\main\\themes\\dark-theme\\images"

os.chdir(destion)
files = glob.glob("**/*.svg", recursive=True)

for x,v in enumerate(files):
	# print(v)
	with open(v, 'r', encoding='utf-8') as f:
		lines = f.readlines()
		findLine = '<g opacity="'
		# f.seek(0)
		for line in lines:
			if findLine in line:
				# f.write(line)
				print(v)
				print(line)
			# else:
				# print(v)
			# f.truncate()



