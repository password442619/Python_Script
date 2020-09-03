#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import zipfile

reload(sys)
sys.setdefaultencoding('gbk')
print "Processing File is :" + sys.argv[1]
pathname = os.path.dirname(os.path.abspath(sys.argv[1]))

file = zipfile.ZipFile(sys.argv[1], "r")
for name in file.namelist():
  try:
    utf8name = name.decode('gbk', 'ignore')
  except UnicodeError as u:
    continue
  print "Extracting" + uft8name
  file.extract(utf8name, pathname)
  #解压zip文件，使用方法./unzipgbk.py XXX.zip
  #此脚本用于解决ubuntu系统解压windows上传的zip包，解压出的文件中文乱码问题。
