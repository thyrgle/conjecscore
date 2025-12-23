from contextlib import asynccontextmanager
import json
import math
from statistics import mean, pvariance
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import asc, select, insert, update

from .dependencies import templates
from .users import router as users_router
from fastapi import Depends
from .db import User, Entry, engine, create_db_and_tables
from .schemas import UserCreate, UserRead, UserUpdate
from .users import auth_backend, current_active_user, fastapi_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt", 
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users_router)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.j2",
        context={}
    )


@app.get("/register", response_class=HTMLResponse)
async def new_account(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="newaccount.j2",
        context={}
    )


def conway_score(graph, n):
    bad_count = 0
    for i in range(n):
        for j in range(i+1, n):
            c = len(set(graph[str(i)]) & set(graph[str(j)]))
            e = int(i in graph[str(j)])
            bad_count += (c - (2 - e)) * (c - (2 - e))
    return bad_count


@app.get("/problems", response_class=HTMLResponse)
async def problems(request: Request):
    return templates.TemplateResponse(
            request = request,
            name = "problems.j2",
            context = {}
    )


@app.post("/conway-submit", response_class=HTMLResponse)
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


@app.get("/conway-99", response_class=HTMLResponse)
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


@app.post("/magicsos-submit", response_class=HTMLResponse)
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


@app.get("/magic-square-of-squares", response_class=HTMLResponse)
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


@app.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    statement = select(User.nickname)
    async with engine.connect() as conn:
        names = await conn.execute(statement)
        return templates.TemplateResponse(
                request = request,
                name = "users.j2",
                context = {
                    "names": names.all()
                }
        )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request = request,
            name = "index.j2",
            context = {}
    )
