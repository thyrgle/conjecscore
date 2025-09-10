from contextlib import asynccontextmanager
import json
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import asc, select, insert

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


def score(graph, n):
    bad_count = 0
    for i in range(n):
        for j in range(i+1, n):
            if j > n:
                continue
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


@app.post("/conway-submit")
async def submit_graph(graph: Annotated[str, Form()],
                       account: User = Depends(current_active_user)):
    graph = json.loads(graph)
    statement = insert(Entry).values(account=account, score=score(graph, 99))
    async with engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()


@app.get("/conway-99", response_class=HTMLResponse)
async def conway(request: Request,
                 user: User = Depends(current_active_user)):
    statement = select(Entry).order_by(asc(Entry.score)).limit(10)
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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request = request,
            name    = "index.j2",
            context = {}
    )
