#-*- coding: utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy

haib_row = 2
camera_xl = xlrd.open_workbook('./二期3000路人脸建设进展.xlsx')
sheetOrig = camera_xl.sheet_by_name('3000路建设_进度明细表')
col_values = sheetOrig.col_values(5)
dic_col = {str(i):col_values[i] for i in range(0, len(col_values))}

dic_haib = {0:'anzhuangweizhi', 1:'jiankongleixing', 2:'shexiangjibianhao', 3:'kongbai', 4:'shexiangjimingcheng', 5:'suoshufenju', 6:'shexiangjisuoshu', 7:'bumenchangsuo', 8:'jiankongquyuleixing', 9:'jiankongzhonglei', 10:'suoshuditutuceng', 11:'shexiangjiweizhileixing', 12:'didianxinxi', 13:'luxiangbaocunshijian', 14:'cunchushebei', 15:'jianshezhutidanwei', 16:'chengjiandanwei', 17:'jianshedanweifuzeren', 18:'fuzerenlianxifangshi', 19:'weihurensuoshudanwei', 20:'weihulianxiren', 21:'weihurenlianxifangshi', 22:'shexiangjichangshang', 23:'shexiangjixinghao', 24:'shexiangjijiage', 25:'shexiangjichaoxiang', 26:'shexiangjileixing', 27:'caijirenyuan', 28:'caijirenlianxifangshi', 29:'qudianfangshi', 30:'anzhuangshijian', 31:'qiyongshijian', 32:'shexiangjiyonghuming', 33:'shexiangjimima', 34:'shexiangjiIP', 35:'shexiangjiduankouhao', 36:'shexiangjiRTSPdizhi', 37:'zubodizhi', 38:'gaoqingtiaoduIP', 39:'gaoqingtiaoduport', 40:'shexiangjiSDKleixing', 41:'shifouzidaiyushua', 42:'shifoutuoguan', 43:'shifoutianwangjianshe', 44:'quanjingxiangjiguanlianqiuji', 45:'haikangpingtaixiangjiid', 46:'ziduanguanlian', 47:'shifoudaijian', 48:'shexiangjishiyongzhuangtai', 49:'shexiangjichaichuqingkuang', 50:'shifouzaileibiaozhongxianshi', 51:'shifouzaigiszhongxianshi', 52:'Xzuobiaozhi', 53:'Yzuobiaozhi', 54:'zifudiejia', 55:'yuyinguangbogongneng', 56:'shiyinqi'}
dic_haib_val = {}

camera_file = open('./camera.txt')
for line in camera_file:
	add_name = line.replace('\n', '')
	if add_name == '':
		break

	number_name = list(dic_col.keys())[list(dic_col.values()).index(add_name)]
	row_values = sheetOrig.row_values(int(number_name))
	dic_haib_val['anzhuangweizhi'] = '0'
	dic_haib_val['jiankongleixing'] = '1'
	dic_haib_val['shexiangjibianhao'] = row_values[27]
	dic_haib_val['kongbai'] = 'RL青岛崂山_'+ add_name
	dic_haib_val['shexiangjimingcheng'] = 'RX崂山_'+ add_name
	dic_haib_val['suoshufenju'] = '崂山分局'
	dic_haib_val['shexiangjisuoshu'] = row_values[7]
	dic_haib_val['bumenchangsuo'] = 'SXJSSBM2'
	dic_haib_val['jiankongquyuleixing'] = 'JKQYLX1'
	dic_haib_val['jiankongzhonglei'] = 'jklb1'
	dic_haib_val['suoshuditutuceng'] = '1'
	dic_haib_val['shexiangjiweizhileixing'] = 'SXJWZLX3'
	dic_haib_val['didianxinxi'] = '0'
	dic_haib_val['luxiangbaocunshijian'] = '30'
	dic_haib_val['cunchushebei'] = 'cc1'
	dic_haib_val['jianshezhutidanwei'] = 'zt2'
	dic_haib_val['chengjiandanwei'] = '深圳云天励飞技术有限公司'
	dic_haib_val['jianshedanweifuzeren'] = '曹钦'
	dic_haib_val['fuzerenlianxifangshi'] = '18503065021'
	dic_haib_val['weihurensuoshudanwei'] = '深圳云天励飞技术有限公司'
	dic_haib_val['weihulianxiren'] = '曹钦'
	dic_haib_val['weihurenlianxifangshi'] = '18503065021'
	dic_haib_val['shexiangjichangshang'] = '云天励飞'
	dic_haib_val['shexiangjixinghao'] = 'IFD-N2124-FcF'
	dic_haib_val['shexiangjijiage'] = '1000'
	dic_haib_val['shexiangjichaoxiang'] = 'SXJCX1'
	dic_haib_val['shexiangjileixing'] = 'SXJLX3'
	dic_haib_val['caijirenyuan'] = '赵增强'
	dic_haib_val['caijirenlianxifangshi'] = '186 6392 6383'
	dic_haib_val['qudianfangshi'] = 'QDFS1'
	dic_haib_val['anzhuangshijian'] = '43756'
	dic_haib_val['qiyongshijian'] = '43817'
	dic_haib_val['shexiangjiyonghuming'] = 'admin'
	dic_haib_val['shexiangjimima'] = 'qdls1234'
	dic_haib_val['shexiangjiIP'] = row_values[10]
	dic_haib_val['shexiangjiduankouhao'] = '8000'
	dic_haib_val['shexiangjiRTSPdizhi'] = 'rtsp://'+ dic_haib_val['shexiangjiyonghuming'] +':'+dic_haib_val['shexiangjimima']+'@'+dic_haib_val['shexiangjiIP']
	dic_haib_val['zubodizhi'] = row_values[29]
	dic_haib_val['gaoqingtiaoduIP'] = ''
	dic_haib_val['gaoqingtiaoduport'] = ''
	dic_haib_val['shexiangjiSDKleixing'] = '100'
	dic_haib_val['shifouzidaiyushua'] = '1'
	dic_haib_val['shifoutuoguan'] = '0'
	dic_haib_val['shifoutianwangjianshe'] = '0'
	dic_haib_val['quanjingxiangjiguanlianqiuji'] = ''
	dic_haib_val['haikangpingtaixiangjiid'] = ''
	dic_haib_val['ziduanguanlian'] = ''
	dic_haib_val['shifoudaijian'] = '0'
	dic_haib_val['shexiangjishiyongzhuangtai'] = 'SXJSYZT'
	dic_haib_val['shexiangjichaichuqingkuang'] = '0'
	dic_haib_val['shifouzaileibiaozhongxianshi'] = '1'
	dic_haib_val['shifouzaigiszhongxianshi'] = '1'
	dic_haib_val['Xzuobiaozhi'] = row_values[13]
	dic_haib_val['Yzuobiaozhi'] = row_values[14]
	dic_haib_val['zifudiejia'] = ''
	dic_haib_val['yuyinguangbogongneng'] = '0'
	dic_haib_val['shiyinqi'] = '0'
	for haib_num in range(0, 57):
		workBook = xlrd.open_workbook('./点位上传表.xlsx')
		newWb = copy(workBook)
		newWs = newWb.get_sheet(3)
		newWs.write(haib_row, haib_num, dic_haib_val[dic_haib[haib_num]])
		newWb.save('./点位上传表.xlsx')
	haib_row = haib_row + 1
camera_file.close()
print('添加结束！')

