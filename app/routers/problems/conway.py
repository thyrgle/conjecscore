import json
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import asc, select, insert, update

from ...dependencies import templates
from ...db import User, Entry, engine
from ...users import current_active_user


router = APIRouter()


def conway_score(graph, n):
    bad_count = 0
    for i in range(n):
        for j in range(i+1, n):
            c = len(set(graph[str(i)]) & set(graph[str(j)]))
            e = int(i in graph[str(j)])
            bad_count += (c - (2 - e)) * (c - (2 - e))
    return bad_count


@router.post("/conway-submit", response_class=HTMLResponse)
async def submit_graph(graph: Annotated[str, Form()],
                       account: User = Depends(current_active_user)):
    graph = json.loads(graph)
    cur_score = conway_score(graph, 99)
    query = select(Entry).where(Entry.account_id == account.id) \
                         .where(Entry.problem == "conway99")
    async with engine.connect() as conn:
        results = await conn.execute(query)
        results = results.all()
        if len(results) == 0:
            statement = insert(Entry).values(account_id=account.id,
                                             account_name=account.nickname,
                                             account_email=account.email,
                                             problem="conway99",
                                             score=cur_score)
            await conn.execute(statement)
            await conn.commit()
        elif results[0].score > cur_score:
            statement = (
                update(Entry)
                .where(Entry.account_id == account.id) \
                .where(Entry.problem == "conway99")
                .values(score=cur_score)
            )
            await conn.execute(statement)
            await conn.commit()


@router.get("/conway-99", response_class=HTMLResponse)
async def conway(request: Request,
                 user: User = Depends(current_active_user)):
    statement = select(Entry).where(Entry.problem == "conway99") \
                             .order_by(asc(Entry.score)).limit(10)
    async with engine.connect() as conn:
        results = await conn.execute(statement) 
        return templates.TemplateResponse(
                request = request,
                name = "conway99.j2", 
                context = {
                    "leaderboard": results.all(),
                    "user": user
                }
        )
