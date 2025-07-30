import json
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import asc
from sqlalchemy.dialects.sqlite import JSON

class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author: str
    graph: dict = Field(sa_type=JSON, nullable=False)
    score: int


def score(graph):
    bad_count = 0
    for i in range(99):
        for j in range(i+1, 99):
            c = len(graph[i] & graph[j])
            e = int(i in graph[j])
            bad_count += ((c - (2 - e)) * (c - (2 - e)))
    return bad_count


engine = create_engine("sqlite:///cw.db")
SQLModel.metadata.create_all(engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/")
async def submit_graph(author: Annotated[str, Form()], 
                       graph: Annotated[str, Form()]):
    graph = json.loads(graph)
    entry = Entry(author=author, graph=graph, score=6)
    with Session(engine) as session:
        session.add(entry)
        session.commit()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    with Session(engine) as session:
        statement = select(Entry).order_by(asc(Entry.score)).limit(10)
        results = session.exec(statement) 
        return templates.TemplateResponse(
                request=request, 
                name="index.html", 
                context={"leaderboard": results.all()}
        )
