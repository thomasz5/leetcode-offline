from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        n = len(words)
        i = 0

        while i < n:
            # Greedily fit as many words as possible
            line_len = len(words[i])
            j = i + 1
            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])  # +1 for the space between words
                j += 1

            line_words = words[i:j]
            is_last_line = (j == n)

            if is_last_line or len(line_words) == 1:
                # Left-justify
                line = " ".join(line_words)
                line += " " * (maxWidth - len(line))
                res.append(line)
            else:
                # Full-justify
                total_chars = sum(len(w) for w in line_words)
                total_spaces = maxWidth - total_chars
                slots = len(line_words) - 1
                base = total_spaces // slots
                extra = total_spaces % slots  # leftmost 'extra' slots get 1 more space

                parts = []
                for k in range(slots):
                    parts.append(line_words[k])
                    gap = base + (1 if k < extra else 0)
                    parts.append(" " * gap)
                parts.append(line_words[-1])  # last word (no trailing spaces)
                res.append("".join(parts))

            i = j

        return res
