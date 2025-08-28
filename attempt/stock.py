from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        
        '''
        buy/sell stock easy answer:
        '''
        # idx2 = 0
        # profit = 0
        # for i in range(len(prices) - 1):
        #     if prices[idx2] < prices[i+1] and prices[i+1] - prices[idx2] > profit:
        #         profit = prices[i+1] - prices[idx2]
        #     elif prices[i] < prices[idx2]:
        #         idx2 = i
        #     elif prices[idx2] > prices[i+1]:
        #         idx2 += 1

        # return profit 



        idx2 = 0
        profit = 0
        prev_profit = 0
        for i in range(len(prices) - 1):
            if prices[idx2] < prices[i+1] and prices[i+1] - prices[idx2] > prev_profit:
                profit += prices[i+1] - prices[idx2] - prev_profit
                prev_profit = prices[i+1] - prices[idx2]
            elif prices[i] > prices[i+1] or prices[i+1] < prices[idx2]:
                idx2 = i + 1
                prev_profit = 0
            # elif :
            #     idx2 = i
            # elif prices[idx2] > prices[i+1]:
            #     idx2 += 1

        return profit 
            




