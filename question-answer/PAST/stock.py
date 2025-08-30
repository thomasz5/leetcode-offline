from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit



# class Solution:
#     def maxProfit(self, prices: List[int]) -> int:
#         cash = 0           # max profit when not holding
#         hold = -10**9      # max profit when holding (negative cost)
#         for p in prices:
#             cash = max(cash, hold + p)   # sell today
#             hold = max(hold, cash - p)   # buy today
#         return cash
