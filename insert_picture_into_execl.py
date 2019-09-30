# -*- codding: cp936 -*-
import os,sys
import xlsxwriter
directory = sys.argv[1]

i = 3
book = xlsxwriter.Workbook('person_import.xlsx')
sheet = book.add_worksheet('Sheet1')
for filename in os.listdir(directory):
	print('A%d' % i, os.path.join(directory,filename))
	sheet.insert_image('A%d' % i,os.path.join(directory,filename))
	i += 1
book.close()
#向person_import.xlsx中插入图片
#脚本后跟图片路径
