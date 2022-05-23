import sys, os

import sys, os, json
import time
from typing import List
from time import strftime
import uiautomation as auto
import subprocess
from ini_common_method import *
from ini_get_all_ini_structs import getAllDirInis



if __name__ == '__main__':
    a= encodeStr("https://connect.navercorp.com/home")
    print(a)
    b = decodeStr(a)
    print(b)