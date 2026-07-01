conjecscore
===========

[conjecscore.org](https://conjecscore.org/) is a website dedicated to open problems in mathematics that can be proven via construction. Furthermore, constructions that are not solution to the problem can be scored, informally, as to how closely they resemble a solution. conjecscore.org keeps track of scoreboards for these open prolems where users can compete or work together to find near or (hopefully) exact solutions to open problems.

Dependencies
============

In order to run the website locally, you will need:

- [npm](https://nodejs.org/en/download)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://just.systems/man/en/)

`npm` will install [Tailwind](https://tailwindcss.com/) and [Typescript](https://www.typescriptlang.org/).

`uv` installs various Python libraries, notably [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/).

`just` builds everything.

Running
=======

You will first need to set up a `.env` file in the `app` directory. That is, you must add a file called `.env` in the `app` directory. The `.env` is used to store environment variables (some of which are secret). Your `.env` file may look something like:

```
SECRET="HELLO"
DATABASE_URL="sqlite+aiosqlite:///:memory:"
```

This will make a temporary in memory database with sqlite. No extra dependencies needed. (Note: The production server uses PostgreSQL.) Then to run the website type:

```
just
```

# Contributing

If you are interested in contributing checkout the documentation on [Readthedocs.](https://conjecscore.readthedocs.io/en/latest/index.html)
