import sys, os

import sys, os, json
import time
from typing import List
from time import strftime
import uiautomation as auto
import subprocess
from ini_common_method import *
from ini_get_all_ini_structs import getAllDirInis

_file = r'C:\Users\Administrator\Documents\source\PRISMLiveStudio\src\prism\main\PLSPlatformApi\youtube\PLSPlatformYoutube.cpp'

_alertKeys = [':warning(', '::information(', ':question(', ':critical(']

_constKeys = ['const', 'define']

class JBAlertData:
    line = str()
    key = str()
    transKey = str()
    isINIFound = bool()

def process_get_alertLines(_file, printProgress, _alerts, lock):
        with open(_file, 'r', encoding='utf-8') as f:
            if printProgress == True:
                print(_file + "\t"+ str(threading.get_ident()))
            allLine = f.readlines()
            for x in allLine:
                for _key in _alertKeys:
                    if _key in x:
                        lock.acquire()
                        _alerts.append(x)
                        lock.release()

def penAndCheckUsedData_Process_process_get_alertLines(fileList, printProgress=False) -> list:
    """
    fileList = 所有文件的路径
    keyList = 查找的key
    isMacro = key 是否是宏
    return 没有使用的key
    这里主要的 耗时在 大字符串 搜索 子字符串里面，是cpu 密集型，所有用多进程
    而python 的锁导致多线程 访问cpu需要串行，所有多线程并没有进行时间优化
    """
    p = mp.Pool(mp.cpu_count()*2)
    m = mp.Manager()
    _alerts=m.list()
    _lock = m.Lock()

    for _file in fileList:
        p.apply_async(process_get_alertLines,args=(_file,printProgress,_alerts, _lock,))

    p.close()
    p.join()

    print(len(_alerts))

    return _alerts

def process_get_const_values(_file, printProgress, keyDic, _lines, lock):
        with open(_file, 'r', encoding='utf-8') as f:
            if printProgress == True:
                print(_file + "\t"+ str(threading.get_ident()))
            allLine = f.readlines()
            for x in allLine:
                for constKey in _constKeys:
                    if constKey in x:
                        for _key in keyDic.keys():
                            if keyDic[_key] > 0:
                                continue
                            if _key in x:
                                lock.acquire()
                                keyDic[_key] = 1
                                _lines.append(x)
                                lock.release()
                                break
                        break

def penAndCheckUsedData_Process_process_get_const_values(fileList, checkList,  printProgress=False) -> list:
    """
    fileList = 所有文件的路径
    keyList = 查找的key
    isMacro = key 是否是宏
    return 没有使用的key
    这里主要的 耗时在 大字符串 搜索 子字符串里面，是cpu 密集型，所有用多进程
    而python 的锁导致多线程 访问cpu需要串行，所有多线程并没有进行时间优化
    """
    _keyDic = {}
    for x in checkList:
        b = " " + x  + " = "
        _keyDic[b] = 0 
    
    p = mp.Pool(mp.cpu_count()*4)
    m = mp.Manager()
    _dic=m.dict(_keyDic)
    _lines=m.list()
    _lock = m.Lock()
    print(_dic)
    for _file in fileList:
        p.apply_async(process_get_const_values,args=(_file, printProgress, _dic, _lines, _lock,))

    p.close()
    p.join()

    print("_lines:", len(_lines))

    return _lines

#获取alert所在的行数据
def getAllAlerts():
    _allAlerts = []
    print(dir_all_alart_lines)
    _sets = set()
    if os.path.exists(dir_all_alart_lines):
        with open(dir_all_alart_lines, 'r', encoding='utf-8') as f:
            allLines = f.readlines()
            for x in allLines:
                x = x.strip('\n')
                _sets.add(x)

        for x in _sets:
            _allAlerts.append(x)
        return _allAlerts

    _li = findAllCheckFile()

    _list_i = findAllCheckFile_i()

    _allLists = []
    for x in _li:
        _allLists.append(x)
    for x in _list_i:
        _allLists.append(x)

    print(len(_allLists))
    for x in _allLists:
        if 'alert-view' in x:
            _allLists.remove(x)
            continue
        if 'qt-wrappers' in x:
            _allLists.remove(x)

    print(len(_allLists))
    
    _allAlerts = k_openAndCheckUsedData_Process(_allLists, False)

    with open(dir_all_alart_lines, 'w', encoding='utf-8') as fp:
        fp.truncate()
        for x in _allAlerts:
            x = x.strip('\n')
            x = x.strip(' ')
            x = x.strip('\t')
            x = x.strip(' ')
            if len(x) > 0:
                fp.write(x)
                fp.write('\n')
    return _allAlerts

