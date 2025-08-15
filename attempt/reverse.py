class Solution:
    def reverseWords(self, s: str) -> str:
        # Variant 1
        # return " ".join(reversed(s.split()))
        # Variant 2 (uncomment to try this instead):
        # return self.reverseWords_alt(s)
        raise NotImplementedError

    def reverseWords_alt(self, s: str) -> str:
        res = []
        i = len(s) - 1
        while i >= 0:
            while i >= 0 and s[i] == ' ':
                i -= 1
            if i < 0:
                break
            j = i
            while j >= 0 and s[j] != ' ':
                j -= 1
            res.append(s[j+1:i+1])
            i = j - 1
        return " ".join(res)


