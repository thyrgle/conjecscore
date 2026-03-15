from itertools import combinations
import numpy as np


def is_latin(sqr: np.ndarray, order: int) -> bool:
    need = set(range(1, order + 1))
    # Check the rows.
    for row in sqr:
        if set(row) != need:
            return False

    # Check the columns.
    for col in sqr.T:
        if set(col) != need:
            return False

    # It passed all checks, it is a Latin square.
    return True


def is_intercalate(sqr: np.ndarray, 
                   r1: int, r2: int, c1: int, c2: int) -> bool:
    if sqr[r1, c1] == sqr[r2, c2] and sqr[r2, c1] == sqr[r1, c2]:
        return True
    return False

async def score(sqr: [int]):
    N = 30
    mat = np.reshape(sqr, (N, N))
    # Check to see if we have a valid Latin square.
    if not is_latin(mat, N):
        return None

    nums = list(range(N))
    count = 0
    for r1, r2 in combinations(nums, 2):
        for c1, c2 in combinations(nums, 2):
            if is_intercalate(mat, r1, r2, c1, c2):
                count += 1

    return count
