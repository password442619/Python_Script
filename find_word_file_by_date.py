#需求：查找文件夹里某个日期区间内的word文档，全部word的名称和路径列出来，比如7月5日到7月31日D盘下的所有word文档。
#coding=utf8
import os,sys
import time
g = os.walk(sys.argv[1])
def judge_time_file(path,file,update_time):
    if not file.endswith(('.doc','.docx')):
        return False
    start_time = time.mktime(time.strptime('2020-04-12 00:00:00',"%Y-%m-%d %H:%M:%S"))
    end_time = time.mktime(time.strptime('2020-05-23 00:00:00',"%Y-%m-%d %H:%M:%S"))
    #print(start_time, update_time, end_time)
    if start_time < update_time < end_time:
        return True
    return False
    
data_list = []

for path, dir_list, file_list in g:
    for file_name in file_list:
        local_time = os.stat(os.path.join(path, file_name)).st_mtime
        if judge_time_file(path, file_name, local_time):
            data_list.append([os.path.join(path, file_name), time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(local_time))])
data_list.sort(key=lambda x:x[1])
print(*data_list, sep='\n')
