import fastapi

from .alloc import router as alloc_router

router = fastapi.APIRouter(prefix="/cloud")
router.include_router(alloc_router)
