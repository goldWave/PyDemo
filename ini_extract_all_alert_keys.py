import sys, os

import sys, os, json
import time
from typing import List
from time import strftime
import uiautomation as auto
import subprocess
from ini_common_method import *
from ini_get_all_ini_structs import getAllDirInis

#_file = r'C:\Users\Administrator\Documents\source\PRISMLiveStudio\src\prism\main\PLSPlatformApi\youtube\PLSPlatformYoutube.cpp'

_alertKeys = [':warning(', '::information(', ':question(', ':critical(']

_constKeys = ['const', 'define']

_chanenlKey = 'Channels.'

_hands_trans_keys = (
    {"key": 'PLSAlertView::Button button = PLSMessageBox::question(this, QString::fromUtf8(Str("Basic.Settings.Audio.MultichannelWarning.Title")), warningString);', 'isSplite':False, "gotKeys":["Basic.Settings.ProgramRestart", 'Basic.Settings.Audio.MultichannelWarning', 'Basic.Settings.Audio.MultichannelWarning.Confirm']},
    {"key": 'PLSAlertView::Button button = PLSMessageBox::question(this, SIMPLE_OUTPUT_WARNING("Lossless.Title"), warningString);', 'isSplite':False, "gotKeys":["Basic.Settings.Output.Simple.Warn.Lossless", 'Basic.Settings.Output.Simple.Warn.Lossless.Msg']},
    {"key": 'PLSAlertView::Button button = PLSMessageBox::question(this, QString::fromUtf8(Str("Basic.Settings.Output.Simple.Warn." "Lossless.Title")), warningString);', 'isSplite':False, "gotKeys":["Basic.Settings.ProgramRestart", 'Basic.Settings.Audio.MultichannelWarning', 'Basic.Settings.Audio.MultichannelWarning.Confirm']},    
    {"key": 'PLSAlertView::Button button = PLSMessageBox::question(this, QTStr("Basic.Settings.Audio.MultichannelWarning.Title"), warningString);', 'isSplite':False, "gotKeys":["Basic.Settings.ProgramRestart", 'Basic.Settings.Audio.MultichannelWarning', 'Basic.Settings.Audio.MultichannelWarning.Confirm']},
    {"key": 'return PLSAlertView::Button::Ok == PLSMessageBox::question(parent, QTStr("ConfirmRemove.Title"), name, text, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':False, "gotKeys":["Basic.Settings.ProgramRestart", 'Basic.Settings.Audio.MultichannelWarning', 'Basic.Settings.Audio.MultichannelWarning.Confirm']},
    {"key": 'return PLSAlertView::question(getMainView(), tr("Confirm"), txt, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel) != PLSAlertView::Button::Ok;', 'isSplite':True, "gotKeys":["main.message.exit_broadcasting_alert", 'main.message.exit_virtual_camera_on_alert']},    
    {"key": 'button = PLSMessageBox::question(this, QTStr("ConfirmRemove.Title"), oldName, text, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["main.message.exit_broadcasting_alert", 'main.message.exit_virtual_camera_on_alert']},
    {"key": 'button = PLSMessageBox::question(this, QTStr("ConfirmRemove.Title"), QString::fromStdString(oldName), text, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["main.message.exit_broadcasting_alert", 'main.message.exit_virtual_camera_on_alert']},
    {"key": 'return (PLSAlertView::Button::Yes == PLSAlertView::question(parent, QObject::tr("Alert.Title"), tipInfo, PLSAlertView::Button::Yes | PLSAlertView::Button::Cancel));', 'isSplite':False, "gotKeys":["需要柱超手动check"], 'isNeedCheck': True},    
    {"key": 'return PLSAlertView::Button::Ok == PLSMessageBox::question(parent, QTStr("ConfirmRemove.Title"), text, name, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["ConfirmRemove.Text.title"]},    
    {"key": 'return PLSAlertView::Button::Ok == PLSMessageBox::question(getMainView(), QTStr("ConfirmRemove.Title"), text, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["ConfirmRemove.Text.title"]},    
    {"key": 'button = PLSMessageBox::question(this, QTStr("ConfirmRemove.Title"), text, QString::fromStdString(oldName), PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["ConfirmRemove.Text.title"]},   
    {"key": 'button = PLSMessageBox::question(this, QTStr("ConfirmRemove.Title"), text, oldName, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel);', 'isSplite':True, "gotKeys":["ConfirmRemove.Text.title"]},
    {"key": 'PLSAlertView::warning(this, tr("Alert.Title"), tr(result == NoNdiRuntimeFound ? "Ndi.Source.NoRuntimeFound" : "Ndi.Source.RuntimeInitializeFail"));', 'isSplite':True, "gotKeys":["Ndi.Source.NoRuntimeFound", 'Ndi.Source.RuntimeInitializeFail']},
    {"key": 'main, [this, error_reason]() { PLSAlertView::critical(this->main->getMainView(), QTStr("Output.StartRecordingFailed"), error_reason); }, Qt::QueuedConnection);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},   
    {"key": 'PLSAlertView::warning(this, name, errorString);', 'isSplite':True, "gotKeys":["laboratory.plugin.beauty.error.no.face", 'laboratory.plugin.beauty.error.out.of.range']},    
    {"key": 'PLSMessageBox::critical(this, QTStr("Output.RecordError.Title"), QT_UTF8(errorMessage));', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},       
    {"key": 'PLSMessageBox::information(this, QTStr("Output.ConnectFail.Title"), QT_UTF8(errorMessage));', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},   
    {"key": 'PLSAlertView::warning(getAlertParent(), QTStr("Alert.Title"), errorAlert);" : "Ndi.Source.RuntimeInitializeFail"));', 'isSplite':True, "gotKeys":['LiveInfo.live.error.stoped.byRemote']},
    {"key": 'PLSAlertView::warning(App()->getMainView(), data.first, data.second);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(App()->getMainView(), title, text);', 'isSplite':True, "gotKeys":['Auth.InvalidScope.Text']},
    {"key": 'PLSAlertView::warning(PLSBasic::Get(), QTStr("Alert.Title"), strError);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'alertResult = PLSAlertView::warning(PLSBasic::Get(), QTStr("Alert.Title"), strError);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(toplevelView, tr("Alert.Title"), result.second);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(pls_get_toplevel_view(this), tr("Alert.Title"), result.second);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'auto ret = PLSAlertView::question(nullptr, tr("Confirm"), questionContent, {{PLSAlertView::Button::Yes, tr("ResolutionGuide.ApplyNowBtn")}, {PLSAlertView::Button::Cancel, tr("Cancel")}});', 'isSplite':True, "gotKeys":['ResolutionGuide.QuestionContent', 'ResolutionGuide.ApplyNowBtn']},
    {"key": 'PLSAlertView::information(nullptr, QTStr("Remux.NoFilesAddedTitle"), QTStr("Remux.NoFilesAdded"), PLSAlertView::Button::Ok);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(App()->getMainView(), source_name, "Save image failed. Please try again.");', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(this, QTStr("Alert.Title"), str);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'QMessageBox::warning(OBSBasic::Get(), title, text);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(getAlertParent(), QTStr("Alert.Title"), errorAlert);', 'isSplite':True, "gotKeys":['LiveInfo.live.error.stoped.byRemote']},
    {"key": 'QMessageBox::warning(OBSBasic::Get(), title, text);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(parent, tr("Blacklist.Alert.Notice"), notice);', 'isSplite':True, "gotKeys":["Blacklist.ThirdParty.Plugins.Crashed", 'Blacklist.ThirdParty.Plugins.Warning']},
    {"key": 'PLSAlertView::warning(alertParent, QTStr("Alert.Title"), msg);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'if (PLSAlertView::Button::Ok != PLSMessageBox::question(getMainView(), QTStr("NoSources.Title"), msg, PLSAlertView::Button::Ok | PLSAlertView::Button::Cancel)) {', 'isSplite':False, "gotKeys":["NoSources.Text", 'NoSources.Text.AddSource']},
    {"key": 'PLSAlertView::warning(window, obs_module_text("Captions.Error.GenericFail"), text.c_str());', 'isSplite':False, "gotKeys":["需要手动check， catch 内部字符串"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::Button button = PLSAlertView::warning(getMainView(), QTStr("ResizeOutputSizeOfSource"),', 'isSplite':False, "gotKeys":["ResizeOutputSizeOfSource.Text", "ResizeOutputSizeOfSource.Continue"]},
    {"key": 'PLSMessageBox::information(this, RP_NO_HOTKEY_TITLE, RP_NO_HOTKEY_TEXT);', 'isSplite':True, "gotKeys":["Output.ReplayBuffer.NoHotkey.Msg"]},
    {"key": 'pls_get_main_view(), [obj]() { PLSAlertView::warning(pls_get_main_view(), tr("Notice"), obj.mText); }, Qt::QueuedConnection);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(this, tr("Alert.Title"), msg);', 'isSplite':True, "gotKeys":["task.timeout", 'task.crash']},
    {"key": 'ret = PLSAlertView::warning(nullptr, QTStr("Alert.Title"), model.showStr, buttons);', 'isSplite':True, "gotKeys":["LiveInfo.live.Check.AutoStart.Rrmp", 'LiveInfo.live.Check.AutoStart.Rrmp', 'LiveInfo.live.Check.AutoStart.Channel', 'LiveInfo.live.Check.AutoStart.Both.ChannelAndRtmp']},
    {"key": 'PLSAlertView::warning(alertParent, QTStr("Alert.Title"), m_showCustomMsg);', 'isSplite':True, "gotKeys":['已废弃的接口']},
    {"key": 'PLSAlertView::critical(main->getMainView(), QTStr("Output.StartRecordingFailed"), error_reason);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::Button button = PLSMessageBox::question(this, QTStr("Confirm"), content, PLSAlertView::Button::Yes | PLSAlertView::Button::No);', 'isSplite':True, "gotKeys":["laboratory.item.open.restart.text", 'laboratory.item.install.finished.restartapp.content']},
    {"key": 'PLSAlertView::warning(nullptr, QTStr("Alert.Title"), content);', 'isSplite':False, "gotKeys":["nshopping需要手动check"], 'isNeedCheck': True},
    {"key": 'QMessageBox::information(nullptr, QObject::tr("Tips"), \\', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(this, getInfo(errorMap, ChannelData::g_errorTitle), getInfo(errorMap, ChannelData::g_errorString));', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::critical(this, QTStr("Output.StartStreamFailed"), message);', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(PLSBasic::Get(), QTStr("Alert.Title"), content);', 'isSplite':True, "gotKeys":["LiveInfo.live.error.stoped.byRemote"]},
    {"key": 'if (PLSMessageBox::question(this, QTStr("Remux.FileExistsTitle"), message) != PLSAlertView::Button::Yes)', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'PLSAlertView::warning(getMainWindow(), getInfo(errorMap, g_errorTitle), getInfo(errorMap, g_errorString));', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
    {"key": 'if (PLSAlertView::warning(PLSBasic::Get(), QTStr("Alert.Title"), message, buttons, PLSAlertView::Button::Ok) == PLSAlertView::Button::Ok) {', 'isSplite':False, "gotKeys":["需要手动check"], 'isNeedCheck': True},
)

class JBAlertData:
    line = str()
    key = str()
    transKey = list()
    isINIFound = bool()
    isSplite = True #多个key是否是分开的

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

    # _list_i = findAllCheckFile_i() #这里不需要 .i 文件

    _allLists = []
    for x in _li:
        _allLists.append(x)
    # for x in _list_i:
    #     _allLists.append(x)

    for x in _allLists:
        if 'alert-view' in x:
            _allLists.remove(x)
            continue
        if 'qt-wrappers' in x:
            _allLists.remove(x)
        if 'PLSTestModule' in x:
            _allLists.remove(x)

    
    _allAlerts = penAndCheckUsedData_Process_process_get_alertLines(_allLists, False)

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

_ignore_lines = ['if (PLSMessageBox::question(this, QTStr("Basic.AutoConfig"), msg) == PLSAlertView::Button::Yes) {','int pls_alert_warning(const char *title, const char *message) override { return PLSAlertView::warning(PLSBasic::Get(), QTStr(title), QTStr(message)); }']

#将文件的行信息，转换成model类型
def getalertModels():

#删除带有channels 开头的重复key
    def delete_duplicate_key(data):
        new_data = []
        for _sub in data:
            _isIn = False
            for _newSub in new_data:
                if _newSub.key == _sub.key and _sub.key.startswith(_chanenlKey):
                    _isIn = True
                    break
            if not _isIn:
                new_data.append(_sub)

        return new_data


    _lines = getAllAlerts()
    print("get all alert lines")

    _datas = []
    for x in _lines:
        _is_ignoreLine = False
        for _ignoreLine in _ignore_lines:
            if _ignoreLine in x:
                _is_ignoreLine = True
                break
        if _is_ignoreLine == True:
            # print('ignore:', x)
            continue

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
                b = b.replace('CHANNELS_TR(', _chanenlKey)
                b = b.replace('obs_module_text("', '')
                b = b.replace('WARNING_TEXT("', 'Basic.AutoConfig.StreamPage.StreamWarning.')
                model.key = b
                break
        _datas.append(model)

    # for i in range(len(_datas)):
    #     _model = _datas[i]
    #     print(_model.key,"\t\t\t", _model.line)
    return _datas

#查找文件中的const 类型，进行model里面的替换
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
            if addKey in _line and ' = "' in _line:
                a = _line.split(' = "')[1]
                a = a.split('";')[0]
                if ')' not in a and 'error_title' != a:
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

    st_white_center = xlwt.easyxf()
    alignment = xlwt.Alignment()
    alignment.vert = xlwt.Alignment.VERT_CENTER #垂直居中
    st_white_center.alignment = alignment

    worksheet.write(_allIndex, 0, "key",st_white_center)
    worksheet.write(_allIndex, 1, "备注",st_white_center)
    worksheet.write(_allIndex, 2, "代码",st_white_center)
    worksheet.write(_allIndex, 3, "en",st_white_center)
    worksheet.write(_allIndex, 4, "kr",st_white_center)
    worksheet.write(_allIndex, 5, "es",st_white_center)
    worksheet.write(_allIndex, 6, "pt",st_white_center)
    worksheet.write(_allIndex, 7, "ID",st_white_center)


    st_orange = xlwt.easyxf('pattern: pattern solid;')
    st_orange.pattern.pattern_fore_colour = 51 #51 是橘黄色
    worksheet.col(0).width = 10534 #行宽140
    worksheet.col(1).width = 10534 #行宽140
    worksheet.col(2).width = 35534 #行宽140

    worksheet.col(3).width = 10534 #行宽140

    for data in _alertModels:
        _allIndex = _allIndex+1
        worksheet.row(_allIndex).height = 320
        if len(data.transKey)  > 1:
            _subStr = '多个key在同一alert：'
            if data.isSplite == True:
                _subStr = '多个key在 不同的 alert：'
            _str = _subStr + ',  '.join(data.transKey)
            worksheet.write(_allIndex, 1, _str,st_white_center)
        else:
            worksheet.write(_allIndex, 1, data.transKey,st_white_center)

        worksheet.write(_allIndex, 2, data.line,st_white_center)
        if data.isINIFound == True:
            worksheet.write(_allIndex, 0, data.key,st_white_center)
            if len(data.transKey) >= 1:
                if data.isSplite == True: #多个key 独立的情况

                    for i in range(len(data.transKey)):
                        _subTransKey = data.transKey[i]
                        for ini in _inis:
                            if ini.keyStr == _subTransKey:
                                worksheet.write(_allIndex, 3, ini.s_en_US,st_white_center)
                                worksheet.write(_allIndex, 4, ini.s_ko_KR,st_white_center)
                                worksheet.write(_allIndex, 5, ini.s_es_ES,st_white_center)
                                worksheet.write(_allIndex, 6, ini.s_pt_BR,st_white_center)
                                worksheet.write(_allIndex, 7, ini.s_id_ID,st_white_center)
                                break
                        if i != 0:
                            worksheet.write(_allIndex, 2, "代码同上，有多个值")
                        if len(data.transKey) > 1 and i != len(data.transKey) - 1:
                            _allIndex = _allIndex+1

                else: #多个transKey用两\n 分割
                    _tmpList = [[],[],[],[],[]]
                    for i in range(len(data.transKey)):
                        _subTransKey = data.transKey[i]
                        for ini in _inis:
                            if ini.keyStr == _subTransKey:
                                _tmpList[0].append(ini.s_en_US)
                                _tmpList[1].append(ini.s_ko_KR)
                                _tmpList[2].append(ini.s_es_ES)
                                _tmpList[3].append(ini.s_pt_BR)
                                _tmpList[4].append(ini.s_id_ID)
                                break
                    worksheet.write(_allIndex, 3, "\n\n".join(_tmpList[0]),st_white_center)
                    worksheet.write(_allIndex, 4, "\n\n".join(_tmpList[1]),st_white_center)
                    worksheet.write(_allIndex, 5, "\n\n".join(_tmpList[2]),st_white_center)
                    worksheet.write(_allIndex, 6, "\n\n".join(_tmpList[3]),st_white_center)
                    worksheet.write(_allIndex, 7, "\n\n".join(_tmpList[4]),st_white_center)
                    if len(_tmpList[0]) > 0:
                        worksheet.row(_allIndex).height_mismatch = True
                        worksheet.row(_allIndex).height = 1020*len(_tmpList[0])
            else:
                #没有transKey的情况
                for ini in _inis:
                    if ini.keyStr == data.key:
                        worksheet.write(_allIndex, 3, ini.s_en_US,st_white_center)
                        worksheet.write(_allIndex, 4, ini.s_ko_KR,st_white_center)
                        worksheet.write(_allIndex, 5, ini.s_es_ES,st_white_center)
                        worksheet.write(_allIndex, 6, ini.s_pt_BR,st_white_center)
                        worksheet.write(_allIndex, 7, ini.s_id_ID,st_white_center)
                        break
        else:
            worksheet.write(_allIndex, 0, data.key, st_orange)
            pass
    workbook.save(_dir)




def gotData():
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
            data.transKey = [_dic[data.key]]
            # print( data.transKey)
            data.isINIFound = True

    for data in _datas:
        if data.isINIFound == True:
            continue
        for x in _hands_trans_keys:
            if data.line == x['key']:
                data.isSplite = x['isSplite']
                data.transKey = list(x['gotKeys'])
                if 'isNeedCheck' in x and x['isNeedCheck'] == True :
                    data.isINIFound = False
                else:
                    data.isINIFound = True
                break


    # print("----")
    # for data in _datas:
    #     print(data.key, "\t\t\t\t", type(data))
    xibPath = dir_cache_path + "alerts.xls"
    # _datas = sorted(_datas, cmp=None, key='', reverse=False)
    # 表示按x[1]升序排序
    _datas.sort(key=lambda x:(x.isINIFound,x.key))

    writeAlertAndIniToExcel(xibPath, _datas, _inis)
    #     #     print("1")

    # for x in _datas:
    #     print(x.isINIFound)



if __name__ == '__main__':
    # # print(query_params[0]['gotKeys'][0])
    # print(query_params[1])
    gotData()


