conjecscore
===========

[conjecscore.org](https://conjecscore.org/) is a website dedicated to open problems in mathematics that can be proven via construction. Furthermore, constructions that are not solution to the problem can be scored, informally, as to how closely they resemble a solution. conjecscore.org keeps track of scoreboards for these open prolems where users can compete or work together to find near or (hopefully) exact solutions to open problems.

Dependencies
============

In order to run the website locally, you will need:

- [npm](https://nodejs.org/en/download)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Postgresql](https://www.postgresql.org/download/)

`npm` will install [Tailwind](https://tailwindcss.com/) and [Typescript](https://www.typescriptlang.org/).

`uv` installs various Python libraries, notably [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/).

`Postgresql` is the underlying database.


Running
=======

You will first need to set up a `.env` file in the `app` directory. That is, you must add a file called `.env` in the `app` directory. The `.env` is used to store environment variables (some of which are secret). Your `.env` file may look something like:

```
SECRET="HELLO"
PGHOST=localhost
PGUSER=testuser
PGDATABASE=testdb
DATABASE_URL="postgresql+asyncpg://testuser:password@localhost:5432/testdb"
```

Assuming you use this as your `.env` you must also set up `Postgresql` to work with a user called `testuser`, password called `password` and database called `testdb`. To do so, first run the command `sudo -u postgres psql`. This will log you in as the default user. Then, to create the `testuser`, run:

```
CREATE USER testuser;
```

To create the database run:

```
CREATE DATABASE testdb;
```

To let the `testuser` have access to the `testdb` run:

```
ALTER DATABASE testdb OWNER TO testuser;
```

This only needs to be done once. After that, in order to start up the website on `localhost:8000`, just run:

```
make all
```
