from math import factorial, isqrt
from .utils import parse_CSV, register_problem


def score(nums: list[int]):
    # Ensure only one number is supplied.
    if len(nums) != 1:
        return None
    # Ensure n >= 8
    num = nums[0]
    if num < 8:
        return None
    
    nfact = factorial(num) + 1
    sml_sqrt = isqrt(factorial(num) + 1)
    big_sqr = (sml_sqrt + 1) ** 2
    sml_sqr = sml_sqrt ** 2 # Now square!
    interval = big_sqr - sml_sqr
    return int((min(nfact - sml_sqr, big_sqr - nfact) / interval) * 10 ** 9)


register_problem("brocard", score, "Brocard's Problem",
                 "brocard.j2", "lowest", "brocard", parse_CSV, "brocard.svg")
