import os
from itertools import combinations
import math
from statistics import mean

from .utils import register_problem, parse_CSV, remove_two_pow


def score(square: list[int]):
    # Ensure there are distinct elements.
    if len(set(square)) != len(square):
        return None
    # Check if they are all squares.
    for entry in square:
        if entry == 0:
            return None
        if math.isqrt(entry) ** 2 != entry:
            return None
    square = remove_two_pow(square)

    sums = []
    # Compute the score
    # Compute rows:
    sums.append(square[0] + square[1] + square[2])
    sums.append(square[3] + square[4] + square[5])
    sums.append(square[6] + square[7] + square[8])
    # Compute columns:
    sums.append(square[0] + square[3] + square[6])
    sums.append(square[1] + square[4] + square[7])
    sums.append(square[2] + square[5] + square[8])
    # Compute diagonals:
    sums.append(square[0] + square[4] + square[8])
    sums.append(square[6] + square[4] + square[2])

    scores = []
    for s1, s2 in combinations(sums, 2):
        b1, b2 = bin(s1)[2::][::-1], bin(s2)[2::][::-1]
        if len(b1) != len(b2):
            scores.append(10 ** 6)
        else:
            pre = len(os.path.commonprefix([b1, b2]))
            scores.append((1 - pre / len(b1)) * 10 ** 6)
    return int(mean(scores))
    

register_problem("magic-square-of-squares", score, "Magic Square of Squares",
                 "magic-square-of-squares.j2", "lowest", "magicsos", parse_CSV)
