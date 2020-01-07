#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
#显示当前目录
dqml = os.getcwd()
#构建文件路径，不创建
xsml = os.path.join(dqml,'test')
#创建构造的目录
os.mkdir(xsml)
#更改工作目录
gggzml = os.chdir(xsml)
#移动文件
full_path = os.path.join(dqml,"file") #构建文件据对路径
shutil.move(full_path, xsml) #移动文件到创建的构建目录里
