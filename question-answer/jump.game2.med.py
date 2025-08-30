# ANSWER
# Idea: Greedy "level-by-level" scan — expand the farthest reachable index within the current jump window; when we finish a window, we take one jump and start the next window at the farthest.

from typing import List

class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        Greedy invariant:
          - We scan indices from left to right inside the *current* jump's reach [0..current_end].
          - While scanning, we track the farthest index we could reach with ONE MORE jump (farthest).
          - When we finish the current window (i == current_end), we must jump: jumps += 1,
            and the next window becomes everything up to 'farthest'.
        This treats each jump like a BFS layer over indices, giving the minimum # of jumps.
        """
        n = len(nums)
        if n <= 1:
            return 0

        jumps = 0          # number of jumps taken so far
        current_end = 0    # rightmost index reachable with 'jumps' jumps
        farthest = 0       # farthest index reachable with 'jumps + 1' jumps

        # We stop at n-2 because once we "open" a new window that reaches the end,
        # we count the jump without needing to process the last index.
        for i in range(n - 1):
            # Update the best we can do with one more jump from any index in current window
            farthest = max(farthest, i + nums[i])

            # If we've reached the end of the current window, we must take a jump
            if i == current_end:
                jumps += 1
                current_end = farthest
                # Early exit: if our current window already reaches/overlaps the last index
                if current_end >= n - 1:
                    break

        return jumps

# Complexity:
# Time  : O(n) — single left-to-right pass.
# Space : O(1) — only a few counters.
