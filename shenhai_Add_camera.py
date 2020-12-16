#-*- coding: utf-8 -*-
import re
import xlrd
import xlwt
from xlutils.copy import copy

shh_row = 1
camera_xl = xlrd.open_workbook('./二期3000路人脸建设进展.xlsx')

sheetOrig = camera_xl.sheets()[2]
shenhaiOrig = camera_xl.sheets()[5]
col_values = sheetOrig.col_values(5)
shenhai_col = shenhaiOrig.col_values(2)

dic_col = {str(i):col_values[i] for i in range(0, len(col_values))}
shenhai_dic_col = {str(i):shenhai_col[i] for i in range(0, len(shenhai_col))}

dic_shh = {0:'xuhao', 1:'suoshuquyu', 2:'shexiangtoumingcheng', 3:'jierufangshi', 4:'IP_dizhi', 5:'duankouhao', 6:'jingdu', 7:'weidu', 8:'shexiangtoumoshi', 9:'RTSPliudizhi', 10:'suoshuNVR', 11:'tongdaohao', 12:'zhanghao', 13:'mima', 14:'guobiaobianma', 15:'jiexileixing', 16:'yundongfangxiang', 17:'changsuobiaoqian', 18:'leixingbiaoqian', 19:'changshang'}
dic_shh_values = {}

camera_file = open('./camera.txt')
for line in camera_file:
	add_name = line.replace('\n', '')
	if add_name == '':
		break
	number_name = list(dic_col.keys())[list(dic_col.values()).index(add_name)]
	row_values = sheetOrig.row_values(int(number_name))
	shenhai_number = list(shenhai_dic_col.keys())[list(shenhai_dic_col.values()).index(list(filter(lambda x: str(x).find(add_name)>0,list(shenhai_dic_col.values())))[0])]
	shenhai_row_values = shenhaiOrig.row_values(int(shenhai_number))
	
	dic_shh_values['xuhao'] = ''
	dic_shh_values['suoshuquyu'] = row_values[7]
	dic_shh_values['shexiangtoumingcheng'] = shenhai_row_values[2]
	dic_shh_values['jierufangshi'] = '本地接入'
	dic_shh_values['IP_dizhi'] = row_values[10]
	dic_shh_values['duankouhao'] = 8000
	dic_shh_values['jingdu'] = str(row_values[13])
	dic_shh_values['weidu'] = str(row_values[14])
	dic_shh_values['shexiangtoumoshi'] = '抓拍模式'
	dic_shh_values['suoshuNVR'] = ''
	dic_shh_values['tongdaohao'] = ''
	dic_shh_values['zhanghao'] = 'admin'
	dic_shh_values['mima'] = 'qdls1234'
	dic_shh_values['guobiaobianma'] = shenhai_row_values[14]
	dic_shh_values['RTSPliudizhi'] = 'rtsp://'+dic_shh_values['zhanghao']+':'+dic_shh_values['mima']+'@'+dic_shh_values['IP_dizhi']
	dic_shh_values['jiexileixing'] = '人脸'
	dic_shh_values['yundongfangxiang'] = ''
	dic_shh_values['changsuobiaoqian'] = ''
	dic_shh_values['leixingbiaoqian'] = ''
	dic_shh_values['changshang'] = ''
	if dic_shh_values['suoshuquyu'] == '中韩边防派出所':
		dic_shh_values['suoshuquyu'] = '海岸警察支队中韩派出所'
	elif dic_shh_values['suoshuquyu'] == '王哥庄派出所':
		dic_shh_values['suoshuquyu'] = '海岸警察支队王哥庄派出所'
	elif dic_shh_values['suoshuquyu'] == '沙子口派出所':
		dic_shh_values['suoshuquyu'] = '海岸警察支队沙子口派出所'
	else:
		print('所属区域（派出所）名称不变。')

	for shh_num in range(0, 20):
		workBook = xlrd.open_workbook('./点位上传表.xlsx')
		newWb = copy(workBook)
		newWs = newWb.get_sheet(2)
		newWs.write(shh_row, shh_num, dic_shh_values[dic_shh[shh_num]])
		newWb.save('./点位上传表.xlsx')
	shh_row = shh_row + 1
camera_file.close()
print('添加结束！')
