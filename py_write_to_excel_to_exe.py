# coding = utf-8

r"""
将所有ini文件 的key value 混合比对 写进 excel 文件

打包命令: pyinstaller -F "D:\pythonDemo\pysrc\py_write_to_excel_to_exe.py" "D:\pythonDemo\pysrc\ini_common_method.py"


使用方法: D:\destion\dist\py_write_to_excel_to_exe.exe --only=True -O="C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\" -D="D:\destion\dist\languages.xls"

param: -O ini 文件的上级目录，地址后面必须以 \\ 结尾 
param: -D 输出的excel 的地址。
param: --only 可选，默认True 是否只输出 特定 这几种en-US., ja-JP, id-ID,ko-KR,pt-BR 语言，否者输出文件夹所有ini文件
"""

import os,sys,glob
import argparse
from ini_common_method import *

s_ini_paths_only = ["en-US.ini", "ja-JP.ini", "id-ID.ini","ko-KR.ini","pt-BR.ini"]
# dir_common_pre = "C:\\Users\\Administrator\\source\\PRISMLiveStudio\\src\\prism\\main\\data\\locale\\"
# s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
# s_write_path_excel = "D:\\languageCache\\all_language.xls"

def writeDiffToExcel(_inis, _to_excel_path):
    #多个ini 互相比较，将 差异 的地方输出到 excel

    _name = ["KEYS"]
    for x in _inis:
        _name.append(x.split("\\")[-1])

    _dics = []
    for x in _inis:
        _dics.append(getINIKeyValuesDict(x))

    _mores = [_dic.keys() for _dic in _dics]
    writeCompareKeyToExcel(_to_excel_path, _name, _mores, _dics, _isWriteAll=True)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='将所有ini文件写入 同一个 excel 中')
    parser.add_argument("-O", type=str, default='', help='ini 文件的上级目录，地址后面必须以\\结尾')
    parser.add_argument("-D", type=str, default='', help='excel 的输出目录')
    parser.add_argument("--only", type=str2bool, default=True ,help='默认为True。 是否只输出 en-US., ja-JP, id-ID,ko-KR,pt-BR 这几种语言，否者输出文件夹所有ini文件')
    args = parser.parse_args()

    dir_common_pre = args.O
    s_write_path_excel = args.D
    _isOnlyIni = args.only
    print("--only=" + str(_isOnlyIni))
    print("-O=" + args.O)
    print("-D=" + args.D)

    if dir_common_pre == "" or s_write_path_excel == "":
        print("----- param -O or -D is empty-------")
        exit()

    s_ini_paths = [dir_common_pre + x for x in s_ini_paths_only]
    if args.only == False:
        s_ini_paths = glob.glob(dir_common_pre + "*.ini", recursive=False)

    writeDiffToExcel()
    print("写入成功，地址：" + s_write_path_excel)
    print("done.")