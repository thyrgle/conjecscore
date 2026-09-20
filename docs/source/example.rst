Adding a Simple Problem
=======================

conjecscore consists of relaxations of open problems in mathematics. In particular, problems are recast as optimization problems where an ideal score often has a score of ``0``. This is not *always* the case, but we will follow that guideline for the simple problem here. Fortunately, little to no knowledge of web development is needed for adding a problem, much of that is abstracted away.

Every problem lives in a single directory, ``conjecscore/app/problems/{problem name}/``, which contains *all* the files needed for the problem:

.. code-block::

   conjecscore/app/problems/closetofive/
   ├── problem.json   # The metadata that registers the problem.   ├── score.py       # The backend (server-side) score function.
   ├── score.ts       # The frontend (browser-side) score function.
   ├── problem.j2     # The problem's page (description, formula, etc.).
   └── image.svg      # The preview image shown on the /problems page.

This tutorial walks through creating each of these files for the toy problem below.

--------------
How Close to 5
--------------

As an example, we will consider the following toy problem:

   Find a number that is as close as possible to ``5``.

Of course, this not an open problem. An optimal score is simply to give the number ``5``. To see how close we are to ``5``, given another number ``x``, we can compute the score as ``abs(x - 5)``. We will need to implement this score function twice.

.. note::

   It is a little unfortunate, but we need ``2`` implementations of the score function for each problem. One implementation in Python, and the other in Typescript. Why? Each implementation serves a different purpose. The Typescript implementation is referred to as the "frontend verification" and the Python implementation is referred to as the "backend verification".
   Given an honest user, they may mistake and submit either an erroneous input. We catch these mistakes and do *not* send them to the server for efficiency purposes. The Typescript implementation checks for erroneous inputs in the browser and saves computation power.
   Unfortunately, a user can be malicious and change the Typescript implementation on their side. Thus, in the case of a malicious user, we must always validate the input on our side to make sure no cheating is involved. The Python implementaiton *cannot* be modified by the user and is instead ran on the server to handle this case. Furthermore, the Python code also updates the database but that is handled for you, so you do not need to worry about that while making a problem.

-------------------------
The Python Implementation
-------------------------

Create the problem directory ``conjecscore/app/problems/closetofive/``. Inside it, create a file called ``score.py`` and write:

.. code-block:: python

   from numbers import Number

   async def score(n: int):
       if not isinstance(n, Number):
           return None
       return abs(n - 5)

That's it! We check if the input is valid (that is, ``n`` is a number) and if it is not valid, we return ``None``. Then we simply return the score as proposed above.

