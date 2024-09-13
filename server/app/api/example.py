from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def example_get() -> JSONResponse:
    return JSONResponse(
        {
            "message": "Hello from Picasso",
            "context": "This is an example GET endpoint.",
        }
    )
