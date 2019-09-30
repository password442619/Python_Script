# -*- coding: utf-8 -*-
import re
content = """
22_庞伟东_M3342.jpeg
23_李振辉_M3343.jpeg
24_张永_M3344.jpeg
25_欧阳晓明_M3345.jpeg
"""

def translate(str):
	line = str.strip()
	pattern = re.compile('[\u4e00-\u9fa5]')
	zh = "".join(pattern.split(line)).strip('.')
	outStr = zh
	return outStr
content_format = content.decode('utf-8')
print(translate(content_format))
