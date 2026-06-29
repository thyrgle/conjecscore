How to Deploy Locally
=====================

------------
Dependencies
------------

In order to run the website locally, you will need:

- `npm <https://nodejs.org/en/download>`_
- `uv <https://docs.astral.sh/uv/getting-started/installation/>`_
- `just <https://just.systems/man/en/installation.html>`_

``npm`` will install `Tailwind <https://tailwindcss.com/>`_ and `Typescript <https://www.typescriptlang.org/>`_.

``uv`` installs various Python libraries, notably `FastAPI <https://fastapi.tiangolo.com/>`_ and `SQLAlchemy <https://www.sqlalchemy.org/>`_.

``just`` builds everything.

-------
Running
-------

You will first need to set up a ``.env`` file in the ``app`` directory. That is, you must add a file called ``.env`` in the ``app`` directory. The ``.env`` is used to store environment variables (some of which are secret). Your ``.env`` file may look something like:

.. code-block::

   SECRET="HELLO"
   DATABASE_URL="sqlite+aiosqlite:///:memory:"

This will make a temporary in memory database with sqlite. No extra dependencies needed. (Note: The production server uses PosgreSQL). Then to run the website:

.. code-block::

   just
