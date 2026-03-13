import numpy as np
from sympy import Matrix
from collections import Counter


async def score(mat: [int]):
    N = 16
    # Not the correct size.
    if len(mat) != N * N:
        return None

    # Ensure there are 10 copies of 1, 10:
    c = Counter(mat)
    for i in range(1, N + 1):
        if c[i] != N:
            return None

    np_mat = np.reshape(mat, (N, N))
    sym_mat = Matrix(np_mat)
    return int(sym_mat.det() / (10 ** 16))
