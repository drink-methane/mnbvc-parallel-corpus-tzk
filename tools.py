import json
import copy
from typing import List, Tuple, Union, Iterable, Sequence, Mapping
from types import NoneType
from datetime import datetime
import re#判断正则表达式
import os
import shutil
import hashlib

def put_in(LANGUAGES, filename, work_dir):
    def traverse_dict(data, curr_path: Tuple, out_all_path_map: Mapping[Tuple, Union[bool, int, float, str, NoneType]]):
        if isinstance(data, dict):
            # 如果是字典，遍历键值对
            for key, value in data.items():
                new_path = curr_path + (key, ) # json 中，一个 object 的 key 值要么是一个整数，要么是一个字符串
                traverse_dict(value, new_path, out_all_path_map)
        elif isinstance(data, list):
            # 如果是列表，遍历列表项
            for index, value in enumerate(data):
                new_path = curr_path + (index, )
                traverse_dict(value, new_path, out_all_path_map)
        else: # json 中的元素只有可能是 object, array, int, float, bool, string, null 其中之一，所以这里处理剩下的基本元素
            out_all_path_map[curr_path] = data

    def numorem(input_string):
        # 定义正则表达式
        pattern = r'^[0-9]*$'
        if not isinstance(input_string, str):
            return True
        if re.match(pattern, input_string):
            return True
        else:
            return False
        
    data_time = datetime.now().strftime("%Y%m%d")#日期

    template_parallel_corpus = {
        "文件名": filename,
        "it_text": "",
        "zh_text": "",
        "en_text": "",
        "ar_text": "",
        "nl_text": "",
        "de_text": "",
        "eo_text": "",
        "fr_text": "",
        "he_text": "",
        "ja_text": "",
        "pt_text": "",
        "ru_text": "",
        "es_text": "",
        "sv_text": "",
        "ko_text": "",
        "th_text": "",
        "id_text":"",
        "cht_text":"",
        "vi_text":"",
        "扩展字段": {}, # 别忘了最后要把扩展字段用 json.dumps(xx, ensure_ascii=False, sort_keys=True) 存成json字符串
        "时间": data_time
    }

    aligned_map = {} # 输出文件结果表, out_paths => parallel_corpus 的映射
    # 将结果按语言放到字典中，而不是对于每个结果写一条 zh_f、en_f、fr_f 之类的变量，这会使编码工作量成倍上升
    # 这种设计也能够保证以后若是有新的语言加入，只需要修改 LANGUAGE 表，新增一项即可
    for lang, (chinese_name, parallel_corpus_key) in LANGUAGES.items():
        # 对于简单的文件读写函数，不建议再加一层封装，你这里需要封装完全是因为你按语言写一条逻辑的写法冗余太多
        # 过渡封装会使整个脚本函数太多，在函数之间跳转很容易打断思路，使得阅读困难
        lang_dir = work_dir / lang
        for json_file in lang_dir.iterdir():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_content = json.load(f)
            except json.JSONDecodeError as e:
                print({str(e)}, json_file)
            # with open(json_file, 'r', encoding='utf-8') as f:
            #     json_content = json.load(f)
            out_paths = {}
            traverse_dict(json_content, (json_file.name ,), out_paths)
            for out_path, data_value in out_paths.items(): # 到这步，data_value就是文本内容
                if numorem(data_value) == True:#如果是数字或者空字符串
                    pass
                else:
                    aligned_row = aligned_map.setdefault(out_path, copy.deepcopy(template_parallel_corpus)) # 用 deepcopy 保证放进去的元素一定是一个拷贝，而不是引用
                    if parallel_corpus_key in aligned_row:
                        aligned_row[parallel_corpus_key] = data_value
                    else: # 在默认键值里没有的，放扩展字段
                        aligned_row['扩展字段'][parallel_corpus_key] = data_value
    with open(work_dir / filename, 'w', encoding='utf-8') as f:
        for out_path, aligned_row in aligned_map.items():
            # aligned_row['扩展字段']['k'] = '.'.join(map(str, out_path)) # 【可选】把对齐依据的key放进去，方便溯源
            aligned_row['扩展字段'] = json.dumps({'other_texts': aligned_row['扩展字段']}, ensure_ascii=False, sort_keys=True)
            json.dump(aligned_row, f, ensure_ascii=False, sort_keys=True)
            f.write('\n')
    return None

def not_exist(dir):
    if os.path.exists(dir) and dir.is_file():
        dir.unlink()
    elif os.path.exists(dir) and dir.is_dir():
        shutil.rmtree(dir)
    else:
        pass

def cut(input_file, output_dir, filenam, lines_per_file):
    filename = filenam.split('.')[0]
    with open(input_file, "r", encoding="utf-8") as infile:
        file_count = 0  # 文件计数器
        line_count = 0  # 行计数器
        outfile = None  # 输出文件对象
        for line in infile:
            if line_count % lines_per_file == 0:
                if outfile:
                    outfile.close()  # 关闭上一个文件
                output_file = os.path.join(output_dir, f"{filename}_{file_count}.jsonl")
                outfile = open(output_file, "w", encoding="utf-8")
                file_count += 1
            outfile.write(line)
            line_count += 1
        if outfile:
            outfile.close()
    return None

def size_check(file_path, standard_size):
    size = os.path.getsize(file_path)
    if size > standard_size*1024*1024:
        return True
    else:
        return None

def ha(input_string):#取哈希值
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hash_value = sha256_hash.hexdigest()
    return hash_value

def check_file_type(folder):
    types = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            ftype = file_path.split(".")[-1]
            if ftype not in types:
                types.append(ftype)
    return types

def del_specific_filetype(folder, tartype):
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            ftype = file_path.split(".")[-1]
            if ftype == tartype:
                os.remove(file_path)
    return 0