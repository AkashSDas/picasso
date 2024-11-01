from typing import Annotated

from fastapi import APIRouter, File, Query, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError

from app import crud, deps, schemas
from app.core import log, responses
from app.core.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
)
from app.utils import FilterUploadResult, filter_storage

router = APIRouter()


@router.post(
    "",
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
        filters = await crud.style_filters.create_many(db, results, user.id)
        return schemas.http.UploadStyleFiltersOut(
            filters=[filter.to_schema() for filter in filters]
        )
    except SQLAlchemyError as e:
        log.error(f"Failed to upload images: {e}. Deleting uploaded images")

        filter_storage.delete(img_ids=[img.img_id for img in results])

        raise InternalServerError()


@router.delete(
    "",
    summary="Delete multiple style filters",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.delete_style_filters,
)
async def delete_filters(
    db: deps.db_dep,
    user: deps.current_user_dep,
    query: Annotated[schemas.StyleFilterDeleteQuery, Query()],
) -> None:
    filters = await crud.style_filters.get_many(db, query.filter_ids)

    if len(filters) == 0:
        raise NotFoundError()

    is_owner = all(filter.author_id == user.id for filter in filters)
    if not is_owner:
        raise ForbiddenError()

    filter_storage.delete(
        [filter.img_id for filter in filters if filter.img_id is not None]
    )

    await crud.style_filters.delete_many(db, [filter.id for filter in filters])


# DELETE
# BAN
# GET authors
# SEARCH
