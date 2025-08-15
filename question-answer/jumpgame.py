from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        reach = 0
        last = len(nums) - 1
        for i, step in enumerate(nums):
            if i > reach:          # can't even get to i
                return False
            reach = max(reach, i + step)
            if reach >= last:      # already can reach the end
                return True
        return True


from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0
