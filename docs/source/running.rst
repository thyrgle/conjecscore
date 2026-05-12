How to Deploy Locally
=====================

------------
Dependencies
------------

In order to run the website locally, you will need:

- `npm <https://nodejs.org/en/download>`_
- `uv <https://docs.astral.sh/uv/getting-started/installation/>`_
- `Postgresql <https://www.postgresql.org/download/>`_
- `just <https://just.systems/man/en/installation.html>`_

``npm`` will install `Tailwind <https://tailwindcss.com/>`_ and `Typescript <https://www.typescriptlang.org/>`_.

``uv`` installs various Python libraries, notably `FastAPI <https://fastapi.tiangolo.com/>`_ and `SQLAlchemy <https://www.sqlalchemy.org/>`_.

``Postgresql`` is the underlying database.

-------
Running
-------

You will first need to set up a ``.env`` file in the ``app`` directory. That is, you must add a file called ``.env`` in the ``app`` directory. The ``.env`` is used to store environment variables (some of which are secret). Your ``.env`` file may look something like:

.. code-block::

   SECRET="HELLO"
   PGHOST=localhost
   PGUSER=testuser
   PGDATABASE=testdb
   DATABASE_URL="postgresql+asyncpg://testuser:password@localhost:5432/testdb"

Assuming you use this as your ``.env`` you must also set up ``Postgresql`` to work with a user called ``testuser``, password called ``password`` and database called ``testdb``. To do so, first run the command ``sudo -u postgres psql``. This will log you in as the default user. Then, to create the ``testuser``, run:

.. code-block::

   CREATE USER testuser;
   ALTER USER testuser WITH PASSWORD 'password';

To create the database run:

.. code-block::
   CREATE DATABASE testdb;

To let the ``testuser`` have access to the ``testdb`` run:

.. code-block::

   ALTER DATABASE testdb OWNER TO testuser;

This only needs to be done once. After that, in order to start up the website on ``localhost:8000``, just run:

.. code-block::

   just

Note: If you are running Windows you may need to specify a different URL. Change the ``backend`` recipe in the ``justfile`` from:

.. code-block::
   uv run fastapi run app/main.py

to:

.. code-block::

   uv run fastapi run --host 127.0.0.1 app/main.py
