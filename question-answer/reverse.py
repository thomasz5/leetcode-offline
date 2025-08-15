class Solution:
    def reverseWords(self, s: str) -> str:
        # split() collapses multiple spaces and trims ends automatically
        return " ".join(reversed(s.split()))


class Solution:
    def reverseWords(self, s: str) -> str:
        res = []
        i = len(s) - 1
        while i >= 0:
            # skip trailing/middle spaces
            while i >= 0 and s[i] == ' ':
                i -= 1
            if i < 0:
                break
            # locate the start of the word
            j = i
            while j >= 0 and s[j] != ' ':
                j -= 1
            # append the word s[j+1:i+1]
            res.append(s[j+1:i+1])
            i = j - 1
        return " ".join(res)