def getalertModels():
    _lines = getAllAlerts()
    print("get all alert lines")

    _datas = []
    for x in _lines:
        model = JBAlertData()
        model.line = x
        model.isINIFound = False
        for _value in _alertKeys:
            if _value in x:
                b = x.split(_value,1)[1]
                b = b.split(',')[2]
                b = b.strip(' ')
                _localList = b.split('tr(')
                if len(_localList) > 1:
                    b = _localList[1]
                b = b.split('")')[0]
                b = b.split(')')[0]
                b = b.strip('"')
                b = b.replace('" "', '')
                b = b.replace('QT_UTF8(', '')
                b = b.replace('QString::fromStdString(', '')
                b = b.strip(' ')
                model.key = b
                break
        _datas.append(model)

    # for i in range(len(_datas)):
    #     _model = _datas[i]
    #     print(_model.key,"\t\t\t", _model.line)
    return _datas

def getAlertCheckKeys(_modelDatas) -> dict:
    _notFoundList = []
    for x in _modelDatas:
        if x.isINIFound == False:
            _notFoundList.append(x.key)

    #获取被const 的所在的行
    _alertLine = []
    if os.path.exists(dir_all_check_alart_lines):
        with open(dir_all_check_alart_lines, 'r', encoding='utf-8') as f:
            allLines = f.readlines()
            for x in allLines:
                x = x.strip('\n')
                _alertLine.append(x)
    else:
        _allCppFiles = findAllCheckFile()
        _alertLine = penAndCheckUsedData_Process_process_get_const_values(_allCppFiles, _notFoundList)
        with open(dir_all_check_alart_lines, 'w', encoding='utf-8') as fp:
            fp.truncate()
            for x in _alertLine:
                x = x.strip('\n')
                fp.write(x)
                fp.write('\n')


    _dic = dict()
    for x in _notFoundList:
        _dic[x] = ""

    for _line in _alertLine:
        for (k,v) in _dic.items():
            if len(v) > 0: #找到了对应的value
                continue
            addKey =  " " + k  + " = "
            if addKey in _line:
                a = _line.split(' = "')[1]
                a = a.split('";')[0]
                _dic[k] = a
    return _dic


def writeAlertAndIniToExcel(_dir, _alertModels = [JBAlertData], _inis = [iniData]):
    if os.path.exists(_dir):
        os.remove(_dir)

    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('main')

    st_orange_center = xlwt.easyxf('pattern: pattern solid;')
    st_orange_center.pattern.pattern_fore_colour = 51 #51 是橘黄色
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER #水平居中
    st_orange_center.alignment = alignment
    _allIndex = 0

    worksheet.write(_allIndex, 0, "key")
    worksheet.write(_allIndex, 1, "transKey")
    worksheet.write(_allIndex, 2, "code")
    worksheet.write(_allIndex, 3, "en")
    worksheet.write(_allIndex, 4, "kr")
    worksheet.write(_allIndex, 5, "es")
    worksheet.write(_allIndex, 6, "pt")
    worksheet.write(_allIndex, 7, "ID")

    st_orange = xlwt.easyxf('pattern: pattern solid;')
    st_orange.pattern.pattern_fore_colour = 51 #51 是橘黄色

    for data in _alertModels:
        _allIndex = _allIndex+1
        print(data.key, data.line, data.transKey)
        worksheet.write(_allIndex, 1, data.transKey)
        worksheet.write(_allIndex, 2, data.line)

        if data.isINIFound == True:
            worksheet.write(_allIndex, 0, data.key)
            for ini in _inis:
                if ini.keyStr == data.key or ini.keyStr == data.transKey:
                    
                    worksheet.write(_allIndex, 3, ini.s_en_US)
                    worksheet.write(_allIndex, 4, ini.s_ko_KR)
                    worksheet.write(_allIndex, 5, ini.s_es_ES)
                    worksheet.write(_allIndex, 6, ini.s_pt_BR)
                    worksheet.write(_allIndex, 7, ini.s_id_ID)
                    break
        else:
            worksheet.write(_allIndex, 0, data.key, st_orange)
    workbook.save(_dir)



if __name__ == '__main__':
    _datas = getalertModels()
    _inis = getAllDirInis()

    for data in _datas:
        if data.isINIFound == True:
            continue

        for ini in _inis:
            if ini.keyStr == data.key:
                data.isINIFound = True

    _dic = getAlertCheckKeys(_datas)
    for data in _datas:
        if data.isINIFound == True:
            continue
        if data.key in _dic and len(_dic[data.key]) > 0:
            data.transKey = _dic[data.key]
            data.isINIFound = True
            # print(_dic[data.key])

    # print("----")
    # for data in _datas:
    #     print(data.key, "\t\t\t\t", type(data))
    xibPath = dir_cache_path + "alerts.xls"
    writeAlertAndIniToExcel(xibPath, _datas, _inis)
    #     #     print("1")