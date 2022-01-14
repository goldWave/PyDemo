# from winreg import *
import winreg
import os, sys


def isDev():
    with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\NAVER Corporation\Prism Live Studio", access=winreg.KEY_READ | winreg.KEY_WRITE) as root_key:
        try:
            val = winreg.QueryValueEx(root_key, 'DevServer1')[0]
        except FileNotFoundError:
            val = "0"
        return val == '1' or val.lower() == "false" or val.lower() == "yes"
        
if __name__ == '__main__':
    print(isDev())

