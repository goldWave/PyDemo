
import sys, os, json
import time
import uiautomation as auto
from pynput import keyboard

auto.uiautomation.SetGlobalSearchTimeout(10)  # 设置全局搜索超时

_dict = {}
# {
#     "vlive":
#     {
#         "acc": "nvqa_prism_cd_003",
#         "pw": ""
#     },
#     "navertv":
#     {
#         "acc": "nvqa_prism_cd_003",
#         "pw": ""
#     },
#     "navershopping":
#     {
#         "acc": "nvqa_shop52",
#         "pw": ""
#     },
#     "band":
#     {
#         "acc": "nvqa_prism_cd_003",
#         "pw": ""
#     },
#     "afreecatv":
#     {
#         "acc": "abby0816",
#         "pw": ""
#     },
#     "facebook":
#     {
#         "acc": "nvqa_4tc134@naver.com",
#         "pw": ""
#     }
# }
def jsonApply():
    global _dict
    _path = os.path.join(os.path.dirname(__file__), "id_pw_user.json")
    if not os.path.exists(_path):
        _path = os.path.join(os.path.dirname(__file__), "id_pw.json")
    if not os.path.exists(_path):
        print('not found any id password local cache path')
        return

    with open(_path, 'r') as f:
        try:
            _dict = json.load(f)
        except Exception as e:
            print("id passord json parase failed! %s" % e.args)

def function_1():
    global isWillExit
    print('Function f2 activated, will stoped in next loops.')
    isWillExit = True
    sys.exit()

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
    elif 'facebook' in urlStr:
        return 'facebook'
    return 'empty'

def toLogin(_url, _id_ui, _pw_ui, _login_btn) -> True:
        _plat = getPlatform(_url)
        print('found %s login page' % _plat)
        _id, _pw = getusername(_plat)
        if _id == '' or _pw == '':
            print('acccout or password is empty')
            time.sleep(4)
            return

        try:
            _id_ui.Click(simulateMove=False)
            _id_ui.GetValuePattern().SetValue(_id)
        except:
            print("id except got it")

        try:
            _pw_ui.Click(simulateMove=False)
            _pw_ui.GetValuePattern().SetValue(_pw)
        except:
            print("pwd except got it")

        safeClick(_login_btn)

        print('maybe succeed...\ntry next...')
        time.sleep(2)
        return True

def getusername(_pls):
    # global _
     if not _pls in _dict.keys():
        return '',''
     _id = _dict[_pls]['acc']
     _pw = _dict[_pls]['pw']
     return _id, _pw


def safeClick(_btn):
    try:
        _btn.Click(simulateMove=False)
    except Exception as e:
        print("btn click failed! %s" % e.args)

