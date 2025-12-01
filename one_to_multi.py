import json
import os
from collections import defaultdict

# 输入数据
file_path = r"C:\files\MNBVC\PEAK\SerializedTermsData.json"
with open(file_path, 'r', encoding = "UTF-8") as f:# 读取文件内容
    content = json.load(f)
# data = content

languages = content["CURRENT_LANGUAGE"]
content["CURRENT_LANGUAGE"] = []

# 为每种语言创建字典
language_data = {lang: defaultdict(dict) for lang in languages}

# 处理数据行（跳过前两行标题行）
for key in content:
    parts = content[key]
    # 为每种语言添加条目
    if len(parts)<len(languages):
        continue
    for i in range(len(languages)):
        lang = languages[i]
        text = parts[i]
        language_data[lang][key] = text

# 为每种语言创建文件夹和JSON文件
for lang, data_dict in language_data.items():
    # 创建语言文件夹
    lang_dir = os.path.join(r"C:\files\MNBVC\PEAK", lang)
    os.makedirs(lang_dir, exist_ok=True)
    
    # 创建JSON文件路径
    json_path = os.path.join(r"C:\files\MNBVC\PEAK", lang_dir, "111.json")
    
    # 写入JSON文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dict(data_dict), f, ensure_ascii=False, indent=4)
    # print(lang_dir)