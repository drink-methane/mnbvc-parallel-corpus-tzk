import json
import os
import concurrent.futures
import multiprocessing
from tqdm import tqdm
import tools as tos
import stat

'''
把文件全部变成utf-8编码。多进程+多线程处理。
'''

def process_single_file(file_path):
    """处理单个文件的函数，用于线程池"""
    try:
        if "." in file_path.split("\\")[-1]:
            extension = "." + file_path.split(".")[-1]
        else:
            extension = ""
        content=tos.readfile(file_path)
        os.chmod(file_path, stat.S_IWRITE)#去除只读属性
        os.remove(file_path)
        if extension == ".json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=4)
        else:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        return True

    except Exception as e:
        print(f"处理失败 {file_path}: {str(e)}")
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
    directory = r"C:\files\MNBVC\zimuku_ass_srt_classify_askmodel\111"
    ufiles = []

    print("正在扫描文件...")
    # 收集所有文件路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            ufiles.append(os.path.join(root, file))

    print(f"找到 {len(ufiles)} 个文件，开始处理...")

    # 设置批处理大小（每批处理xx个文件）
    batch_size = 4
    file_batches = [ufiles[i:i + batch_size] 
                    for i in range(0, len(ufiles), batch_size)]

    total_files = len(ufiles)
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