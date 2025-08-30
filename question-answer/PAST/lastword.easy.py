class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        return len(s.split()[-1])


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        # skip trailing spaces
        while i >= 0 and s[i] == ' ':
            i -= 1
        # count the last word
        length = 0
        while i >= 0 and s[i] != ' ':
            length += 1
            i -= 1
        return length
