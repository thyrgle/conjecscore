from itertools import batched, combinations


def colinear(p1, p2, p3):
    # From https://math.stackexchange.com/a/405981/15140
    a, b = p1
    m, n = p2
    x, y = p3
    return (n - b) * (x - m) == (y - n) * (m - a)


async def score(nums: list[int]):
    # All coordinate values must be in range [0, 99]
    for num in nums:
        if num < 0 or num >= 100:
            return None
    # Need two values for each point, so length should be even.
    if len(nums) % 2 == 1:
        return None
    points = list(batched(nums, 2))
    dups = set(points)
    # All points should be distinct!
    if len(dups) != len(points):
        return None
    # Cannot have more than 2*n (n = 100)
    if len(points) > 200:
        return None

    # Now check if any of the points are colinear, if so, not a valid config.
    for p1, p2, p3 in combinations(points, 3):
        if colinear(p1, p2, p3):
            return None

    return (200 - len(points)) * 5000
