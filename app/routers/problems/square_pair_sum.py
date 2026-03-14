from math import isqrt
from itertools import combinations


async def score(nums: [int]):
    N = 6

    # Not the correct size.
    if len(nums) != N:
        return None

    # All numbers must be positive
    for num in nums:
        if num <= 0:
            return None

    # Not all entries were distinct.
    if len(nums) != len(set(nums)):
        return None

    for x, y in combinations(nums, 2):
        # A pair did not sum to a square
        if isqrt(x + y) ** 2 != x + y:
            return None

    return max(nums)
