# coding = utf-8

import sys
import win32api
import win32gui
import win32con
import time
import random
from pynput import keyboard

#WinSpy64.exe 抓取

def close_property_view():
    pro_hld = 0
    maxCount = 5
    index = 0
    while True:
        index += 1
        pro_hld = win32gui.FindWindow(None, "Properties for \'Clock Widget\'")
        if (pro_hld <= 0):
            if index >= maxCount:
                print("超出时间推出循环")
                return
            time.sleep(random.randint(50, 150) / 1000)
        else:
            break
    pro_rect = win32gui.GetWindowRect(pro_hld)
    win32api.SetCursorPos([pro_rect[2] - 20, pro_rect[1] + 20])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def get_widget_pos():
    hld = win32gui.FindWindow(None, "Sources")
    if (hld <= 0):
        return []
    hwnd1 = win32gui.FindWindowEx(hld, None, 'Qt5QWindowIcon', None)  # 目标子句柄
    if (hwnd1 <= 0):
        return []
    r1 = win32gui.GetWindowRect(hwnd1)
    if (len(r1) == 0):
        return []

    return [r1[0] + 20, r1[1] + 30]


def double_click_timer_button():
    global widget_pos
    win32api.SetCursorPos(widget_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def function_1():
    global isWillExit
    print('Function 1 activated')
    isWillExit = True


if __name__ == '__main__':
    t0 = time.time()
    isWillExit = False
    listener = keyboard.GlobalHotKeys({'<f8>': function_1})
    listener.start()

    widget_pos = get_widget_pos()
    print(widget_pos)
    if len(widget_pos) == 0:
        exit()

    index = 0
    while True:
        double_click_timer_button()
        close_property_view()
        print('点击循环次数' + str(index) + "   耗时" + str(time.time() - t0))
        index+=1
        if isWillExit == True:
        	print('exit with shortcut')
        	exit()
        time.sleep(0.2)
