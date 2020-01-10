#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import os
import shutil
reload(sys)  #重新加载系统
sys.setdefaultencoding('utf-8')  #设置系统默认编码格式为utf-8
scene_model_list = []
total_size = 0
db = MySQLdb.connect("192.168.1.138", "root", "Boyun@2019", "video_tagging_db", charset='utf8')
cursor = db.cursor()
sql = "select basic_video_info_all.video_name,basic_video_info_all.save_path,basic_video_info_all.video_size,basic_video_info_all.video_weather,basic_video_info_all.video_light,basic_video_info_all.time_area,basic_video_info_all.device_name from basic_video_info_all where basic_video_info_all.dt_id in (select device_tags_info.id from device_tags_info as device_tags_info where device_tags_info.device_area like %s);" % ("\"%普通道路%\"")
cursor.execute(sql) #执行sql语句
results = cursor.fetchall() #获取查询到的所有数据
dqml = os.getcwd() #获取当前目录
for row in results:
	video_name = row[0]
	save_path = row[1]
	video_size = row[2]
	video_weather = row[3]
	video_light = row[4]
	time_area = row[5]
	device_name = row[6]
	scene_model = row[3]+row[4]+row[5]+row[6]
	if scene_model not in scene_model_list:
		xsml = os.path.join(dqml, device_name, time_area, video_weather, video_light)
		#os.mkdir(xsml)  #创建xsml目录
		file_path = os.path.join(save_path, video_name)
		if "Gb" in video_size:
			num = video_size.split( )
			total_size = total_size + int(num[0])*1024
		elif "Mb" in video_size:
			num = video_size.split( )
			total_size = total_size + int(num[0])
		scene_model_list.append(scene_model)
#print str(scene_model_list).replace('u\'','\'').decode("unicode-escape")  #list中的中文字符串处理
#print "video_name=%s, save_path=%s, video_size=%s, scene_model=%s" % (video_name, save_path, video_size, scene_model)
db.close()
print total_size
#for row in results:
#	if "Gb" in row[2]:
#		convert = row[2].split( )
#		string = str(int(convert[0])*1024)
#		video_size = string+" Mb"
#		print "video_size: %s" % video_size
