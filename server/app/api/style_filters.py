from fastapi import APIRouter, File, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError

from app import crud, deps, schemas
from app.core import log, responses
from app.core.exceptions import BadRequestError, InternalServerError
from app.utils import FilterUploadResult, filter_storage

router = APIRouter()


@router.post(
    "/upload",
    summary="Upload filters",
    responses=responses.upload_style_filters,
    response_model=responses.upload_style_filters[status.HTTP_201_CREATED]["model"],
)
async def upload_filters(
    db: deps.db_dep,
    user: deps.current_user_dep,
    files: list[UploadFile] = File(..., description="Filters to upload"),
) -> schemas.http.UploadStyleFiltersOut:
    for file in files:
        if file.size and file.size > filter_storage.MAX_FILE_SIZE:
            max_file_size_in_mb = filter_storage.to_mb(filter_storage.MAX_FILE_SIZE)
            input_file_size_in_mb = filter_storage.to_mb(file.size)

            raise BadRequestError(
                message=(
                    f"File size must be less than {max_file_size_in_mb} MB "
                    f"{file.filename} is {input_file_size_in_mb} MB large"
                ),
                reason="Upload file size exceeded",
            )

    results: list[FilterUploadResult] = []

    for file in files:
        result = filter_storage.upload(file)
        if result:
            results.append(result)

    try:
        filters = await crud.style_filters.create_filters(db, results, user.id)
        return schemas.http.UploadStyleFiltersOut(
            filters=[filter.to_schema() for filter in filters]
        )
    except SQLAlchemyError as e:
        log.error(f"Failed to upload images: {e}. Deleting uploaded images")

        filter_storage.delete(img_ids=[img.img_id for img in results])

        raise InternalServerError()


# DELETE
# BAN
# GET authors
# SEARCH
