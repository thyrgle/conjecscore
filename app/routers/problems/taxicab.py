import os
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_low_score, render_lowest, remove_two_pow

router = APIRouter()


def score(nums: list[int]):
    # Ensure there are no duplicate numbers
    if len(nums) != len(set(nums)):
        return None
    # Ensure 4 numbers are supplied.
    if len(nums) != 4:
        return None
    # Ensure numbers are positive.
    for num in nums:
        if num <= 0:
            return None
    nums = remove_two_pow(nums)

    a, b, c, d = nums
    c1 = bin(a ** 5 + b ** 5)[2::][::-1]
    c2 = bin(c ** 5 + d ** 5)[2::][::-1]
    size = len(c1)
    if size != len(c2):
        return 10 ** 6
    pre = len(os.path.commonprefix([c1, c2]))
    return int((1 - pre / size) * 10 ** 6)


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
