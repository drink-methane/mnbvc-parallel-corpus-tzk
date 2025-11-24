import chardet
import os
import json
import concurrent.futures
import tempfile
import re
import multiprocessing
from tqdm import tqdm
# import shutil
import tools as tos
# import subprocess

def remove_html_tags(text):
    # 使用正则表达式移除所有<...>标签及其内容
    return re.sub(r'<[^>]*>', '', text)

def process_single_file(file_path):
    """处理单个JSON文件的函数，用于线程池"""
    file_type = ".txt"
    try:
        json_file_path = os.path.splitext(file_path)[0] + ".json"
        # os.remove(json_file_path)
        # return True
        # 检测文件编码
        content = tos.readfile(file_path, file_type)
        
        flattened_data = {}
        lines = content.splitlines()#lines是包含每一行的一个列表
        n=0
        for line in lines:
            value=line.strip()
            key=str(n)
            flattened_data[key]=value
            key=""
            value=""
            n=n+1

        # 使用临时文件确保操作原子性
        with tempfile.NamedTemporaryFile(
            mode='w', 
            encoding='utf-8',
            delete=False,
            dir=os.path.dirname(file_path),
            suffix='.tmp'
        ) as tmp_file:
            json.dump(flattened_data, tmp_file, ensure_ascii=False, indent=4)
            temp_name = tmp_file.name
        
        # 替换原文件
        os.replace(temp_name, json_file_path)
        if 'temp_name' in locals() and os.path.exists(temp_name):
            os.remove(temp_name)
        # os.remove(file_path)
        return True
    
    except Exception as e:
        print(f"处理失败 {file_path}: {str(e)}")
        # 清理临时文件（如果存在）
        if 'temp_name' in locals() and os.path.exists(temp_name):
            os.remove(temp_name)
        # os.remove(file_path)
        return False

def process_file_batch(file_batch):
    """处理一批文件的函数，每个进程内部使用线程池"""
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers= 4) as executor:
        # 提交所有任务
        futures = {executor.submit(process_single_file, file_path): file_path for file_path in file_batch}
        
        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            file_path = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"处理文件时发生错误 {file_path}: {str(e)}")
    
    return success_count, len(file_batch)

def main():
    directory = r"C:\files\MNBVC\米塔MiSide"
    global file_type
    file_type = ".txt"
    json_files = []

    print("正在扫描文件...")
    # 收集所有JSON文件路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                json_files.append(os.path.join(root, file))

    print(f"找到 {len(json_files)} 个" + file_type + "文件，开始处理...")

    # 设置批处理大小（每批处理xx个文件）
    batch_size = 24
    file_batches = [json_files[i:i + batch_size] 
                    for i in range(0, len(json_files), batch_size)]

    total_files = len(json_files)
    total_success = 0

    # 使用多进程池处理文件批次
    with multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2) as pool:
        # 使用tqdm显示进度条
        with tqdm(total=total_files, desc="处理文件") as pbar:
            # 处理每个批次
            for success_count, batch_size in pool.imap_unordered(process_file_batch, file_batches):
                total_success += success_count
                pbar.update(batch_size)
                pbar.set_postfix({"成功率": f"{total_success/total_files:.1%}"})

    print(f"处理完成! 成功: {total_success}/{total_files} ({total_success/total_files:.1%})")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn', force=True)
    main()