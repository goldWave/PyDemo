# coding = utf-8

import sys
import time
from pynput import keyboard
import uiautomation as auto

auto.uiautomation.SetGlobalSearchTimeout(2)  # 设置全局搜索超时 15
# 由 微软自带的 Inspect 自动抓取

def get_timer_item():
    global window
    print(window)
    sub = window.Control(AutomationId='PLSMainView.body.content.PLSBasic.sourcesDock')# search 4 times
    print(sub)
    sub1=sub.ListItemControl(searchDepth=5,Name='Clock Widget')
    print('\n')
    print(sub1)
    return sub1

def close_property_view_1():
    global window
    pro_win=window.WindowControl(searchDepth=1,ClassName='PLSBasicProperties')
    # print(pro_win)
    close_btn = pro_win.ButtonControl(Name="Cancel", ClassName='QPushButton')
    # print('\n')
    # print(close_btn)
    close_btn.Click()

def function_1():
    global isWillExit
    print('Function f8 activated')
    isWillExit = True


if __name__ == '__main__':
    t0 = time.time()
    isWillExit = False
    listener = keyboard.GlobalHotKeys({'<f8>': function_1})
    listener.start()

    window=auto.WindowControl(searchDepth=1,Name='Prism Live Studio')
    window.SetActive()
    item = get_timer_item()
    
    index = 0
    while True:
        item.DoubleClick()
        close_property_view_1()
        print('点击循环次数' + str(index) + "   耗时" + str(time.time() - t0))
        index+=1
        if isWillExit == True:
            print('exit with shortcut')
            exit()
