# -*- coding: utf-8 -*-
import os
import shutil #文件移动，拷贝等操作所需要的modul

photo_path_list = []
with open("photo.txt", "r") as photo_path:
	for i in photo_path:
		photo_path_list.append(i[:-1])

class_list = []
with open("result_new.txt", "r") as result:
	for i in result:
		result_dict = eval(i) #将字符型i转化为class型，并赋值给result_dict字典
		if "data" in result_dict:
			data_dict = result_dict["data"]
			class_list.append(data_dict["cluster_id"])
		else:
			class_list.append("0")

for i in range(3929):
	ph_path = os.path.join('/Users/pangweidong/Desktop/store_as_needed', str(photo_path_list[i]))
	image_name = os.path.basename(ph_path)
	cl_path = os.path.join('/Users/pangweidong/Desktop/store_as_needed', str(class_list[i]), image_name)
	shutil.copy(ph_path, cl_path)
  
#根据给定的photo.txt和result_new.txt两个文件中的内容进行文件分类操作。
