import os
import requests

def download_image(url, folder_path):
    # 获取文件名
    filename = os.path.join(folder_path, url.split('/')[-1])
    
    # 发送GET请求下载图片
    response = requests.get(url)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 写入图片文件
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"图片已下载到：{filename}")
    else:
        print("下载失败")
