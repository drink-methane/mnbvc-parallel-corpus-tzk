import chardet#可用的
import os
import json
# import json5
import pysubs2
# import sys
# import struct
# from charset_mnbvc import api
# import re
import shutil

directory = r"D:\MNBVC\AzurLane\AzurLaneData"

def process_string(s):
    # 查找第一个逗号的位置
    first_comma_index = s.find(',')
    # 如果没有逗号，则返回空字符串
    if first_comma_index == -1:
        return ""
    # 提取第一个逗号之后的所有内容
    result = s[first_comma_index + 1:]
    # 如果结果非空且最后一个字符是逗号，则移除末尾的逗号
    if result and result[-1] == ',':
        result = result[:-1]
    return result

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        json_file_path = os.path.splitext(file_path)[0] + '.json'
        result_dict = {}
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encodindic = chardet.detect(raw_data)#这是一个字典，{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
            encodin = encodindic['encoding']
        # encodin = api.get_cn_charset(file_path)#encodin是编码方式的名字
        if file_path.endswith('.oxt'):#处理oxt文件
            try:
                with open(file_path, 'r', encoding = encodin) as f:# 读取.oxt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                for line in lines:
                    if '=' in line:
                        key, value = line.split('=', 1)# 使用split方法以等号为分隔符分割字符串
                        result_dict[key.strip()] = value.strip()# 将键值对添加到字典中
                    else:
                        pass#result_dict是一个对好的字典
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)#删除源文件
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.txt'):#处理txt文件
            try:
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取.txt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                ln = 0
                for line in lines:
                    key = str(ln)
                    ln = ln + 1
                    value = line.strip()
                    result_dict[key] = value
                    key = ""
                    value = ""
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.csv'):#处理csv文件
            try:
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取.txt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                for line in lines:
                    if "," in line:
                        key = line.split(',')[0]# 使用split方法以等号为分隔符分割字符串
                        value = process_string(line)
                        result_dict[key.strip()] = value.strip()# 将键值对添加到字典中
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.ssa'):#处理ssa文件
            try:
                subs = pysubs2.load(file_path, encoding=encodin)
                subtitles = {}
                for line in subs:
                    subtitles[line.start/1000] = line.text.strip()
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(subtitles, f, ensure_ascii=False, indent=4)
                os.remove(file_path)
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.ass'):#处理ass文件
            try:
                with open(file_path, 'r', encoding=encodin) as file:
                    ass_content = file.readlines()
                for line in ass_content:
                    if line.startswith("Dialogue: "):
                        parts = line[10:].split(",", 9)
                        result_dict[parts[1]] = parts[9].strip()
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.sub'):#处理sub文件
            try:
                # with open(file_path, 'r', encoding = encodin) as f:# 读取.txt文件内容
                #     lines = file.readlines()#content是str！
                # for line in lines:
                #     # 假设每行格式为 "start_time --> end_time|subtitle text"
                #     parts = line.split('|')
                #     time_range = parts[0].strip()
                #     subtitle_text = parts[1].strip()
                #     start_time, end_time = time_range.split('-->')
                #     start_time = start_time.strip()
                #     result_dict[start_time] = subtitle_text
                # with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                #     json.dump(result_dict, f, ensure_ascii=False, indent=4)
                # os.remove(file_path)
                # print(encodin)
                # print("成")
                pass
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.idx'):#处理idx文件
            try:
                # os.remove(file_path)
                # print("成")
                pass
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.uexp'):#处理uexp文件
            try:
                with open(file_path, 'r', encoding = "UTF-16 LE") as f:# 读取.oxt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                lines = lines[4:]
                tem_n = 1
                for line in lines:
                    if tem_n%2 == 1:
                        key = line
                    else:
                        if ";" in line:
                            line = line.split(';')
                            value = line[-1]
                        else:
                            value = line
                        result_dict[key.strip()] = value.strip()# 将键值对添加到字典中
                        key = ""
                        value = ""
                    tem_n = tem_n+1
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)#删除源文件
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        # elif file_path.endswith('.rar'):#处理rar文件
        #     os.remove(file_path)
        # elif file_path.endswith('.zip'):#处理zip文件
        #     os.remove(file_path)
        # elif file_path.endswith('.7z'):#处理7z文件
        #     os.remove(file_path)
        elif file_path.endswith('.pot'):#处理pot文件
            os.remove(file_path)
        elif file_path.endswith('.uasset'):#处理uasset文件
            os.remove(file_path)
        elif file_path.endswith('.locres'):#处理locres文件
            os.remove(file_path)
        elif file_path.endswith('.po'):#处理po文件
            os.remove(file_path)
        elif file_path.endswith('.archive'):#处理archive文件
            newpath = file_path.replace(".archive", ".json")
            shutil.move(file_path, newpath)
            pass
        elif file_path.endswith('.json'):#处理json文件
            try:
                key_l = []#需要添加文件等信息。
                result_dict = {}
                def pro(content, key_l):
                    '''
                    content: 得到的内容。
                    key_l: 一个列表，用于生成最后文件当中每一个键值对的key。
                    用来处理一个列表或者字典。
                    '''
                    global result_dict
                    key = '_'.join(key_l)
                    if isinstance(content, str):
                        result_dict[key.strip()] = content.strip()
                    elif isinstance(content, list):
                        i = 0
                        for item in content:
                            keyteml = key_l + [str(i)]
                            i+=1
                            pro(item, keyteml)
                    elif isinstance(content, dict):
                        for key in content.keys():
                            keyteml = []
                            keyteml = key_l + [key]#这样可以得到一个新列表，否则只会在原列表上操作。
                            pro(content[key], keyteml)
                    return 0
                with open(file_path, 'r', encoding = encodin) as f:# 读取.txt文件内容
                    content = json.load(f)
                pro(content = content, key_l = key_l)
                    # key = root.split("\\")[-1] + "_" + k
                    # key = key.strip()
                    # value = content["content"][k]
                    # value = value.strip()
                    # result_dict[key] = value
                os.remove(file_path)
                with open(file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                result_dict = {}
                # os.remove(file_path)
                print("成")
            except Exception as e:
                print("寄")
                print(file_path)
                # os.remove(file_path)
                # break