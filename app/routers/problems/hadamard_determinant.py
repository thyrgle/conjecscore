import numpy as np
from sympy import Matrix


async def score(mat: [int]):
    if len(mat) != 23 * 23:
        return None
    for num in mat:
        if num != 1 and num != -1:
            return None
    np_mat = np.reshape(mat, (23, 23))
    sym_mat = Matrix(np_mat)
    return sym_mat.det() // (10 ** 9)
