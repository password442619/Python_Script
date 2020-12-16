#-*- coding: utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy

shm_row = 1
#打开3000路建设进展表
camera_xl = xlrd.open_workbook('./二期3000路人脸建设进展.xlsx')
sheetOrig = camera_xl.sheet_by_name('3000路建设_进度明细表')
col_values = sheetOrig.col_values(5)

dic_shm = {0:'quyu', 1:'chengshi', 2:'yinqingdanyuan', 3:'wenhoushi', 4:'yonghuming', 5:'mima', 6:'shexiangtoumingcheng', 7:'shexiangtouIP', 8:'port', 9:'shexiangtouzuobiao', 10:'shebeibianma', 11:'caijileixing', 12:'shipinbofangdizhi', 13:'bendi'}
dic_shm_val = {}
dic_shm_val['yinqingdanyuan'] = input("请输入引擎单元:")

#生成摄像机名称一列的字典
dic_col = {str(i):col_values[i] for i in range(0,len(col_values))}

camera_file = open('./camera.txt')
for line in camera_file:
	add_name = line.replace('\n', '')
	if add_name == '':
		break
	number_name = list(dic_col.keys())[list(dic_col.values()).index(add_name)]	
	row_values = sheetOrig.row_values(int(number_name))
	
	dic_shm_val['quyu'] = row_values[7]
	dic_shm_val['chengshi'] = '青岛'
	dic_shm_val['wenhoushi'] = '非问候室'
	dic_shm_val['yonghuming'] = 'admin'
	dic_shm_val['mima'] = 'qdls1234'
	dic_shm_val['shexiangtoumingcheng'] = add_name
	dic_shm_val['shexiangtouIP'] = row_values[10]
	dic_shm_val['port'] = 8000
	dic_shm_val['shexiangtouzuobiao'] = str(row_values[13])+','+str(row_values[14])
	dic_shm_val['caijileixing'] = '海康抓拍模式'
	dic_shm_val['shipinbofangdizhi'] = 'rtsp://'+dic_shm_val['yonghuming']+':'+dic_shm_val['mima']+'@'+dic_shm_val['shexiangtouIP']
	dic_shm_val['shebeibianma'] = ''
	dic_shm_val['bendi'] = '是'
	
	#向深目批量添加摄像头内容
	for shm_num in range(0, 14):
		workBook = xlrd.open_workbook('./点位上传表.xlsx')
		newWb = copy(workBook)
		newWs = newWb.get_sheet(1)
		newWs.write(shm_row, shm_num,dic_shm_val[dic_shm[shm_num]])
		newWb.save('./点位上传表.xlsx')
	shm_row = shm_row + 1
camera_file.close()
print('添加结束!')
