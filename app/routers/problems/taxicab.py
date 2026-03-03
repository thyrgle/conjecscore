from math import log
from statistics import mean, pvariance
from .utils import parse_CSV, register_problem


async def score(nums: list[int]):
    # Ensure there are no duplicate numbers
    if len(nums) != len(set(nums)):
        return None
    # Ensure 4 numbers are supplied.
    if len(nums) != 4:
        return None
    # Ensure numbers are positive.
    for num in nums:
        if num <= 0 or num >= 10 ** 20:
            return None

    a, b, c, d = nums
    lhs = a ** 5 + b ** 5
    rhs = c ** 5 + d ** 5
    M = max(lhs, rhs)
    m = min(lhs, rhs)
    me = mean([lhs, rhs])
    var = pvariance(nums)
    return int((M - m) / (log(me) * var) * 10 ** 6)


register_problem("taxicab", score, "Taxicab(5,2,n)",
                 "taxicab.j2", "lowest", "taxicab", parse_CSV, "taxicab.svg")
