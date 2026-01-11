from fastapi import APIRouter
from .conway import router as conway_router
from .magicsos import router as magicsos_router
from .taxicab import router as taxicab_router
from .collatz import router as collatz_router
from .hadamard_determinant import router as hadamard_determinant_router


router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    responses={404: {"description": "Not found"}}
)

router.include_router(conway_router)
router.include_router(magicsos_router)
router.include_router(taxicab_router)
router.include_router(collatz_router)
router.include_router(hadamard_determinant_router)
