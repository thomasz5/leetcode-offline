from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        if k == 0:
            return nums
        start = n - k
        nums[:] = nums[start:] + nums[:start]




