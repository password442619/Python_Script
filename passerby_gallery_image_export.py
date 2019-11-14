# -*- coding:utf-8 -*-

'''
脚本说明：
适合于导出wmfe路人库里的原图与人脸图，存放在当前目录
原图与人脸图的文件名字会有face_id进行对应存储
'''

import urllib
import requests
import time
import json
from jsonpath import jsonpath
import datetime

# 需要修改路人库名，服务ip,port信息
url = 'http://192.168.4.218:8712/fres/face_lib/retrieve'     # 获取路人库数据的接口
headers = {"Host": "192.168.4.218:8712"}
headers1={'Content-Type': 'application/json'}

# 需要修改为想要读取内容的路人库库名
facedb_names="star1112"                # 路人库名称
print (u"程序开始时间：%s"%datetime.datetime.now() )    # 记录程序运行开始时间

data={
 "facedb_names":[facedb_names],
 "videosource_id":"",
     "ts_begin":1583217569000,     # 0代表库里从头开始的所有数据，也可以修改下发的任务的开始时间
     "ts_end":1596265847000,       # 结束时间
     "sortparam":1,
     "reverse":1,
     "max_rec":200,
     "min_sim":0.3,
     "feature":""
 }

r = requests.post(url, data=json.dumps(data),headers=headers)
raw=r.text
json_data = json.loads(raw)      # 把返回的结果以json格式展示
code=(json_data.get('code'))     # 判断接口返回code是否正确
if code==0:
    face_id = jsonpath(json_data, "$..face_id")      # 获取返回的face_id
    uri_face = jsonpath(json_data, "$..uri_face")    # 获取返回的uri_face
    uri_src = jsonpath(json_data, "$..uri_src")      # 获取返回的uri_src
    print(face_id)
    count = len(face_id)
    print("-------------------------------------------------------------------------------")
    print(u"抓拍目标数共计:%s" % count)       # 计算路人库内抓拍总数
    print("-------------------------------------------------------------------------------")
    a=0
    b=0
    for f in face_id:
        faceimg_name = uri_face[a]
        srcimg_name = uri_src[b]
        print(faceimg_name)
       # print(srcid)
        faceid_url = ("http://192.168.4.218:8083/wmzt_image?uid=" + faceimg_name)
        srcid_url = ("http://192.168.4.218:8083/wmzt_image?uid=" + srcimg_name)
        # print(imageurl)
        faceimg_name1=faceimg_name.replace('|','')
        faceimg_name2=faceimg_name1.replace('/','')
        srcimg_name1=srcimg_name.replace('|','')
        srcimg_name2 =srcimg_name1.replace('/', '')
        urllib.urlretrieve(faceid_url, filename=str(f)+'___'+faceimg_name2+".jpg")
        urllib.urlretrieve(srcid_url, filename=str(f)+'___'+srcimg_name2+ ".jpg")
        a = a + 1
        b = b + 1
else:
    print(u"查询路人库请求失败")
