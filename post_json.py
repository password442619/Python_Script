# _*_ coding:utf-8 _*_
import urllib2
import json
import time
import os
for file_name in os.listdir("/data/select_video"):
	time.localtime(time.time())
	local_time = time.strftime('%Y%m%d%H%M%S%j',time.localtime(time.time()))
	TaskID = "SS"+local_time
	data = {"taskType": 3,"latitude": "36.06014911002","targetType": 4,"startTime": "2019-09-24 15:29:00","remark": "","endTime": "2020-01-01 00:00:00","deviceId": "37020000001321113003","deviceName": u"B4一层大厅","clip_count": 1,"taskId": "","longitude": "120.4008270711959","URL": u""}
	for taskId in data:
		data["taskId"] = TaskID
	for URL in data:
		data["URL"] = "/data/select_video/"+file_name
	print json.dumps(data).decode('unicode-escape')
	headers = {'Content-Type':'application/json'}
	request = urllib2.Request(url='http://192.168.1.201:18700/structure/submitTask',headers=headers,data=json.dumps(data))
	response = urllib2.urlopen(request)
	print response.read()
	time.sleep(10)