def transPage(_windget):
    global isWillExit
    global _needTrans
    global login_page
    global window

    _document = _windget.DocumentControl(searchDepth=1)
    if not window.Exists(0,0) or not login_page.Exists(0,0):
        print('login page not found--------------')
        time.sleep(3)
        return

    if not _document.Exists(0,0):
        print('_document page not found--------------')
        return
    docuName = _document.Name
    # print('docuName: %s' % docuName)
    # print('docuurl: %s' % str(_document.GetValuePattern().Value))
    if docuName == 'V LIVE':
        print('found vlive page')
        _btn = _document.CustomControl(searchDepth=1, AutomationId='content').HyperlinkControl(searchDepth=2, SubName='NAVER')
        safeClick(_btn)
    elif docuName in ['네이버 : 로그인', 'Naver Sign in']:
        _sign_in_group = _document.CustomControl(searchDepth=2, AutomationId='container').CustomControl(searchDepth=1, AutomationId='frmNIDLogin')
        _id_input = _sign_in_group.EditControl(AutomationId='id')
        _pw_input = _sign_in_group.EditControl(AutomationId='pw')
        _btn = _sign_in_group.ButtonControl(AutomationId='log.login')

        toLogin(_document.GetValuePattern().Value,_id_input, _pw_input, _btn)
       
    elif docuName == '네이버 쇼핑라이브':
        print('found navershopping page')
        _btn = _document.CustomControl(searchDepth=2, AutomationId='root').GroupControl(searchDepth=2, AutomationId='content').HyperlinkControl(searchDepth=1, foundIndex=1)
        safeClick(_btn)

    elif '| BAND' in  docuName or  "| 밴드" in docuName:
        print('found band page')
        _btn = _document.GroupControl(searchDepth=2, AutomationId='content').ListControl(searchDepth=2, AutomationId='login_list').ListItemControl(searchDepth=1, foundIndex=3).TableControl(searchDepth=1)
        safeClick(_btn)

    elif docuName == ['BAND Together!', '"Ayo bersama di BAND!"', '"모임이 쉬워진다! 우리끼리 밴드"']:
        print('验证码我破解不了， sleep5')
        time.sleep(5)
    elif docuName in ['AfreecaTV',"아프리카TV 로그인","아프리카TV"]:
        print('found AfreecaTV page')
        _url = _document.GetValuePattern().Value
        if 'campaign_pw' in _url:
            _btn = _document.ButtonControl(AutomationId='btnNextTime')
            safeClick(_btn)
            return
        _id_input = _document.EditControl(AutomationId='uid')

        _pw_input = _document.EditControl(AutomationId='password')

        _btn = None
        _btn_en = _document.ButtonControl(Name='LOG IN')
        _btn_kr = _document.ButtonControl(Name='로그인')
        try:
            if _btn_en.Exists(0,0):
                _btn = _btn_en
                print("btn except got it 111")

            elif _btn_kr.Exists(0,0):
                _btn = _btn_kr
                print("btn except got it 111")
        except Exception as e:
            print("_btn failed. %s" % e.args)

        if _btn == None:
            return
        toLogin(_url ,_id_input, _pw_input, _btn)

    elif 'Log in With Facebook' in docuName:
        print('found Facebook page')
        _dialog  = _document.CustomControl(searchDepth=3,Name='Dialogue content')#, Name=
        if _dialog.Exists(0,0):
            _btn1 = _dialog.CustomControl(searchDepth=2, AutomationId='platformDialogForm').ButtonControl(Name='Agree and Continue')
            _btn2 = _dialog.CustomControl(searchDepth=2, AutomationId='platformDialogForm').ButtonControl(Name='OK')
            #"PRISM Live Studio's Privacy Policy and Terms"
            _btn3 = _dialog.CustomControl(searchDepth=2, AutomationId='platformDialogForm').ButtonControl(Name='Continue')
            try:
                if _btn1.Exists(0,0):
                    _btn1.Click(simulateMove=False)
                elif _btn2.Exists(0,0):
                    _btn2.Click(simulateMove=False)
                elif _btn3.Exists(0,0):
                    _btn3.Click(simulateMove=False)
            except Exception as e:
                print("_btn failed. %s" % e.args)

        time.sleep(2)
    elif 'Facebook | Facebook' in docuName:
        _frame_1 = _document.CustomControl(searchDepth=3, AutomationId='globalContainer').GroupControl(searchDepth=1, AutomationId='content').CustomControl(searchDepth=1, AutomationId='login_form')
        _err = _frame_1.CustomControl(searchDepth=1, AutomationId='error_box')
        _ignore = False
        try:
            if _err.Exists(0,0):
               _ignore = True
        except Exception as e:
            print("_btn1 failed. %s" % e.args)

        if _ignore == True:
            time.sleep(5)
            return

        _frame = _frame_1.CustomControl(searchDepth=1, AutomationId='loginform')
        _id_input = _frame.EditControl(AutomationId='email')
        _pw_input = _frame.EditControl(AutomationId='pass')
        _btn = _frame.ButtonControl(AutomationId='loginbutton')
        toLogin(_document.GetValuePattern().Value,_id_input, _pw_input, _btn)
    else:
        print("ignore docuName: %s" % docuName)

if __name__ == '__main__':

    jsonApply()
    isWillExit = False
    listener = keyboard.GlobalHotKeys({'<f2>': function_1})
    listener.start()
    print('start ...')
    _root = auto.GetRootControl()
    window=_root.WindowControl(searchDepth=1,Name='Prism Live Studio')
    login_page = window.WindowControl(searchDepth=1, AutomationId='PLSMainView.PLSBrowserView')
    while True:
        if isWillExit == True:
            sys.exit()
            break
        if not window.Exists(0,0) or not login_page.Exists(0,0):
            print('searching ...')
            time.sleep(5)
        else:
            try:
                print('try found ...')
                window.Refind()
                login_page.Refind()
                _tr = login_page.GetTransformPattern()
                _rect = login_page.BoundingRectangle
                if login_page.HasKeyboardFocus == True:
                    _tr.Resize(_rect.width(), 2000)
                login_page.SetActive()
                login_page.Refind()
            except Exception as e:
                print("search failed. %s" % e.args)

            while True:
                print("next loop...")
                if isWillExit == True:
                    sys.exit()
                    break
                _windget = login_page.GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
                _windget_1 = login_page.WindowControl(searchDepth=1, ClassName='QPLSBrowserPopupDialog').GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
                if not login_page.Exists(0,0):
                    print("login_page not Exists. seleep 5")
                    time.sleep(5)
                    break
                _needTrans = False
                if _windget_1.Exists(0,0):
                    _needTrans = True
                transPage(_windget if _needTrans == False else _windget_1)
                time.sleep(1)
