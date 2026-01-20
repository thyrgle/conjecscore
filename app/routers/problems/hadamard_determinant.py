import numpy as np
from sympy import Matrix

from .utils import register_problem, parse_CSV


def score(mat: [int]):
    if len(mat) != 23 * 23:
        return None
    for num in mat:
        if num != 1 and num != -1:
            return None
    np_mat = np.reshape(mat, (23, 23))
    sym_mat = Matrix(np_mat)
    return sym_mat.det() // (10 ** 9)


register_problem("hadamard-determinant", score, "Hadamard Determinant",
                 "hadamard-determinant.j2", "highest", "haddet", parse_CSV)
