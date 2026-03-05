import os
import importlib
import json
from typing import Annotated

from sqlalchemy import asc, desc, select, insert, update

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse

from ...db import User, Entry, engine
from ...users import current_active_user
from ...dependencies import templates

# Used by `register_problem` in `.utils` to hook all the pages to this router.
router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    responses={404: {"description": "Not found"}}
)


# For the problems.j2 template. Each entry in this list is the relative URL,
# the full name of the problem, and a preview image for the card. Such as:
# ("hadamard-determinant", "Hadamard Determinant", "hadamard.svg")
# Added to in the register_problem function.
problem_registry: dict[dict] = {}


def parse_JSON(submission):
    return json.loads(submission)


def parse_CSV(submission):
    return list(map(int, submission.split(",")))


def parse_integer(submission):
    return int(submission)


parse_table = {
    "json": parse_JSON,
    "csv": parse_CSV,
    "text": parse_integer
}


_submit_order_map = {
    "lowest": lambda x,y: x > y,
    "highest": lambda x,y: x < y
}

async def submit_score(score: int, account: User, problem: str, order):
    score = await score
    if score is None:
        return
    order = _submit_order_map[order]
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
        elif order(results[0].score, score):
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == problem)
                .values(score=score)
            )
            await conn.execute(statement)
            await conn.commit()


_render_order_map = {
    "lowest": asc,
    "highest": desc
}

async def render_score(request: Request, user: User,
                       problem: str, template: str, submission_type: str,
                       order: str):
    order = _render_order_map[order]
    statement = select(Entry).where(Entry.problem == problem) \
                             .order_by(order(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = template,
                context = {
                    "leaderboard": results.all(),
                    "user": user,
                    "submission_type": submission_type
                }
        )


def register_problem(mod, problem_info):
    get = router.get("/" + problem_info["route"], response_class=HTMLResponse)
    async def prob_page(request: Request,
                        user: User=Depends(current_active_user)):
        return await render_score(request, user,
                                  problem_info["db_entry"],
                                  problem_info["template"],
                                  problem_info["submission_type"],
                                  problem_info["order"])
    get(prob_page)

    post = router.post("/" + problem_info["route"] + "-submit",
                       response_class=HTMLResponse)
    async def prob_submit(submission: Annotated[str, Form()],
                          user: User=Depends(current_active_user)):
        data = parse_table[problem_info["submission_type"]](submission)
        score = getattr(mod, problem_info["score_func"])
        await submit_score(score(data), user,
                           problem_info["db_entry"],
                           problem_info["order"])
    post(prob_submit)


for problem_entry in os.listdir(path="app/routers/problems/registry"):
    with open("app/routers/problems/registry/" + problem_entry, 'r') as pe:
        problem_info = json.loads(pe.read())
    # -4 to exclude .json
    problem_registry[problem_entry[:-4]] = problem_info
    # These are not problems.
    pyfile = importlib.import_module(
            "app.routers.problems." + problem_info["python_file_name"][:-3]
    )
    register_problem(pyfile, problem_info)
