from math import isqrt


async def score(nums: list[int]):
    if len(nums) != 3:
        return None
    a, b, c = nums
    # Check to make sure it is an Euler Brick
    if a <= 0 or b <= 0 or c <= 0:
        return None
    # a^2 + b^2 = d^2
    ab = a ** 2 + b ** 2
    if isqrt(ab) ** 2 != ab:
        return None
    # a^2 + c^2 = e^2
    ac = a ** 2 + c ** 2
    if isqrt(ac) ** 2 != ac:
        return None
    # b^2 + c^2 = f^2
    bc = b ** 2 + c ** 2
    if isqrt(bc) ** 2 != bc:
        return None
    # How close to a square is a^2 + b^2 + c^2?
    abc = a ** 2 + b ** 2 + c ** 2
    sml_sqrt = isqrt(abc)
    big_sqr = (sml_sqrt + 1) ** 2
    sml_sqr = sml_sqrt ** 2
    interval = big_sqr - sml_sqr
    bil = 10 ** 9
    return int((min(abc - sml_sqr, big_sqr - abc) * bil/ interval))
