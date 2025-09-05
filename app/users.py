from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .dependencies import templates

router = APIRouter()

@router.get("/users/newaccount", response_class=HTMLResponse)
async def new_account(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="newaccount.j2",
        context={}
    )
