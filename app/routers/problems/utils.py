from sqlalchemy import asc, desc, select, insert, update

from fastapi import Request

from ...db import User, Entry, engine
from ...dependencies import templates


async def submit_low_score(score: int, account: User, problem: str):
    if score is None:
        return
    query = select(Entry).where(Entry.account_id == account.id) \
                         .where(Entry.problem == problem)
    async with engine.connect() as conn:
        results = await conn.execute(query)
        results = results.all()
        if len(results) == 0:
            statement = insert(Entry).values(account_id=account.id,
                                             account_name=account.nickname,
                                             account_email=account.email,
                                             problem=problem,
                                             score=score)
            await conn.execute(statement)
            await conn.commit()
        elif results[0].score > score:
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == problem)
                .values(score=score)
            )
            await conn.execute(statement)
            await conn.commit()


async def render_lowest(request: Request,
                        user: User, 
                        problem: str,
                        template_name: str):
    statement = select(Entry).where(Entry.problem == problem) \
                             .order_by(asc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = template_name,
                context = {
                    "leaderboard": results.all(),
                    "user": user
                }
        )


async def submit_high_score(score: int, account: User, problem: str):
    if score is None:
        return
    query = select(Entry).where(Entry.account_id == account.id) \
                         .where(Entry.problem == problem)
    async with engine.connect() as conn:
        results = await conn.execute(query)
        results = results.all()
        if len(results) == 0:
            statement = insert(Entry).values(account_id=account.id,
                                             account_name=account.nickname,
                                             account_email=account.email,
                                             problem=problem,
                                             score=score)
            await conn.execute(statement)
            await conn.commit()
        elif results[0].score < score:
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == problem)
                .values(score=score)
            )
            await conn.execute(statement)
            await conn.commit()


async def render_highest(request: Request,
                         user: User, 
                         problem: str,
                         template_name: str):
    statement = select(Entry).where(Entry.problem == problem) \
                             .order_by(desc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = template_name,
                context = {
                    "leaderboard": results.all(),
                    "user": user
                }
        )


def remove_two_pow(nums: list[int]) -> list[int]:
    while all([x % 2 == 0 for x in nums]):
        nums = [x // 2 for x in nums]
    return nums
