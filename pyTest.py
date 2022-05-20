import sys, os

import sys, os, json
import time
from typing import List
from time import strftime
import uiautomation as auto
import subprocess




# if __name__ == '__main__':

#     _root = auto.GetRootControl()
#     window=_root.WindowControl(searchDepth=1,Name='Prism Live Studio')
    
#     source= window.WindowControl(AutomationId="PLSMainView.body.content.PLSBasic.sourcesDock")
#     _list = source.ListControl(AutomationId="PLSMainView.body.content.PLSBasic.sourcesDock.content.dockWidgetContents_6.sourcesFrame.sources")
#     # _list.children()
#     print(_list)
#     sourceItem = _list.ListItemControl()
    
#     cou = 0

#     for _ in range(10000):
#         sourceItem.DoubleClick(simulateMove=False)
#         alert = window.WindowControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSDialogView")
#         time.sleep(1)
#         if cou % 2 == 0:
#             alert.ButtonControl(Name="OK").Click(simulateMove=False)
#         else:
#             alert.ButtonControl(Name="Cancel").Click(simulateMove=False)
#         cou += 1
#         # time.sleep(1)

# if __name__ == '__main__':
#     # _f = r'C:\Users\Administrator\Downloads\WORKS\20220517093356_PRISMLiveStudio - 1.txt'
#     # _f = r'C:\Users\Administrator\Downloads\20220516131441_PRISMLiveStudio.txt'
#     _f = r'C:\Users\Administrator\Downloads\20220517093356_PRISMLiveStudio.txt'
#     _datas = {}
#     with open(_f, 'r', encoding='utf-8') as f:
#             allLines = f.readlines()
#             for x in allLines:
#                 if ': http request start:' in x:
#                     a = x.split('url = ')[1]
#                     # print(a)
#                     if a.endswith('.\n'):
#                         # a.replace('.\n', '')
#                         a = a[:-3]
#                     _datas[a] = 0
#     # print(_datas)
#     with open(_f, 'r', encoding='utf-8') as f:
#         allLines = f.readlines()
#         for x in allLines:
#             if 'http response ' in x:
#                 a = x.split('url = ')[1]
#                 if a.endswith('.\n'):
#                     # a.replace('.\n', '')
#                     a = a[:-4]
#                 if ',' in a:
#                     a = a.split(",")[0]
#                     a = a[:-4]
#                 # print(a)
#                 for key in _datas.keys():
#                     if a in key or key in a:
#                         # print(key)
#                         _datas[key] = 1
#     # print("\n\n\n\n")
#     for key in _datas.keys():
#         if _datas[key] == 0:
#             print(key)

#     # print(_datas)
#         # return _allFiles

_dir = r'C:\Users\Administrator\AppData\Local\PRISMLiveStudio\PRISMLauncher.exe'

if __name__ == '__main__':

    index = 0
    while True:
        print("index", index)
        _root = auto.GetRootControl()
        vsWindow=_root.WindowControl(searchDepth=1,AutomationId='VisualStudioMainWindow')
        vsWindow.SetActive()
        a = vsWindow.PaneControl(Name="ToolBarDockTop").ToolBarControl(ClassName="ToolBar")
        _runBtn =  a.SplitButtonControl(AutomationId="PART_FocusTarget", Name="调试目标")

        isOk = False
        for x in range(10):
            print("check run btn index: ", x)
            if (_runBtn.IsEnabled):
                isOk = True
                break
            time.sleep(6)

        print("click run btn isOk:", isOk)
        _runBtn.Click()

        
        window=_root.WindowControl(searchDepth=1,Name='Prism Live Studio')
        
        window.Exists(60,5)
        time.sleep(3)
        window.Refind()
        btn = window.ButtonControl(AutomationId="PLSMainView.titleBar.close")
        btn.Click(simulateMove=True)
        # isOk = False
        # for x in range(10):
        #     window.Refind()
        #     if (btn.Exists(0,0)):
        #         isOk = True
        #         break
        #     time.sleep(6)

        # print("click close btn isOk:", isOk)
        # btn.Refind()
        # btn.Click()

        index += 1


