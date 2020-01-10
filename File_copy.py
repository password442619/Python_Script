import os
import sys
import io
import shutil
sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding='gb18030')  #更改脚本的标准输出为‘gb18030’
with open("file_path.txt",'r', encoding='utf-8') as f:
	lines = f.readlines()

with open("xsml.txt",'r', encoding='utf-8') as ff:
	lines_ = ff.readlines()

for i in range(len(lines)):
	xsml = lines_[i].strip("\n") #去掉每行后的回车符号
	file_path = lines[i].strip("\n") #同上
	xsml_ = os.path.join(xsml,file_path.split('\\')[-1]) #file_path用“\”为分隔符，取最后一位拼接到xsml目录里，赋值给xsml_
	shutil.copyfile(file_path,xsml_) #拷贝file_path为xsml_
	#print(xsml)
	#os.makedirs(xsml)
	#print(xsml)
	#print(lines_[i])
f.close()
ff.close()
