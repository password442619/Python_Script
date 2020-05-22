#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from PIL import Image #PIL模块需要使用pip安装
import json

def cut_img(img_path, coord):  #传入图片绝对路径和对应的坐标值抠图
	img = Image.open(img_path)
	target_img = img.crop(coord)
	return target_img

def save_img(target_img, target_dir, target_name): #存图片
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	if not os.path.isfile(os.path.join(target_dir, target_name)):
		target_img.save(os.path.join(target_dir, target_name))

def excute_img(img_path, type_name, coord, target_path):
	if not os.path.exists(img_path):
		return
	try:
		targetImg = cut_img(img_path,coord)
		target_name = type_name
		print(target_name)
		save_img(targetImg, target_path, target_name)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	base_path = r'/Users/pangweidong/Desktop/图片抠图/标注图像/'
	for root, dirs, files in os.walk(base_path):
		for name in files:
			file_path = os.path.join(root, name) #文件的绝对路径
			base_file_name = os.path.splitext(name)[0] #去掉后缀的文件名字
			coord_file_path = os.path.join(root, '%s.txt' % base_file_name)
			image_file_path = os.path.join(root, '%s.jpg' % base_file_name)
 			#coordinate_file = os.path.join(base_path, "%s.txt" % name)
			f = open(coord_file_path, 'r')
			coord_content = f.readlines()[0]
			_ = coord_content[:-2].split(" ")
			x = _[1]
			y = _[2]
			w = _[3]
			h = _[4]
			f.close()
			#image_file = os.path.join(base_path, "%s.jpg" % name)
			img = Image.open(image_file_path)
			img_size = img.size
			hig = img_size[1]
			wid = img_size[0]
			coordinate = (int(float(x)*wid)-int(float(w)*wid/2), int(float(y)*hig)-int(float(h)*hig/2), int(float(x)*wid)+int(float(w)*wid/2), int(float(y)*hig)+int(float(h)*hig/2))
			new_image = os.path.join(root, "%s_new.jpg" % base_file_name)
			excute_img(image_file_path, new_image, coordinate, base_path)
      
#坐标信息x,y,w,h中的x,y值是中心点的坐标
