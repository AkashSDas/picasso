from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def example_get() -> JSONResponse:
    return JSONResponse(
        {
            "message": "Hello from Picasso",
            "context": "This is an example GET endpoint.",
        }
    )
