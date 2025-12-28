import math
from statistics import pvariance, mean
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import asc, select, insert, update

from ...dependencies import templates
from ...db import User, Entry, engine
from ...users import current_active_user


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
async def submit_square(square: Annotated[str, Form()],
                        account: User = Depends(current_active_user)):
    square = list(map(int, square.split(",")))
    cur_score = magic_sos_score(square)
    if cur_score is None:
        return # Invalid square.
    query = select(Entry).where(Entry.account_id == account.id) \
                         .where(Entry.problem == "magicsos")
    async with engine.connect() as conn:
        results = await conn.execute(query)
        results = results.all()
        if len(results) == 0:
            statement = insert(Entry).values(account_id=account.id,
                                             account_name=account.nickname,
                                             account_email=account.email,
                                             problem="magicsos",
                                             score=cur_score)
            await conn.execute(statement)
            await conn.commit()
        elif results[0].score > cur_score:
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == "magicsos")
                .values(score=cur_score)
            )
            await conn.execute(statement)
            await conn.commit()


@router.get("/magic-square-of-squares", response_class=HTMLResponse)
async def magic_sos(request: Request,
                    user: User = Depends(current_active_user)):
    statement = select(Entry).where(Entry.problem == "magicsos") \
                             .order_by(asc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = "magic-square-of-squares.j2",
                context = {
                    "leaderboard": results.all(),
                    "user": user
                }
        )
