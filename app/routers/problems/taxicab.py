import os
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_low_score, render_lowest

router = APIRouter()


def score(nums: list[int]):
    if len(nums) != len(set(nums)):
        return None
    if len(nums) != 4:
        return None
    a, b, c, d = nums
    big = bin(max(a ** 5 + b ** 5, c ** 5 + d ** 5))[2::]
    small = bin(min(a ** 5 + b ** 5, c ** 5 + d ** 5))[2::]
    size = len(big)
    pre = lambda x: len(os.path.commonprefix(x))
    if size != len(small):
        return 10 ** 6
    else:
        return int((1 - (pre([big, small]) * (1/ size))) * 10 ** 6)


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
