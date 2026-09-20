from math import isqrt, gcd, log


async def score(nums: list[int]):
    # Ensure 3 integers are supplied.
    if len(nums) != 3:
        return None
    # Ensure numbers are between 1 and 10^100 
    for num in nums:
        if not (1 <= num <= 10 ** 100):
            return None

    a, b, c = nums

    # Ensure it is primitive
    if gcd(a, gcd(b, c)) > 1:
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
    numer = min(abc - sml_sqr, big_sqr - abc)

    mil = 10 ** 6
    return int(-log(numer / interval) * mil)
