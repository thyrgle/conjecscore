from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select

from .dependencies import templates
from .db import User, engine, create_db_and_tables
from .schemas import UserCreate, UserRead, UserUpdate

from .users import auth_backend, fastapi_users
from .users import router as users_router
from .routers.problems import problems as probs


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
app.include_router(probs.router)


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


@app.get("/problems", response_class=HTMLResponse)
async def problems(request: Request):
    return templates.TemplateResponse(
            request = request,
            name = "problems.j2",
            context = {
                "problems": probs.problem_link_and_name
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


@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = RedirectResponse(
        url="/problems",
    )
    response.delete_cookie("fastapiusersauth")
    return response


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request = request,
            name = "index.j2",
            context = {}
    )
