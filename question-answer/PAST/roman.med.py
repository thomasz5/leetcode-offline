class Solution:
    def intToRoman(self, num: int) -> str:
        values  = [1000, 900, 500, 400, 100,  90,  50,  40,  10,   9,   5,   4,   1]
        symbols = ["M", "CM","D", "CD","C", "XC","L", "XL","X", "IX","V", "IV","I"]
        res = []
        for v, s in zip(values, symbols):
            while num >= v:
                res.append(s)
                num -= v
        return "".join(res)


class Solution:
    def intToRoman(self, num: int) -> str:
        thousands = ["", "M", "MM", "MMM"]
        hundreds  = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens      = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones      = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

        return (
            thousands[num // 1000] +
            hundreds[(num % 1000) // 100] +
            tens[(num % 100) // 10] +
            ones[num % 10]
        )
