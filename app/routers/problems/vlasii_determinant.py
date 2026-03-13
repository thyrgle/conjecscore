import numpy as np
from sympy import Matrix
from collections import Counter


async def score(mat: [int]):
    # Not the correct size.
    if len(mat) != 10 * 10:
        return None

    # Ensure there are 10 copies of 1, 10:
    c = Counter(mat)
    for i in range(1, 11):
        if c[i] != 10:
            return None

    np_mat = np.reshape(mat, (10, 10))
    sym_mat = Matrix(np_mat)
    return int(sym_mat.det() / (10 ** 6))
