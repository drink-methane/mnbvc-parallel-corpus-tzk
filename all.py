from pathlib import Path
import sys
import os
import shutil
import tools as tos
import subprocess

LANGUAGES = { # 将需要按语言写死的部分，全部放到这一个表中，如果有组合数据，应该考虑用dict
    'zhs':('简体中文','zh_text'), # 如果需要语言重命名，或者打印语言信息，可以像这样把每个语言的设置拆成 tuple 来写。这个表的意义是建立语言的映射关系
    'en':('英文','en_text'),
    # 'FR':('法语','fr_text'),
    # 'DE':('德语','de_text'),
    # 'IT':('意大利语','it_text'),
    'ja':('日语','ja_text'),
    # 'KO':('韩语','ko_text'),
    # 'pl':('波兰语','pl'), # 填扩展字段里
    # 'PT':('葡萄牙语','pt_text'),
    # 'RU':('俄语','ru_text'),
    # 'ES':('西班牙语','es_text'),
    # 'ind':('印尼语','id_text'),
    # 'nb':('挪威语','no'), # 填扩展字段里
    # 'gre':('希腊语','el'), # 填扩展字段里
    # 'fi':('芬兰语','fi'), # 填扩展字段里
    # 'epo':('世界语','eo_text'),
    # 'nl':('荷兰语','nl_text'),
    'zht':('繁体中文','cht_text'),
    # 'vi':('越南语','vi_text'),
    # 'uk':('乌克兰语','uk'), # 填扩展字段里
    # 'tr':('土耳其语','tr'), # 填扩展字段里
    # 'th':('泰语','th_text'),
    # 'srp':('塞尔维亚语(拉丁字母)','sr'), # 填扩展字段里
    # 'srb':('塞尔维亚语(西里尔字母)','sr2'),
    # 'JP':('另一种日语','jp2'), # 填扩展字段里
    # 'es-MX':('墨西哥语','esmx'),
    # 'cs':('捷克语','cs'),# 填扩展字段里
    # 'hu':('匈牙利语','hu'),# 填扩展字段里
    # 'ar':('阿拉伯语','ar'),# 填扩展字段里
    # 'BP':('巴西葡语','pt_BR'),# 填扩展字段里
    # 'sv-SE':('瑞典语','sv'),# 填扩展字段里
    # 'da':('丹麦语','da'),# 填扩展字段里
    # 'be':('白俄罗斯语','be'),# 填扩展字段里
    # 'ca':('加泰罗尼亚语','ca'),# 填扩展字段里
    # 'gl':('加利西亚语','gl'),# 填扩展字段里
    # 'lt':('立陶宛语','lt'),# 填扩展字段里
    # 'ro':('罗马尼亚语','ro'),# 填扩展字段里
    # 'hr':('克罗地亚语','hr'),# 填扩展字段里
    # 'sk':('斯洛伐克语','sk'),# 填扩展字段里
    # 'sl':('斯洛文尼亚语','sl'),# 填扩展字段里
}
mate_dir = Path(r"D:\sandbox\data")
filename = "AstralParty.jsonl"
max_lines = 500000
max_size = 512

codes_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(codes_dir, 'DataCheck_MNBVC-main'))
log_dir = Path(os.path.join(codes_dir, "logs", "check_log.txt"))
log_file_dir = Path(os.path.join(codes_dir, "logs"))
mate_dir_l = mate_dir / Path(filename)
mate_dir_j = mate_dir / Path(r"jsonl_reworked")
mate_dir_jl = mate_dir_j / Path(filename)
tos.not_exist(mate_dir_j)
tos.not_exist(log_dir)
tos.not_exist(mate_dir / Path("check_log.txt"))

types = tos.check_file_type(mate_dir)
for ftype in types:
    if ftype != "json":
        tos.del_specific_filetype(folder = mate_dir, tartype = ftype)
for item in os.listdir(mate_dir):
    if item not in LANGUAGES:
        item_path = os.path.join(mate_dir, item)
        shutil.rmtree(item_path)

tos.put_in(LANGUAGES, filename, mate_dir)
command = ["python", "jsonlchk.py", "-d", str(mate_dir)]
subprocess.run(command, capture_output=True, text=True)
if tos.size_check(mate_dir_jl, max_size) == True:
    tos.cut(mate_dir_jl, mate_dir, filename, max_lines)
    mate_dir_l.unlink()
    shutil.rmtree(mate_dir_j)
    command = ["python", "jsonlchk.py", "-d", str(mate_dir)]
    subprocess.run(command, capture_output=True, text=True)
    for root, dirs, files in os.walk(mate_dir_j):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.jsonl'):
                shutil.move(file_path, os.path.join(mate_dir, os.path.basename(file_path)))
            else:
                pass
    shutil.rmtree(mate_dir_j)
else:
    mate_dir_l.unlink()
    shutil.copy(mate_dir_jl, mate_dir_l)
    shutil.rmtree(mate_dir_j)
command = ["python", "DataCheck_MNBVC/check_data.py", "--dataset", str(mate_dir)]
subprocess.run(command, capture_output=True, text=True)
shutil.move(log_dir, os.path.join(mate_dir, os.path.basename(log_dir)))
shutil.rmtree(log_file_dir)