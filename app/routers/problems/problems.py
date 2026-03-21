from collections import namedtuple
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
Variant = namedtuple('Variant', ['name', 'func_name'])
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

async def submit_score(score: int, variant: str | None,
                       account: User, problem_info: dict[str]):
    if score is None:
        return
    if variant is None:
        variant = "default"
    order = _submit_order_map[problem_info["order"]]
    query = select(Entry).where(Entry.account_id == account.id) \
                         .where(Entry.problem == problem_info["db_entry"]) \
                         .where(Entry.variant == variant)
    async with engine.connect() as conn:
        results = await conn.execute(query)
        results = results.all()
        if len(results) == 0:
            statement = insert(Entry).values(account_id=account.id,
                                             account_name=account.nickname,
                                             account_email=account.email,
                                             problem=problem_info["db_entry"],
                                             score=score,
                                             variant=variant)
            await conn.execute(statement)
            await conn.commit()
        elif order(results[0].score, score):
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == problem_info["db_entry"]) \
                .where(Entry.variant == variant)
                .values(score=score)
            )
            await conn.execute(statement)
            await conn.commit()


_render_order_map = {
    "lowest": asc,
    "highest": desc
}


async def render_score(request: Request, user: User, problem_info: dict[str]):
    order = _render_order_map[problem_info["order"]]
    statement = select(Entry).where(Entry.problem == problem_info["db_entry"]) \
                             .order_by(order(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement)
        variants = None
        variant_funcs = None
        default_name = None
        if problem_info["variants"] is not None:
            variants = []
            variant_funcs = []
            for var in problem_info["variants"]:
                variants.append(Variant(var["name"], var["score_func"]))
                variant_funcs.append(var["score_func"])
                default_name = problem_info["default_variant_name"]
        return templates.TemplateResponse(
                request = request,
                name = problem_info["template"],
                context = {
                    "leaderboard": results.all(),
                    "user": user,
                    "problem_title": problem_info["title"],
                    "submission_type": problem_info["submission_type"],
                    "js_file": problem_info["js_file_name"],
                    "variants": variants,
                    "variant_funcs": variant_funcs,
                    "default_name": default_name,
                }
        )


def register_problem(mod, problem_info):
    # Register default problem.
    get = router.get("/" + problem_info["route"], response_class=HTMLResponse)
    async def prob_page(request: Request,
                        user: User=Depends(current_active_user)):
        return await render_score(request, user, problem_info)
    get(prob_page)

    # Register variants.
    try:
        for variant in problem_info["variants"]:
            get = router.get(
                "/" + problem_info["route"] + "-" + variant["name"],
                         response_class=HTMLResponse)
            async def prob_page(request: Request,
                                user: User=Depends(current_active_user)):
                return await render_score(request, variant["name"],
                                          user, problem_info)

            get(prob_page)
    except KeyError:
        # No variants, just move on.
        pass

    
    # Register default problem.
    post = router.post("/" + problem_info["route"] + "-submit",
                       response_class=HTMLResponse)
    async def prob_submit(submission: Annotated[str, Form()],
                          user: User=Depends(current_active_user)):
        data = parse_table[problem_info["submission_type"]](submission)
        score = getattr(mod, problem_info["score_func"])
        await submit_score(await score(data), user, problem_info)
    post(prob_submit)

    try:
        # Register variants (if they exist).
        for variant in problem_info["variants"]:
            post = router.post(
                "/" + problem_info["route"] + "-" + variant["name"] +  "-submit",
                response_class=HTMLResponse
            )
            async def prob_submit(submission: Annotated[str, Form()],
                                  user: User=Depends(current_active_user)):
                data = parse_table[problem_info["submission_type"]](submission)
                score = getattr(mod, variant["score_func"])
                await submit_score(await score(data), user, problem_info)
            post(prob_submit)
    except KeyError:
        # No variants, move on.
        pass


for problem_entry in os.listdir(path="app/routers/problems/registry"):
    with open("app/routers/problems/registry/" + problem_entry, 'r') as pe:
        problem_info = json.loads(pe.read())
    # -5 to exclude .json
    problem_registry[problem_entry[:-5]] = problem_info
    pyfile = importlib.import_module(
            "app.routers.problems." + problem_info["python_file_name"][:-3]
    )
    register_problem(pyfile, problem_info)
