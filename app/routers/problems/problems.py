import os
import importlib
from fastapi import APIRouter

# Used by `register_problem` in `.utils` to hook all the pages to this router.
router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    responses={404: {"description": "Not found"}}
)


# For the problems.j2 template. Each entry in this list is the relative URL,
# the full name of the problem, and a preview image for the card. Such as:
# ("hadamard-determinant", "Hadamard Determinant", "hadamard.svg")
# Added to in the register_problem function.
problem_link_and_name: list[tuple] = []


for problem in os.listdir(path="app/routers/problems/"):
    # These are not problems.
    if problem in ("problems.py", "utils.py") or problem[-3:] != ".py":
        continue
    else:
        importlib.import_module("app.routers.problems." + problem[:-3])
