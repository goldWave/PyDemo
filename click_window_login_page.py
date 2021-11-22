# coding = utf-8

import sys
import time
from pynput import keyboard
import uiautomation as auto
from enum import Enum, unique

auto.uiautomation.SetGlobalSearchTimeout(2)  # 设置全局搜索超时

_dict = {}


def function_1():
    global isWillExit
    print('Function f8 activated')
    isWillExit = True

def getPlatform(urlStr) -> str:
    if 'band.us' in urlStr:
        return 'band'
    elif 'vlive.tv' in urlStr:
        return 'vlive'
    elif 'shoppinglive' in urlStr:
        return 'navershopping'
    elif urlStr.endswith('nidlogin.login'):
        return 'navertv'
    elif 'afreecatv' in urlStr:
        return 'afreecatv'

    return 'empty'

def getusername(_pls):
     if not _pls in _dict.keys():
        return '',''
     _id = _dict[_pls]['acc']
     _pw = _dict[_pls]['pw']
     return _id, _pw

def transPage(_windget):
    global isWillExit
    global _needTrans

    _document = _windget.DocumentControl(searchDepth=1)

    if not _document.Exists(0,0):
        return;
    docuName = _document.Name
    if docuName == 'V LIVE':
        _document.CustomControl(searchDepth=1, AutomationId='content').HyperlinkControl(searchDepth=2, Name='Continue with NAVER').Click(simulateMove=False)
    elif docuName == 'Naver Sign in':
        a = _document.GetValuePattern().Value
        _plat = getPlatform(a)
        _id, _pw = getusername(getPlatform(a))
        if _id == '' or _pw == '':
            print('acccout or password is empty')
            time.sleep(4)
            return
        _sign_in_group = _document.CustomControl(searchDepth=2, AutomationId='container').CustomControl(searchDepth=1, AutomationId='frmNIDLogin')
        _id_input = _sign_in_group.EditControl(AutomationId='id')
        _id_input.Click(simulateMove=False)
        _id_input.GetValuePattern().SetValue(_id)
        time.sleep(0.05)
        _pw_input = _sign_in_group.EditControl(AutomationId='pw')
        _pw_input.Click(simulateMove=False)
        _pw_input.GetValuePattern().SetValue(_pw)
        _btn = _sign_in_group.ButtonControl(AutomationId='log.login')
        _btn.Click(simulateMove=False)
        print('maybe succeed...\ntry next...')
        time.sleep(2)
    elif docuName == '네이버 쇼핑라이브':
        print('-----')
        _document.CustomControl(searchDepth=2, AutomationId='root').GroupControl(searchDepth=2, AutomationId='content').HyperlinkControl(searchDepth=1, foundIndex=1).Click(simulateMove=False)
    elif docuName == 'Log in | BAND':
        _document.GroupControl(searchDepth=2, AutomationId='content').ListControl(searchDepth=2, AutomationId='login_list').TableControl(searchDepth=2, Name='Log in using NAVER ID').Click(simulateMove=False)
    elif docuName == 'BAND Together!':
        print('sleep5')
        time.sleep(5)
    elif docuName == 'AfreecaTV':
        a = _document.GetValuePattern().Value
        _id, _pw = getusername(getPlatform(a))
        if len(_id) == 0 or len(_pw) == 0:
            print('acccout or password is empty')
            time.sleep(4)
            return
        if 'campaign_pw' in a:
            _document.ButtonControl(AutomationId='btnNextTime').Click(simulateMove=False)
            return
        _sign_in_group = _document.CustomControl(searchDepth=1, AutomationId='accountN')
        _id_input = _sign_in_group.EditControl(AutomationId='uid')
        _id_input.Click(simulateMove=False)
        _id_input.GetValuePattern().SetValue(_id)
        time.sleep(0.05)
        _pw_input = _sign_in_group.EditControl(AutomationId='password')
        _pw_input.Click(simulateMove=False)
        _pw_input.GetValuePattern().SetValue(_pw)
        _btn = _sign_in_group.ButtonControl(Name='LOG IN')
        _btn.Click(simulateMove=False)
        print('maybe succeed...\ntry next...')
        time.sleep(2)
    

if __name__ == '__main__':
    t0 = time.time()
    isWillExit = False
    listener = keyboard.GlobalHotKeys({'<f8>': function_1})
    listener.start()
    print('start ...')
    _root = auto.GetRootControl()
    window=_root.WindowControl(searchDepth=1,Name='Prism Live Studio')
    login_page = window.WindowControl(searchDepth=1, AutomationId='PLSMainView.PLSBrowserView')
    while True:
        if isWillExit == True:
            break
        if not login_page.Exists(0,0):
            time.sleep(5)
        else:
            try:
                window.Refind()
                login_page.Refind()
                _tr = login_page.GetTransformPattern()
                _rect = login_page.BoundingRectangle
                if login_page.HasKeyboardFocus == True:
                    _tr.Resize(_rect.width(), 2000)
                login_page.SetActive()
                login_page.Refind()
            finally:
                pass

            while True:
                if isWillExit == True:
                    break
                _windget = login_page.GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
                _windget_1 = login_page.WindowControl(searchDepth=1, ClassName='QPLSBrowserPopupDialog').GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
                if not login_page.Exists(0,0):
                    time.sleep(5)
                    break
                print('11')
                _needTrans = False
                if _windget_1.Exists(0,0):
                    print('22')
                    _needTrans = True
                transPage(_windget if _needTrans == False else _windget_1)
                time.sleep(1)