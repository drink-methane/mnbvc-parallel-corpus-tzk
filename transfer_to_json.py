import chardet#可用的
import os
import json
# import json5
import pysubs2
# import sys
# import struct
# from charset_mnbvc import api
import re
import shutil

directory = r"C:\files\MNBVC\RiichiCity\RiichiCity"

def extract_outer_quotes(text):
    # 查找第一个双引号的位置
    first_quote = text.find('"')
    if first_quote == -1:
        return None  # 如果没有双引号，返回None
    
    # 查找最后一个双引号的位置
    last_quote = text.rfind('"')
    if last_quote == first_quote:
        return None  # 如果只有一个双引号，返回None

    # 提取两个最外层双引号之间的内容
    return text[first_quote + 1:last_quote]

def extract_before_first_quote(text):
    """
    提取字符串中第一个双引号之前的内容
    
    参数:
        text (str): 输入字符串
        
    返回:
        str: 第一个双引号之前的内容，如果没有双引号则返回原字符串
    """
    # 查找第一个双引号的位置
    quote_index = text.find('"')
    
    # 如果找到双引号，返回之前的内容
    if quote_index != -1:
        return text[:quote_index]
    else:
        # 如果没有双引号，返回整个字符串
        return text

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
                print("oxt成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.txt'):#处理txt文件
            try:
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取.txt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                n=0
                for line in lines:
                    value=line.strip()
                    key=str(n)
                    result_dict[key]=value
                    key=""
                    value=""
                    n=n+1
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                result_dict = {}
                # os.remove(file_path)
                print("txt成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.csv'):#处理csv文件
            try:
                # continue
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取.txt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                for line in lines:
                    if line.count(",") >= 2 and line.endswith(","):
                        linel = line.split(",")
                        key = linel[0]
                        value = linel[1].strip()
                        value = re.sub(r'\[.*?\]', '', value)#去除[]以及之间的内容。
                        value = re.sub(r'\{.*?\}', '', value)#去除{以及之间的内容}。
                        if "::" in value:
                            valuel = value.split("::")
                            value = valuel[1]
                        result_dict[key] = value# 将键值对添加到字典中
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                # os.remove(file_path)
                print("csv成")
            except Exception as e:
                print("寄", e)
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
                print("ssa成")
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
                print("ass成")
            except Exception as e:
                print("寄", e)
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
                # print("sub成")
                pass
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.idx'):#处理idx文件
            try:
                # os.remove(file_path)
                # print("idx成")
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
                print("uexp成")
            except Exception as e:
                print("寄")
                print(file_path)
                break
        elif file_path.endswith('.yml'):#处理yml文件
            try:
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取.oxt文件内容
                    content = f.read()#content是str！
                lines = content.splitlines()#lines是包含每一行的一个列表
                lines = lines[0:]
                for line in lines:
                    if line.count("\"") > 1:
                        value = extract_outer_quotes(line).strip()
                        key = extract_before_first_quote(line).strip()
                        result_dict[key] = value
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)#删除源文件
                print("yml成")
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
        elif file_path.endswith('.png'):#处理png文件
            os.remove(file_path)
        elif file_path.endswith('.uasset'):#处理uasset文件
            os.remove(file_path)
        elif file_path.endswith('.locres'):#处理locres文件
            os.remove(file_path)
        elif file_path.endswith('.po'):#处理po文件
            with open(file_path, 'r', encoding = encodin) as f:# 读取.txt文件内容
                content = f.read()
            lines = content.splitlines()#lines是包含每一行的一个列表
            ln = 1
            for line in lines:
                if line.startswith("#."):
                    key = line
                elif line.startswith("msgid"):
                    value = extract_outer_quotes(line)
                    result_dict[key] = value
                    key = ""
                    value = ""
            with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                json.dump(result_dict, f, ensure_ascii=False, indent=4)
            # print(type(content))
        elif file_path.endswith('.bundle'):#处理bundle文件
            os.remove(file_path)
        elif file_path.endswith('.tmp'):#处理tmp文件
            os.remove(file_path)
        elif file_path.endswith('.archive'):#处理archive文件
            newpath = file_path.replace(".archive", ".json")
            shutil.move(file_path, newpath)
            pass
        # elif file_path.endswith('.asset'):#处理asset文件
        #     os.remove(file_path)
        elif file_path.endswith('.lua'):#处理lua文件
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                table_start = content.find('{')
                table_end = content.rfind('}')
                if table_start != -1 and table_end != -1:
                    table_content = content[table_start + 1:table_end].strip()
                else:
                    raise ValueError("Invalid Lua table format")

                # Use regex to find all key = [[value]], pairs, allowing multiline values
                pattern = r'(\w+)\s*=\s*\[\[(.*?)\]\],'
                matches = re.findall(pattern, table_content, re.DOTALL)

                # Create dictionary from matches
                result_dict = {key.strip(): value.strip() for key, value in matches}
                    
                with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
                os.remove(file_path)
                print("lua成")
            except Exception as e:
                print("寄", e)
                print(file_path)
                break
        elif file_path.endswith('.json'):#处理json文件
            # os.remove(file_path)
            continue
            try:
                result_dict = {}
                with open(file_path, 'r', encoding = encodin) as f:# 读取.txt文件内容
                    content = json.load(f)
                for ke in content:
                    if "lang" in ke:
                        content[ke]=""
                os.remove(file_path)
                with open(file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(content, f, ensure_ascii=False, indent=4)
                result_dict = {}
                # os.remove(file_path)
                print("json成")
            except Exception as e:
                print("寄")
                print(file_path)
                # os.remove(file_path)
                # break
                # pass