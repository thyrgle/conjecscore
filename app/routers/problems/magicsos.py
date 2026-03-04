from math import log
from statistics import pstdev

from .utils import register_problem, parse_CSV


async def score(square: list[int]):
    # Ensure there are 9 entries
    if len(square) != 9:
        return None
    # Ensure there are distinct elements.
    if len(set(square)) != len(square):
        return None
    # Check if they are all squares.
    for entry in square:
        if entry <= 0 or entry >= 10 ** 20:
            return None
    std = pstdev(square)
    square = [x ** 2 for x in square]

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

    M = max(sums)
    m = min(sums)
    result = (M - m) / (log(M) * std)
    return int(result * 10 ** 6)
    

register_problem("magic-square-of-squares", score, "Magic Square of Squares",
                 "magic-square-of-squares.j2", "lowest", "magicsos", 
                 parse_CSV, "magicsos.svg")
