import os
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_low_score, render_lowest

router = APIRouter()


def score(nums: list[int]):
    # Ensure there are 4 numbers
    if len(nums) != 4:
        return None
    # Ensure there are distinct elements.
    if len(set(nums)) != 4:
        return None
    
    a, b, c, d = nums
    big = bin(max(a ** 5 + b ** 5, c ** 5 + d ** 5))[2::] # Drop the '0b'
    small = bin(min(a ** 5 + b ** 5, c ** 5 + d ** 5))[2::] # Drop the '0b'
    i = len(small)
    while i < len(big):
        small += "0"
        i += 1
    pre = os.path.commonprefix([big, small]) + 1
    suf = os.path.commonprefix([big[::-1], small[::-1]]) + 1
    return (1 - min(suf, pre) / (len(big) + 1)) * (10 ** 6)


@router.post("/taxicab-submit", response_class=HTMLResponse)
async def submit_square(submission: Annotated[str, Form()],
                        account: User = Depends(current_active_user)):
    nums = list(map(int, submission.split(",")))
    cur_score = score(nums)
    await submit_low_score(cur_score, account, "taxicab")


@router.get("/taxicab", response_class=HTMLResponse)
async def taxicab(request: Request,
                    user: User = Depends(current_active_user)):
    return await render_lowest(request, 
                               user, 
                               "taxicab", 
                               "taxicab.j2")
