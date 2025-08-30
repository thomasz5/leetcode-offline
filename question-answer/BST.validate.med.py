# ANSWER
# Idea: DFS with value bounds. For each node, enforce low < node.val < high, then narrow the bounds as we go left/right.

from typing import Optional

# LeetCode provides:
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: Optional['TreeNode']) -> bool:
        # Helper checks subtree rooted at `node` must have all values in (low, high)
        def dfs(node: Optional['TreeNode'], low: float, high: float) -> bool:
            if not node:
                return True  # Empty subtree is valid

            # BST requires STRICT inequalities:
            #   every value in left subtree < node.val
            #   every value in right subtree > node.val
            if not (low < node.val < high):
                return False

            # Left children must be < node.val, so tighten upper bound to node.val
            # Right children must be > node.val, so tighten lower bound to node.val
            return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

        # Start with infinite bounds (unrestricted root)
        return dfs(root, float("-inf"), float("inf"))

# Complexity:
# Time:  O(n) — visit each node once.
# Space: O(h) — recursion stack height (h = tree height; O(n) worst-case skewed, O(log n) average balanced).
