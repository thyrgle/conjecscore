import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import asc
from sqlalchemy.dialects.sqlite import JSON

from .dependencies import templates
from .users import router as users_router

@dataclass_json
@dataclass
class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    author: str
    graph: dict = Field(sa_type=JSON, nullable=False)
    score: int


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


engine = create_engine("sqlite:///cw.db")
SQLModel.metadata.create_all(engine)


app      = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users_router)


@app.get("/problems", response_class=HTMLResponse)
async def problems(request: Request):
    return templates.TemplateResponse(
            request = request,
            name    = "problems.html",
            context = {}
    )


@app.post("/conway-submit")
async def submit_graph(author: Annotated[str, Form()], 
                       graph: Annotated[str, Form()]):
    graph = json.loads(graph)
    entry = Entry(author=author, graph=graph, score=score(graph, 99))
    with Session(engine) as session:
        session.add(entry)
        session.commit()


@app.get("/conway-99", response_class=HTMLResponse)
async def conway(request: Request):
    with Session(engine) as session:
        statement = select(Entry).order_by(asc(Entry.score)).limit(10)
        results   = session.exec(statement) 
        return templates.TemplateResponse(
                request = request,
                name    = "conway99.html", 
                context = {"leaderboard": results.all()}
        )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request = request,
            name    = "index.html",
            context = {}
    )


@app.get("/data", response_class=FileResponse)
async def download(request: Request):
    # TODO: Make this download the json file to the user
    with Session(engine) as session:
        # export the contents of the database as a JSON file
        statement = select(Entry) 
        results   = session.exec(statement)
        first     = True

        with open("data/output.json", "w") as file:
            file.write("{")
            for entry in results:
                if (not first):
                    file.write(", ")
                first = False
                file.write(entry.to_json()[1:-1])
                print (entry.to_json())
            file.write("}")
            
        return "data/output.json"
