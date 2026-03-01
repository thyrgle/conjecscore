import os
from .utils import remove_two_pow, parse_CSV, register_problem


async def score(nums: list[int]):
    # Ensure there are no duplicate numbers
    if len(nums) != len(set(nums)):
        return None
    # Ensure 4 numbers are supplied.
    if len(nums) != 4:
        return None
    # Ensure numbers are positive.
    for num in nums:
        if num <= 0:
            return None
    nums = remove_two_pow(nums)

    a, b, c, d = nums
    c1 = bin(a ** 5 + b ** 5)[2::]
    c2 = bin(c ** 5 + d ** 5)[2::]
    size = len(c1)
    if size != len(c2):
        return 10 ** 6
    pre = len(os.path.commonprefix([c1, c2]))
    return int((1 - pre / size) * 10 ** 6)


register_problem("taxicab", score, "Taxicab(5,2,n)",
                 "taxicab.j2", "lowest", "taxicab", parse_CSV, "taxicab.svg")
