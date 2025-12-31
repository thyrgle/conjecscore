import math
from statistics import pvariance, mean
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_low_score, render_lowest

router = APIRouter()


def magic_sos_score(square: list[int]):
    # Ensure there are distinct elements.
    if len(set(square)) != len(square):
        return None
    # Check if they are all squares.
    for entry in square:
        if math.isqrt(entry) ** 2 != entry:
            return None
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
    
    # Dispersion index of dispersion x 10^9 to make a nice number.
    return int((10 ** 9) * pvariance(sums) / mean(sums))


@router.post("/magicsos-submit", response_class=HTMLResponse)
async def submit_square(submission: Annotated[str, Form()],
                        account: User = Depends(current_active_user)):
    square = list(map(int, submission.split(",")))
    cur_score = magic_sos_score(square)
    await submit_low_score(cur_score, account, "magicsos")


@router.get("/magic-square-of-squares", response_class=HTMLResponse)
async def magic_sos(request: Request,
                    user: User = Depends(current_active_user)):
    return await render_lowest(request, 
                               user, 
                               "magicsos", 
                               "magic-square-of-squares.j2")
