from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def test_get() -> JSONResponse:
    return JSONResponse({"message": "Hello from Picasso"})
