
import os, time, sys, io, json
import datetime
from ctypes import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from auto_download_chromedriver_ifneed import download_chromedriver
from auto_download_chromedriver_ifneed import download_chromedriver as autoDC
from ini_common_method import *

class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        isFirstIn = True
        size = len(nums)
        if size == 0:
            return
        tmpK = k % size
        print(tmpK)
        i = 0
        preVal = nums[i]
        while True:
            if i >= size - 1:
                i -= size
            if not isFirstIn and i == 0:
                break
            j = i+tmpK
            isFirstIn = False
            if j >= size - 1:
                j -= size

            print(i,j)
            tmp = nums[j]
            nums[j] = preVal
            preVal = tmp
            i += 1
        print(nums)


def findData(nums, val):
    n = len(nums)
    start = 0
    end = n - 1
    while start <= end:
        idx = start + (end - start) // 2
        print(idx, start, end)

        if nums[idx] > val:
            end =  idx  - 1
        elif nums[idx] < val:
            start = idx + 1
        else:
            return idx
        # if idx == start or idx == end:
        #     break
    return -1

if __name__ == '__main__':
    # s = Solution()
    # # s.rotate([1,2,3,4,5,6,7], 3)
    # s.rotate([-1,-100,3,99], 2)
    # INT_MIN, INT_MAX = -2**31, 2**31 - 1
    # print(2**32-1)
    # print(INT_MAX)
    nums = [1,4,6,8,9,11,23]
    i = findData(nums, 26);
    print(i)
# 2147483647
# 4294967295