import json
from typing import Annotated

from sqlalchemy import asc, desc, select, insert, update

from fastapi import Request, Depends, Form
from fastapi.responses import HTMLResponse

from ...db import User, Entry, engine
from ...users import current_active_user

from ...dependencies import templates
from .problems import router, problem_link_and_name


def parse_JSON(submission):
    return json.loads(submission)


def parse_CSV(submission):
    return list(map(int, submission.split(",")))


def parse_integer(submission):
    return int(submission)


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
                        template_name: str,
                        submission_type: str):
    statement = select(Entry).where(Entry.problem == problem) \
                             .order_by(asc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = template_name,
                context = {
                    "leaderboard": results.all(),
                    "user": user,
                    "submission_type": submission_type
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
                         template_name: str,
                         submission_type: str):
    statement = select(Entry).where(Entry.problem == problem) \
                             .order_by(desc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = template_name,
                context = {
                    "leaderboard": results.all(),
                    "user": user,
                    "submission_type": submission_type
                }
        )


def remove_two_pow(nums: list[int]) -> list[int]:
    while all([x % 2 == 0 for x in nums]):
        nums = [x // 2 for x in nums]
    return nums


def register_problem(name, score, full_name, 
                     template, order, db_entry, parse_submission, image,
                     submission_type="file"):
    problem_link_and_name.append((name, full_name, image))
    get = router.get("/" + name, response_class=HTMLResponse)
    if order == "lowest":
        async def prob_page(request: Request,
                            user: User=Depends(current_active_user)):
            return await render_lowest(request,
                                       user,
                                       db_entry,
                                       template,
                                       submission_type)
        get(prob_page)
    elif order == "highest":
        async def prob_page(request: Request,
                            user: User=Depends(current_active_user)):
            return await render_highest(request,
                                        user,
                                        db_entry,
                                        template,
                                        submission_type)
        get(prob_page)

    post = router.post("/" + name + "-submit", response_class=HTMLResponse)
    if order == "lowest":
        async def prob_submit(submission: Annotated[str, Form()],
                              user: User = Depends(current_active_user)):
            data = parse_submission(submission)
            await submit_low_score(score(data), user, db_entry)
        post(prob_submit)
    elif order == "highest":
        async def prob_submit(submission: Annotated[str, Form()],
                              user: User = Depends(current_active_user)):
            data = parse_submission(submission)
            await submit_high_score(score(data), user, db_entry)
        post(prob_submit)
