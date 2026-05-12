The Architecture
================

Here we give a deeper dive into how things are implemented (beyond making a simple problem). We first address the question, 

   how are problems actually imported into the website?

--------------------------
How Are Problems Imported?
--------------------------

If you are comming from "Adding a Simple Problem" you might be surprised at how little-to-no boilerplate is need when making a score function. We use some import magic for *both* the frontend verification and backend verification.

--------------------------------------
Backend Verification: Python Importing
--------------------------------------


