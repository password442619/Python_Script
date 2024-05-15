import requests
import os
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from Downlod_Picture import download_image

# Suppress only the single InsecureRequestWarning caused by not verifying SSL certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def execute_kibana_query(query, username, password):
    url = 'https://IP:5601/api/console/proxy?path=/bigdata_event/_search&method=POST'  # 注意此处使用 POST 方法，并将路径包含在 URL 中
    headers = {
        'Content-Type': 'application/json',
        'kbn-version': '6.8.0'
    }
    auth = (username, password)
    session = requests.session()

    response = session.post(url, headers=headers, auth=auth, json=query, verify=False)  # 将查询体传递给 json 参数，并禁用 SSL 证书验证

    if response.status_code == 200:
        return response.json()
    else:
        print("Error executing query:", response.status_code)
        return None

# Your Kibana Dev Tools query
with open('11.txt', 'r') as file:
    for line in file.readlines():
        kibana_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "aid": {
                                    "value": line.rstrip()
                                }
                            }
                        }
                    ]
                }
            },
            "size": 200,
            "_source": ["imageUrl", "faceUrl"]
        }
        
        username = "elastic"
        password = "introcks1234"
        
        result = execute_kibana_query(kibana_query, username, password)
        face_urls = [hit['_source']['faceUrl'] for hit in result['hits']['hits']]
        image_urls = [hit['_source']['imageUrl'] for hit in result['hits']['hits']]
        #print(kibana_query)
        print(line.rstrip())
        folder_path = line.rstrip()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for i in image_urls:
            download_image(i, folder_path)
        for u in face_urls:
            download_image(u, folder_path)
        #print(image_urls)
        #print(face_urls)
