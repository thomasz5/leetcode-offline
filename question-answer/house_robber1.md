Solution 1: Dynamic Programming with an Array
Problem Recap
A thief is robbing houses along a street, but they can't rob two consecutive houses. Each house has a certain amount of money, and the goal is to maximize the amount stolen without breaking the rule.

Approach
Key Observations
If a thief robs house i, they cannot rob house i-1 due to the constraints.
If the thief skips house i, their maximum profit up to house i is the same as the profit for house i-1.
DP Definition
Let dp[i] represent the maximum amount of money that can be stolen from the first i+1 houses.

State Transition
The thief has two options at house i:

Skip the house: Maximum profit is the same as the previous house, dp[i-1].
Rob the house: Add the value of the house to the profit two houses back, nums[i] + dp[i-2].
Thus, the recurrence relation is:

dp[i] = max(dp[i-1], nums[i] + dp[i-2])
Base Cases
If there is only one house, the maximum profit is simply nums[0].
For two houses, take the maximum value between the two: max(nums[0], nums[1]).
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        
        if n == 1:
            return nums[0]
        
        dp = [0] * n
        
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        
        for i in range(2, n):
            dp[i] = max(dp[i-1], nums[i] + dp[i-2])
        
        return dp[-1] 
Step-by-Step Example
Consider nums = [2, 7, 9, 3, 1]:

dp[0] = 2: Robbing the first house.
dp[1] = 7: Robbing the second house since it has more money.
dp[2] = max(7, 9 + 2) = 11: Robbing the first and third houses.
dp[3] = max(11, 3 + 7) = 11: Skipping the fourth house.
dp[4] = max(11, 1 + 11) = 12: Robbing the first, third, and fifth houses.
Output: 12

Complexity
Time Complexity: O(n) — A single loop processes all houses.
Space Complexity: O(n) — The dp array stores results for all houses.


Solution 2: Optimized Space Dynamic Programming
Optimizing the Approach
In Solution 1, we used an array dp to store results for all houses. However, only the last two values in the dp array are needed at any time. This insight allows us to reduce space complexity by using two variables to track these values.

Approach
Variables
prev_rob: Maximum profit if the thief robs up to house i-2.
max_rob: Maximum profit if the thief robs up to house i-1.
Transition
At each house, calculate the maximum profit:

temp = max(max_rob, prev_rob + nums[i])
Then update the variables:

prev_rob = max_rob
max_rob = temp
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev_rob = max_rob = 0

        for cur_val in nums:
            temp = max(max_rob, prev_rob + cur_val)
            prev_rob = max_rob
            max_rob = temp
        
        return max_rob
Step-by-Step Example
For nums = [2, 7, 9, 3, 1]:

House	Current Value (cur_val)	Profit If Robbed (prev_rob + cur_val)	Profit If Skipped (max_rob)	Updated prev_rob	Updated max_rob
1	2	2	0	0	2
2	7	7	2	2	7
3	9	11	7	7	11
4	3	10	11	11	11
5	1	12	11	11	12
Output: 12

Complexity
Time Complexity: O(n) — A single loop processes all houses.
Space Complexity: O(1) — Only two variables are used.
Comparison of Approaches
Approach	DP with Array	Space-Optimized DP
Code Readability	Easy to follow, tracks all states	More compact, but state transitions are implicit
Space Complexity	O(n)	O(1)
When to Use	When debugging or visualizing intermediate states is important	When memory efficiency is critical
Both solutions solve the problem using dynamic programming principles. The choice between them depends on the specific constraints and requirements of your use case.