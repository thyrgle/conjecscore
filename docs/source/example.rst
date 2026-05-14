Adding a Simple Problem
=======================

conjecscore consists of relaxations of open problems in mathematics. In particular, problems are recast as optimization problems where an ideal score often has a score of ``0``. This is not *always* the case, but we will follow that guideline for the simple problem here. Fortunately, little to no knowledge of web development is needed for adding a problem, much of that is abstracted away.

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

Change directories to ``conjecscore/app/routers/problems/``. In this file there are various Python files, each file corresponds to a Python implementation of a score function. To add the new problem, create a file in the directory called ``close_to_five.py`` and write:

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

Now change the directory to the ``conjecscore/static/scores`` directory. In this directory there are Typescript files with score functions. Add the file ``closetofive.ts``:

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

To fix this, change the directory to ``conjecscore/templates/`` and create a file called ``closefive.j2`` and fill it with:

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

An image (in particular, an SVG) must be supplied for the problem to be listed on the ``/problems`` page. Add the following image to ``conjecscore/static/images``

.. image:: closetofive.svg

Make sure that it is named ``closetofive.svg``. This is so the problem is listed in ``https://conjecscore.org/problems`` and so that it displays properly.

-------------------------------------------
One Final Step: Putting Everything Together
-------------------------------------------

Go to ``conjecscore/app/routers/problems/registry``. We will now register the problem, that is give the names of the files we used so the website can "sniff" them out and make a page for them.

Add the file ``closefive.json`` to the registry with the contents:

.. code-block:: json

   {
     "python_file_name": "close_to_five.py",
     "js_file_name": "closetofive.js",
     "db_entry": "closetofive",
     "route": "closetofive",
     "title": "Close To Five",
     "template": "closefive.j2",
     "order": "lowest",
     "variants": {
       "default": { "name": "default", "score_func": "score"}
     },
     "image": "closetofive.svg",
     "submission_type": "text"
   }

We are mostly supplying names of the files we created. However, there are a couple options that not just file names:

- ``db_entry``: The database contains a collection of problem submissions. ``db_entry`` refers to the value for the column ``problem``. This is so we can look up submissions for the particular problem.
- ``title``: The name of the problem the user sees.
- ``order``: As alluded to above, *most* of the time the ideal score is a low score of ``0``, but sometimes we want to make the number as large as possible too. Depending on whether we want a low or high score we supply the option ``"lowest"`` or ``"highest"``, respectively.
- ``variants``: There might be "variants" such as different sizes for a particular open problem. We only have one here, but we should indicate the name of the ``score_func`` associated with the ``default`` variant.
- ``route``: Indicates the route should be ``https://conjecscore.org/problems/closetofive``. That is, this is the name of the route where the user can see the problem.

.. DANGER::

   We use the generated *Javascript* file name. Not the *Typescript* name. Observe the extension is ``.js`` not ``.ts``.

Now that everything is in the registry, all the files can be found by the application and the problem is operational!
