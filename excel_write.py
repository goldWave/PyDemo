import xlwt, os 

def createExcel():
	_dir = 'D:\\languageCache\\compare1.xls'

	if os.path.exists(_dir):
		os.remove(_dir)
	# 创建一个workbook 设置编码
	workbook = xlwt.Workbook(encoding = 'utf-8')
	# 创建一个worksheet
	worksheet = workbook.add_sheet('My Worksheet')

	# 写入excel
	# 参数对应 行, 列, 值
	# worksheet.write(0,0, label = 'theeeis is test')`

	for i in range(0, 100):
		st = xlwt.easyxf('pattern: pattern solid;')
		st.pattern.pattern_fore_colour = 51
		worksheet.write(i % 24, i // 24, 'Test text', st)



	# 保存
	workbook.save(_dir)

if __name__ == '__main__':
	createExcel()