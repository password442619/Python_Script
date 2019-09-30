# -*- coding: utf-8 -*-
import os 
import sys
import argparse
import re

def translate(str):
	line = str.strip()
	pattern = re.compile('[\u4e00-\u9fa5]')
	zh = "".join(pattern.split(line)).strip()
	outStr = zh
	return outStr

def main(args):
    for filename in os.listdir(args.path):
		name_tmp = filename.split('.')
		name = name_tmp[0]
		stu_num_tmp = name.split('_')
		stu_num = stu_num_tmp[1]
		stu_name = translate(name)
		print(stu_name)
		#print(stu_num)
def parser_arguments(argv):
    parser = argparse.ArgumentParser()
    #参数--path
    parser.add_argument('--path',dest='path',type=str,default='/Users/pangweidong/Desktop/test',help='默认目录/Users/pangweidong/Desktop/test')
    #参数--num
    parser.add_argument('--num',dest='num',type=int,default=100,help='默认输出个数')
    return parser.parse_args(argv)



if __name__ == '__main__':
    main(parser_arguments(sys.argv[1:]))
