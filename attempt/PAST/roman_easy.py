##
# Input: s = "MCMXCIV"
# Output: 1994
# Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
##
class Solution:

    def romanToInt(self, s: str) -> int:
        val = {'I' : 1, 'V' : 5, "X" : 10, "L" : 50, "C" : 100, "D" : 500, "M" : 1000}
        # sum = 0
        # for i in range(1,len(s)):
        #         if val[s[i]] > val[s[i-1]]:
        #             sum += val[s[i]] - val[s[i-1]]
        #             if i < len(s) - 2:
        #                 i += 1
        #         elif i == len(s):
        #             sum += val[s[i]] +  val[s[i-1]]
                   
        #         else:
        #             sum += val[s[i-1]]
        # return sum

        sum = 0
        for i in range(len(s)):
            if i + 1 < len(s) and val[s[i]] < val[s[i+1]]: # why doesnt (if val[s[i]] < val[s[i+1]] and i + 1 < len(s):) work?
                sum -= val[s[i]]
            else:
                sum += val[s[i]]
        return sum