.. note::

   If you are confused about the ``async`` keyword it is safe to not worry about it now. This is mostly for computationally intensive score functions. The ``async`` keyword (in conjunction with the ``asyncio.sleep`` function allows for the server to periodically "take breaks" and help keep things running smoothly. For a simple score function like this, we do not need to worry about it.

-------------------------
Typescript Implementation
-------------------------

In the same problem directory, add the file ``score.ts``:

.. code-block:: typescript

   export async function score(n: bigint): Promise<bigint> {
     try {
       return n >= 5n ? n - 5n : 5n - n;
     } catch (e) {
       console.error(e);
       return "Could not score input!";
     }
   }

.. DANGER::

   ``Math.abs(n - 5n)`` might seem reasonable, but ``Math.abs`` works on floating-point numbers and may lose precision for extremely large values. The ternary expression used above avoids this issue.

A couple things to note: We often support Javascript `bigint <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt>`_ so please check the link and become familiar with the quirks (like why there is an ``n`` after ``5``). Also, (like mentioned above in the first note) a user may accidentally enter a non-number. We prevent that from being sent to the server by returning a ``string`` that corresponds to the error message.

---------------------
A Problem Description
---------------------

We should also supply details like how the problem is scored, references, etc. to the user. Currently, the user has *no idea* what the score function is or even the problem is asking. All they can do is submit blindly.

To fix this, in the same problem directory create a file called ``problem.j2`` and fill it with:

.. code-block::

   {% extends "problem_template.j2" %}

   {% block problem_description %}
   <p>
   Find a number as close as possible to \(5\).
   </p>
   {% endblock %}

   {% block submission_format %}
   <p>
   Please input a single number. Let the single number be denoted as \(x\). The score is computed as:

   $$\left|x - 5\right|$$
   </p>
   {% endblock %}
   {% block score_func %}
   from numbers import Number

   def score(n: int):
       if not isinstance(n, Number):
           return None
       return abs(n - 5)
   {% endblock %}

A problem description has ``3`` parts: ``problem_description`` contains basic information on the problem. ``submission_format`` contains information on the data format that the user should submit to get scored (i.e. a number, CSV file, or JSON file are common ones) as well as a formula for explicitly describing how the problem is scored. ``score_func`` is similar to the server verification code and it is used to help the user get started on problem.

.. note::

   ``score_func`` is usually not the *same* as the server verification code because it excludes references to ``async`` that the server uses.


---------------------------------
An Image for the ``/problems`` Page
---------------------------------

An image (in particular, an SVG) must be supplied for the problem to be listed on the ``/problems`` page. Save it as ``image.svg`` inside the problem directory:

.. image:: closetofive.svg

Make sure that it is named ``image.svg``. This is so the problem is listed in ``https://conjecscore.org/problems`` and so that it displays properly.

-------------------------------------------
One Final Step: Putting Everything Together
-------------------------------------------

Finally, we will register the problem. Create the file ``problem.json`` inside the problem directory with the contents:

.. code-block:: json

   {
     "route": "closetofive",
     "db_entry": "closetofive",
     "title": "Close To Five",
     "order": "lowest",
     "submission_type": "text",
     "variants": {
       "default": { "name": "default", "score_func": "score"}
     }
   }

Since every problem directory uses the same file names, the registry only describes the things that are genuinely particular to the problem:

- ``db_entry``: The database contains a collection of problem submissions. ``db_entry`` refers to the value for the column ``problem``. This is so we can look up submissions for the particular problem.
- ``title``: The name of the problem the user sees.
- ``order``: As alluded to above, *most* of the time the ideal score is a low score of ``0``, but sometimes we want to make the number as large as possible too. Depending on whether we want a low or high score we supply the option ``"lowest"`` or ``"highest"``, respectively.
- ``variants``: There might be "variants" such as different sizes for a particular open problem. We only have one here, but we should indicate the name of the ``score_func`` associated with the ``default`` variant.
- ``route``: Indicates the route should be ``https://conjecscore.org/problems/closetofive``. That is, this is the name of the route where the user can see the problem.

.. note::

   The directory name (``closetofive``) and the ``route`` do not have to match, but keeping them the same is the convention on this site.

Now that the problem directory is complete, all the files can be found by the application and the problem is operational! To see everything in action, run:

.. code-block::

   just

.. note::

   ``just`` first compiles the frontend and then the backend. Furthermore, ``npm`` is ran first, then ``tailwind``, and finally ``fastapi`` is ran. If you receive an error, you can check to see which tool failed.

Then navigate to:

.. code-block::

   http://127.0.0.1:8000/

If you click on the ``Problems`` button right below the logo you will go to a list of problem. "Close To Five" should now appear as one of those options and clicking it will take you to ``http://127.0.0.1:8000/problems/closetofive``.

Once on the page, inputing a score of ``5`` (for instance) will result in "You scored 0!". Refreshing the page will then display your score (assuming you are logged in.) If you input something like ``a``, it will instead display "Your input could not be scored!"

---------------
Common Mistakes
---------------

- Incorrect naming: the files in a problem directory must use the exact names listed at the top of this tutorial (``problem.json``, ``score.py``, ``score.ts``, ``problem.j2`` and ``image.svg``). Otherwise, various problems can happen:

  - No SVG will show up (instead a missing image placeholder will show up) if the image is not named ``image.svg``.
  - A ``problem.j2`` that is missing or misplaced will cause the page to crash completely.
  - Using the incorrect ``route`` will cause a ``404`` if that page is accessed. (However, you should be able to access the page at the incorrect name.)
  - Incorrect ``submission_type`` will mean a different kind of submission needs to be supplied. In this case, the textbox will no longer appear below the scoreboard. Instead, a file will be required.

- The logic for the serverside (Python) verifcation and clientside (Typescript) verification are different.

  - Various issues related issues can occur. In every case, the message the user receives below the textbox will not match the scoreboard for some inputs.
