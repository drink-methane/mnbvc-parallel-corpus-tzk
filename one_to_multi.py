import json
import os
from collections import defaultdict
import tools as tos

# 输入数据
file_path = r"C:\files\MNBVC\彼方的她localization_2025_4_23\localization_2025_4_23.txt"
content = tos.readfile(file_path, ".txt", encl=["utf-8"])
data = content.splitlines()
languages = ["zh", "en", "zh2"]

# 为每种语言创建字典
language_data = {lang: defaultdict(dict) for lang in languages}

for i in data:
    datal = i.split(",")
    for j in range(3):
        language_data[languages[j]][datal[0]] = datal[j+2]

# 为每种语言创建文件夹和JSON文件
for lang, data_dict in language_data.items():
    # 创建语言文件夹
    lang_dir = os.path.join(r"C:\files\MNBVC\彼方的她localization_2025_4_23", lang)
    os.makedirs(lang_dir, exist_ok=True)
    
    # 创建JSON文件路径
    json_path = os.path.join(r"C:\files\MNBVC\彼方的她localization_2025_4_23", lang_dir, "111.json")
    
    # 写入JSON文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dict(data_dict), f, ensure_ascii=False, indent=4)
    # print(lang_dir)