
import glob, os

destion = "D:\\pythonDemo\\images"

os.chdir(destion)
files = glob.glob("**.jpg", recursive=False)

for x,v in enumerate(files):
	# print(v)
	re = v
	os.rename(v, re.replace('.jpg', '-4k.jpg'))
	# os.rename(v, )
	# with open(v, 'r', encoding='utf-8') as f:
	# 	lines = f.readlines()
	# 	findLine = '<g opacity="'
	# 	# f.seek(0)
	# 	for line in lines:
	# 		if findLine in line:
	# 			# f.write(line)
	# 			print(v)
	# 			print(line)
			# else:
				# print(v)
			# f.truncate()



