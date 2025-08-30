# ANSWER
# Idea: An inorder traversal of a BST visits values in sorted order; the minimum difference must be between adjacent inorder values.

from typing import Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def getMinimumDifference(self, root: Optional['TreeNode']) -> int:
        smallest_gap = float('inf')  # best answer so far
        previous_val = None          # last value seen in inorder sequence

        def inorder(node: Optional['TreeNode']) -> None:
            nonlocal smallest_gap, previous_val
            if not node:
                return

            # 1) explore left (smaller values)
            inorder(node.left)

            # 2) visit node: compare with previous inorder value
            if previous_val is not None:
                # In a BST, inorder yields sorted values, so comparing to the
                # immediately previous value suffices to find the global minimum.
                current_gap = node.val - previous_val
                if current_gap < smallest_gap:
                    smallest_gap = current_gap
            previous_val = node.val

            # 3) explore right (larger values)
            inorder(node.right)

        inorder(root)
        return smallest_gap

# Complexity:
# Time  : O(n) — each node is visited once.
# Space : O(h) recursion stack, where h is tree height (O(n) worst-case skewed, O(log n) if balanced).
