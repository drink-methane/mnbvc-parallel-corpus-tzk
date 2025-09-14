import json
import os
from collections import defaultdict

# 输入数据
file_path = r"D:\MNBVC\Mirror1\TextAsset\Sys_Localization"
with open(file_path, 'r', encoding = "UTF-8") as f:# 读取文件内容
    content = f.read()
data = content

# 解析数据
lines = data.split('\n')
headers = lines[0].split('\t')
languages = headers[4:]  # 从第5列开始是语言列

# 为每种语言创建字典
language_data = {lang: defaultdict(dict) for lang in languages}

# 处理数据行（跳过前两行标题行）
for line in lines[2:]:
    if not line.strip():
        continue
    parts = line.split('\t')
    entry_id = parts[0]
    className = parts[1]
    mapProperties = parts[2]
    key = parts[3]
    
    # 为每种语言添加条目
    for i, lang in enumerate(languages):
        text = parts[4 + i]
        language_data[lang][entry_id] = text

# 为每种语言创建文件夹和JSON文件
for lang, data_dict in language_data.items():
    # 创建语言文件夹
    lang_dir = os.path.join(r"D:\MNBVC\Mirror1\TextAsset", lang)
    os.makedirs(lang_dir, exist_ok=True)
    
    # 创建JSON文件路径
    json_path = os.path.join(r"D:\MNBVC\Mirror1\TextAsset", lang_dir, "Sys_Localization.json")
    
    # 写入JSON文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dict(data_dict), f, ensure_ascii=False, indent=4)
    # print(lang_dir)