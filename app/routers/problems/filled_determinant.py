import numpy as np
from sympy import Matrix


async def score(mat: [int]):
    N = 11
    elems = set(mat)
    # Need 64 elements
    if len(elems) != N * N:
        return None
    
    # Need all the elements 1, ..., 64
    need = set(range(1, N ** 2 + 1))
    if elems != need:
        return None

    print("H1")
    np_mat = np.reshape(mat, (N, N))
    sym_mat = Matrix(np_mat)
    P = 470379650542113331346272
    return int((sym_mat.det() / P) * 10 ** 9)
