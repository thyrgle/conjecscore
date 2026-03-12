import numpy as np
from sympy import Matrix


async def score(mat: [int]):
    # Not the correct size.
    if len(mat) != 9 * 9:
        return None

    # Each row should have {1, ..., 9} in it.
    np_mat = np.reshape(mat, (9, 9))
    # {1, ..., 9}
    nums = set(range(1, 10))
    for i in range(9):
        row = set(np_mat[i])
        if set(row) != nums:
            return None

    sym_mat = Matrix(np_mat)
    return sym_mat.det()
