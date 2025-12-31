import json
from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse

from ...db import User
from ...users import current_active_user

from .utils import submit_low_score, render_lowest

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
async def submit_graph(submission: Annotated[str, Form()],
                       account: User = Depends(current_active_user)):
    graph = json.loads(submission)
    cur_score = conway_score(graph, 99)
    await submit_low_score(cur_score, account, "conway99")    


@router.get("/conway-99", response_class=HTMLResponse)
async def conway(request: Request,
                 user: User = Depends(current_active_user)):
    return await render_lowest(request, user, "conway99", "conway99.j2")
