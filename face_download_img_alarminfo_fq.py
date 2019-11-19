# _*_ coding:utf-8 _*_
import os
import time
import datetime
#import numpy as np
import requests
import json
import urllib2

download_type=0 #0从告警查询接口请求下载,1为从json文件下载,需要配置json文件地址
#请求下载
start_time=1573639239000
end_time=1583900812000
#文件下载
alarm_info_json='alarm_infos.json'

download_dir='d:/test'

img_url='http://192.168.4.236:9083/wmzt_image?uid='
alarm_query_url='http://192.168.4.236:8712/fres/alarm/query'

def load_file(file):
    with open(file, 'rb') as f:
        return f.read()
    print 'open file error:%s' % file
    return ''

def reqUrl(requrl,reqdata):
    try:
        req = urllib2.Request(url=requrl, data=reqdata)
        result = urllib2.urlopen(req).read()
        return result
    except urllib2.URLError, e:
        print 'requrl error--->',str(e)
    return ''

def down_img(url,img_name):
    try:
        f = urllib2.urlopen(url) 
        data = f.read() 
        with open(img_name, "wb") as code: 
            code.write(data)
            return ''
        print 'download file error'
    except urllib2.URLError, e:
        print 'requrl error--->',str(e)
        return ''

#从文件解析下载
def download_from_file(file):
    json_data=load_file(file)
    if not json_data:
        return ''
    r=json.loads(json_data)
    if r['code'] != 0:
        return ''
    return r['data']

#从请求解析下载
def download_from_req(st,et):
    req_data={}
    req_data['start_time']=st
    req_data['end_time']=et
    req_data['videosource_ids']=[]
    #req_data['min_score']=0.5
    reqdata=json.dumps(req_data)
    rsp=reqUrl(alarm_query_url,reqdata)
    if not rsp:
        return ''
    r=json.loads(rsp)
    if r['code'] != 0:
        return ''
    return r['data']

if __name__=="__main__":
    
    print '------> start download type:%d<------'%(download_type)
    dataArry=None
    if download_type == 1:#从文件解析下载
        dataArry=download_from_file(alarm_info_json)
    else:
        dataArry=download_from_req(start_time,end_time)
    if not dataArry:
        print 'load data error'
    
    for i in range(0,len(dataArry)):
        print '------[%d]------'%(i)
        obj=dataArry[i]
        zp_idx=obj['idx']
        zp_tmp=obj['timestamp']
        zp_src=obj['src_id']
        zp_face=obj['face_id']
        zp_name=obj['videosource_name'] 
        zp_dir='%s/%d'%(download_dir,zp_idx)
        os.makedirs(zp_dir)
        zp_src_url=img_url+zp_src
        zp_face_url=img_url+zp_face
        zp_src_name=zp_dir+'/zp_src_%s.jpg'%(zp_tmp)
        zp_face_name=zp_dir+'/zp_face_%s.jpg'%(zp_tmp)
        down_img(zp_src_url,zp_src_name)
        down_img(zp_face_url,zp_face_name)
        
        result=obj['result']
        for j in range(0,len(result)):
            infoObj=result[j]
            db=infoObj['databaseName']
            retrieve=infoObj['retrieve']
            for k in range(0,len(retrieve)):
                gjObj=retrieve[k]
                gj_idx=gjObj['idx']
                gj_score=gjObj['score']
                gj_aid=gjObj['archives_id']
                gj_card=gjObj['id_card']
                gj_src=gjObj['src_uid']
                gj_face=gjObj['face_uid']
                
                gj_name=zp_dir+'/%d_%d_%s[%.3f]'%(gj_idx,gj_aid,gj_card,gj_score)
                gj_src_name=gj_name+'src.jpg'
                gj_face_name=gj_name+'face.jpg'
                gj_src_url=img_url+gj_src
                gj_face_url=img_url+gj_face
                down_img(gj_src_url,gj_src_name)
                down_img(gj_face_url,gj_face_name)
                
