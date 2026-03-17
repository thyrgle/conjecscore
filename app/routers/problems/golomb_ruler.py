from itertools import combinations


async def score(nums: [int]):
    N = 212
    # Looking for a length 29 Golomb ruler.
    if len(nums) != N:
        return None

    diffs = []
    for n1, n2 in combinations(nums, 2):
        diffs.append(abs(n1 - n2))

    # Not a Golomb ruler.
    if len(diffs) != len(set(diffs)):
        return None
   
    # We allow starting at any number so the order is max - min.
    return max(nums) - min(nums)
