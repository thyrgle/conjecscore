from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

import numpy as np
from sympy import Matrix

from ...db import User
from ...users import current_active_user

from .utils import submit_high_score, render_highest

router = APIRouter()


def score(mat: [int]):
    if len(mat) != 23 * 23:
        return None
    for num in mat:
        if num != 1 and num != -1:
            return None
    np_mat = np.reshape(mat, (23, 23))
    sym_mat = Matrix(np_mat)
    return sym_mat.det() // (10 ** 9)


@router.post("/hadamard-determinant-submit", response_class=HTMLResponse)
async def submit_hadamard_det(submission: Annotated[str, Form()],
                              account: User = Depends(current_active_user)):
    nums = list(map(int, submission.split(",")))
    cur_score = score(nums)
    await submit_high_score(cur_score, account, "haddet")


@router.get("/hadamard-determinant", response_class=HTMLResponse)
async def hadamard_determinant(request: Request,
                               user: User = Depends(current_active_user)):
    return await render_highest(request, 
                                user, 
                                "haddet", 
                                "hadamard-determinant.j2")
