import xml.etree.ElementTree as ET
import os
import json
import re

directory = r"D:\MNBVC\AstralParty\TextAsset"
pattern = r'\[[^\]]*\]'

for root, dirs, files in os.walk(directory):
    for file in files:
        lan = file.split(".")[0]
        filename = "TextAsset"
        file_path = os.path.join(root, file)
        json_file_path = os.path.join(root, lan, filename + '.json') 
        if not os.path.exists(os.path.join(root, lan)):
            os.makedirs(os.path.join(root, lan))
        result_dict = {}

        with open(file_path, 'r', encoding = 'UTF-8') as f:# 读取.oxt文件内容
            content = f.read()#content是str！

        xmlroot = ET.fromstring(content)
        for entry in xmlroot.findall("string"):
            key = entry.get('name')#re.sub(pattern, '', str(entry.text).strip())
            value = re.sub(pattern, '', str(entry.text).strip())
            result_dict[key] = value
        with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
            json.dump(result_dict, f, ensure_ascii=False, indent=4)
        result_dict = {}
        file_path = r""