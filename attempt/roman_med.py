class Solution:
    def intToRoman(self, num: int) -> str:
        
        values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        characters = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'CL', 'X', 'IX', 'V','IV', 'I']
        output = []
        for v, c in zip(values, characters):
            while num >= v:
                num -= v
                output.append(c)
        return ''.join(output)



        # val = {1 : 'I', 5 : 'V', 10 : 'X', 50 : 'L', 100 : 'C', 500 : 'D', 1000 : 'M' }
        # sum = ''
        # ones = num % 10
        # num -= ones
        # tens = num % 100
        # num -= tens
        # hundreds = nums % 1000
        # num -= hundreds
        # thousands = nums 
       

        # while ones < 0:
        #     if ones > 5:
        #         sum + val[5]
        #         ones -= 5
        #     else:
        #         sum + val[1]
        #         ones -= 1
        
        # while tens < 0:
        #     if tens > 50:
        #         sum = val[50] + sum
        #         tens -= 50
        #     else: 
        #         sum += 
        # value = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
        # rom = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'LC', 'C', 'LD']

        # for x, y in enumerate(zip(value,rom)):
        #     if value

       

        


            # check if difference between number off of 1, 10, 100
            # number % val[num[x]]
            # if (int // 5) // 5





