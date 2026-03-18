from itertools import combinations, batched


async def score(nums: [int]):
    N = 28
    # Looking for a length 14 points.
    if len(nums) != 2 * N: # Remember each point is 2 values.
        return None

    # Must be integers
    for num in nums:
        if int(num) != num:
            return None
    # Require 14 distinct points
    points = list(batched(nums, 2))
    if len(set(points)) != N:
        return None

    squared_dists = []
    for p1, p2 in combinations(points, 2):
        squared_dist = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
        squared_dists.append(squared_dist)

    # All distances must be distinct!
    if len(squared_dists) != len(set(squared_dists)):
        return None

    # We allow starting at any number so the order is max - min.
    return max(squared_dists)
