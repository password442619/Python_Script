#适用于python3.5以上的python版本
import os
import sys
import io
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='utf-8')  #重新定义脚本的标准输出的编码格式为“utf-8”

with open('file_path.txt','r', encoding='utf-8') as f:
	lines = f.readlines()

with open('xsml.txt','r', encoding='utf-8') as ff:
	lines_ = ff.readlines()

for i in range(len(lines)):
	print(lines[i])
	print(lines_[i])
  
#打开file_path.txt和xsml.txt，分别从两个文件中读取每行并显示
