import numpy as np
from sympy import Matrix


async def score(mat: [int]):
    # Not the correct size.
    if len(mat) != 10 * 10:
        return None

    # Each row should have {1, ..., 10} in it.
    np_mat = np.reshape(mat, (10, 10))
    # {1, ..., 10}
    nums = set(range(1, 11))
    for i in range(10):
        row = set(np_mat[i])
        if set(row) != nums:
            return None

    sym_mat = Matrix(np_mat)
    return sym_mat.det()
