# ANSWER — LeetCode 1627: Graph Connectivity With Threshold (Hard)
# One-line idea:
#   Sieve-style Union-Find: for every divisor d > threshold, union all multiples of d.
#   Then each query [a, b] is connected iff find(a) == find(b).

from typing import List

class DSU:
    def __init__(self, n: int):
        # parent[i] = representative of i; size[i] = size of the set rooted at i
        self.parent = list(range(n + 1))  # we use 1..n
        self.size = [1] * (n + 1)

    def find(self, x: int) -> int:
        # Path compression — flattens the tree
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        # Union by size — attach smaller tree under larger tree
        ra, rb = self.find(a), self.find(b)
        if ra == rb: 
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


class Solution:
    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        # Quick edge cases:
        # 1) threshold >= n  -> no divisor strictly greater than threshold can divide any 1..n
        #    hence no edges at all (queries are ai != bi), answer = all False.
        if threshold >= n:
            return [False] * len(queries)

        # 2) threshold == 0 -> every pair shares divisor 1 (>0), the graph is complete, all True.
        #    This early return is optional (Union-Find would also handle it), but it's O(1) to short-circuit.
        if threshold == 0:
            return [True] * len(queries)

        dsu = DSU(n)

        # Core sieve-like union:
        # For each divisor d in (threshold+1 .. n), union d with all its multiples: 2d, 3d, ..., kd <= n.
        # Why this works: If two labels x and y share a common divisor z > threshold, then both x and y
        # are multiples of z, and our loop will connect every multiple of z into the same component.
        for d in range(threshold + 1, n + 1):
            first_multiple = 2 * d
            if first_multiple > n:
                continue
            for m in range(first_multiple, n + 1, d):
                dsu.union(d, m)

            # Optional micro-optimization: when d > n // 2, there's at most one multiple (2d) to union.
            # We already handle this naturally with the loop above.

        # Answer queries by checking whether they share the same representative.
        return [dsu.find(a) == dsu.find(b) for a, b in queries]


# -------------------- WHY THIS WORKS --------------------
# If two nodes x and y are connected (directly or indirectly) under the problem rule, then there exists
# a chain x = v0, v1, ..., vk = y where each consecutive pair shares some common divisor > threshold.
# For any fixed divisor d > threshold, our loops union every number that is a multiple of d into a single component.
# Therefore, if x and y share a divisor z > threshold, both x and y get joined to z's component, hence find(x) == find(y).

# -------------------- COMPLEXITY --------------------
# Building unions: sum_{d=threshold+1..n} floor(n/d) ≈ n * (H_n - H_threshold) = O(n log(n/threshold)).
# Union-Find operations are effectively amortized O(α(n)) per op (α is inverse Ackermann, ~ constant).
# Answering Q queries is O(Q).
# Total: O(n log(n/threshold) + Q) time, O(n) space.

# -------------------- TINY WALKTHROUGH (Example 1) --------------------
# n=6, threshold=2 → consider d=3,4,5,6:
#   d=3: union(3,6)  -> {3,6} together
#   d=4: union(4,8)  but 8>6, so none → 4 alone
#   d=5: union(5,10) but 10>6, so none → 5 alone
#   d=6: union(6,12) but 12>6, so none → 6 stays with 3 from earlier
# Queries:
#   [1,4] → find(1)!=find(4) → False
#   [2,5] → find(2)!=find(5) → False
#   [3,6] → find(3)==find(6) → True
