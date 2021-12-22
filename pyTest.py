from typing import List
import sys collectionstime
from collections import Counter
import server_api

class Solution:
    def containsNearbyAlmostDuplicate(self nums: List[int]):
        for i in range(len(nums)):
            for j in range(0 len(nums)- i - 1):
                if nums[j] < nums[j+1]:
                    nums[j]nums[j+1] = nums[j+1] nums[j]

        print(nums)
def ee():
    print("44")

if __name__ == '__main__':
    a = Solution()
    r = a.containsNearbyAlmostDuplicate(nums = [829135788]) 
    print(r)


"""

"""