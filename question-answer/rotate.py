from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        if k == 0:
            return

        right = nums[-k:]   # last k elements
        left  = nums[:-k]   # the rest
        nums[:] = right + left   # in-place replacement (preserves list identity)
