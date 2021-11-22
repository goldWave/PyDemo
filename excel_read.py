import xlrd, os

work_path = "C:\\Users\\Administrator\\Desktop"
ex_path = "C:\\Users\\Administrator\\Desktop\\[翻译]PC 문구_20210326.xlsx";
s_key = "KEY"
s_ind = "IND"
s_por = "POR"

def readExcel():

	workbook = xlrd.open_workbook(ex_path)
	sheet_names = workbook.sheet_names()
	for _name in sheet_names:
		sheet1_object = workbook.sheet_by_name(sheet_name=_name)
		
		# 获取sheet1中的有效行数
		nrows = sheet1_object.nrows
		print(_name )
		print(nrows)
		dic_key=[]
		dic_ind=[]
		dic_por=[]

		# 获取sheet1中的有效列数
		ncols = sheet1_object.ncols
		for _clos in range(0,ncols):

			cell_info = sheet1_object.cell_value(rowx=0, colx=_clos)

			if cell_info == s_key:
				for _index in range(1,nrows):
					_value = sheet1_object.cell_value(rowx=_index, colx=_clos)
					dic_key.append(_value)

			elif cell_info == s_ind:
				for _index in range(1,nrows):
					_value = sheet1_object.cell_value(rowx=_index, colx=_clos)
					dic_ind.append(_value)
			elif cell_info == s_por:
				for _index in range(1,nrows):
					_value = sheet1_object.cell_value(rowx=_index, colx=_clos)
					dic_por.append(_value)

			print(cell_info)
		# print(dic_key)

		if len(dic_key) > 0 and len(dic_ind) == len(dic_key):
			_ind_path = work_path + "\\" + _name + "___" + "IND.ini"
			with open(_ind_path, 'w', encoding='utf-8') as fp:
				fp.truncate()
				for i,v in enumerate(dic_key):
					_str = dic_key[i] + "=\"" + dic_ind[i] + "\"" 
					fp.write(_str)
					fp.write('\n')

		if len(dic_key) > 0 and len(dic_por) == len(dic_key):
			_por_path = work_path + "\\" + _name + "___" + "POR.ini"
			with open(_por_path, 'w', encoding='utf-8') as fp:
				fp.truncate()
				for i,v in enumerate(dic_key):
					_str = dic_key[i] + "=\"" + dic_por[i] + "\"" 
					fp.write(_str)
					fp.write('\n')
		# break
	# print(sheet_names)

if __name__ == '__main__':
	os.chdir(work_path)
	readExcel()