from fastapi.templating import Jinja2Templates

# Shared templating engine. `app/problems` is also on the search path so each
# problem's `problem.j2` can be loaded as `{problem name}/problem.j2`.
templates = Jinja2Templates(directory=["templates", "app/problems"])
