from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_high_score, render_highest

router = APIRouter()


def score(n: [int]):
    if len(n) > 1:
        return None
    n = n[0]
    orbit = 0
    magnitude = n.bit_length()
    while n != 1:
        if n % 2 == 1:
            orbit += 1
            n = 3 * n + 1
        else:
            n = n // 2
    return int((orbit / magnitude) * 1000)


@router.post("/collatz-submit", response_class=HTMLResponse)
async def submit_collatz(submission: Annotated[str, Form()],
                        account: User = Depends(current_active_user)):
    nums = list(map(int, submission.split(",")))
    cur_score = score(nums)
    await submit_high_score(cur_score, account, "collatz")


@router.get("/collatz", response_class=HTMLResponse)
async def collatz(request: Request,
                    user: User = Depends(current_active_user)):
    return await render_highest(request, 
                                user, 
                                "collatz", 
                                "collatz.j2")
