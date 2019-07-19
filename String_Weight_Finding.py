# -*- coding: utf-8 -*-
import sys
import os
#with open('C:\Users\45439\Desktop\find.txt', 'r', encoding='utf-8')as f:
list = []
with open('C:/Users/45439/Desktop/find.txt', 'r', encoding='utf-8')as f:
	for line in f:
		list.append(line[0:13])

new_list = []
for i in list:
	if i not in new_list:
		new_list.append(i)
	else:
		print(i)
