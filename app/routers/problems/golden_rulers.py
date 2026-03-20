from itertools import combinations


async def score(nums: list[int]):
    N = 7

    # Check the length of array
    if len(nums) != N*(N+1)//2:
        return None

    # Check the value range of array elements
    for x in nums:
        if x < 1 or x > 10000:
            return None

    # Calculate the set of lengths measured by all rulers
    diffs = set()
    for k in range(N):
        v = [0]
        a = 0
        for i in range(k*(k+1)//2, k*(k+1)//2+k+1):
            a += nums[i]
            v.append(a)
        for n1, n2 in combinations(v, 2):
            diffs.add(abs(n1 - n2))

    # Calculate score
    perfect = set(range(1, N*(N+1)*(N+2)//6+1))
    return len(perfect.intersection(diffs))
