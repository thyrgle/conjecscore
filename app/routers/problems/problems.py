from fastapi import APIRouter
from .conway import router as conway_router
from .magicsos import router as magicsos_router


router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    responses={404: {"description": "Not found"}}
)

router.include_router(conway_router)
router.include_router(magicsos_router)
