from typing import Annotated
from uuid import UUID

import filetype
from fastapi import APIRouter, File, Query, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError

from app import crud, deps, schemas
from app.core import log, responses
from app.core.exceptions import (
    BadRequestError,
    EntityTooLargeError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnsupportedMediaTypeError,
)
from app.utils import FilterUploadResult, filter_storage

router = APIRouter()

MAX_REPORT_COUNT = 25


@router.post(
    "",
    summary="Upload filters",
    responses=responses.upload_style_filters,
    response_model=responses.upload_style_filters[status.HTTP_201_CREATED]["model"],
)
async def upload_filters(
    db: deps.db_dep,
    user: deps.current_user_dep,
    files: list[UploadFile] = File(..., description="Filters to upload", media_type=""),
) -> schemas.http.UploadStyleFiltersOut:
    log.info(f"Files {len(files)}: {files}")

    for file in files:
        file_info = filetype.guess(file.file)
        if file_info is None:
            raise UnsupportedMediaTypeError(
                message=f"File '{file.filename}' is not a valid image",
                reason="Invalid file type",
            )

        detected_content_type = file_info.extension.lower()

        if (
            file.content_type not in filter_storage.SUPPORTED_FILE_TYPE
            or detected_content_type not in filter_storage.SUPPORTED_FILE_TYPE
        ):
            raise UnsupportedMediaTypeError(
                message=f"File '{file.filename}' is not a valid image",
                reason="Invalid file type",
            )

        if file.size and file.size > filter_storage.MAX_FILE_SIZE:
            max_file_size_in_mb = filter_storage.to_mb(filter_storage.MAX_FILE_SIZE)
            input_file_size_in_mb = filter_storage.to_mb(file.size)

            raise EntityTooLargeError(
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
        assert len(results) == len(files), "Failed to upload all of the images"

        filters = await crud.style_filter.create_many(db, results, user.id)
        return schemas.http.UploadStyleFiltersOut(
            filters=[filter.to_schema() for filter in filters]
        )
    except (SQLAlchemyError, AssertionError) as e:
        log.error(f"Failed to upload images: {e}. Deleting uploaded images")

        filter_storage.delete(img_ids={img.img_id for img in results})

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
    filters = await crud.style_filter.get_many_by_ids(db, query.filter_ids)

    if len(filters) == 0:
        raise NotFoundError()

    is_owner = all(filter.author_id == user.id for filter in filters)
    if not is_owner:
        raise ForbiddenError()

    filter_storage.delete(
        {filter.img_id for filter in filters if filter.img_id is not None}
    )

    await crud.style_filter.delete_many(db, [filter.id for filter in filters])


@router.patch(
    "/{filter_id}/report",
    summary="Report a filter and if it's report count is above threshold then ban it",
    status_code=status.HTTP_200_OK,
    responses=responses.report_style_filter,
    response_model=responses.report_style_filter[status.HTTP_200_OK]["model"],
)
async def report_style_filter(
    db: deps.db_dep,
    filter_id: UUID,
    user: deps.current_user_dep,
    query: Annotated[schemas.ReportStyleFilterQuery, Query()],
) -> schemas.http.ReportStyleFilterOut:
    style_filter = await crud.style_filter.get_by_id(db, filter_id)

    if style_filter is None:
        raise NotFoundError()

    is_increment = query.type == "increment"
    has_reported = style_filter.id in user.reported_filter_ids

    if is_increment and has_reported:
        raise BadRequestError("Already reported")
    if not is_increment and not has_reported:
        raise BadRequestError("Not reported style filter")

    is_banned = style_filter.report_count > MAX_REPORT_COUNT

    await crud.style_filter.change_report_count(
        db,
        filter_id,
        is_increment=is_increment,
        is_banned=is_banned,
        commit=False,
    )

    new_reported_filter_ids = user.reported_filter_ids.copy()
    if is_increment:
        new_reported_filter_ids.append(style_filter.id)
    else:
        new_reported_filter_ids.remove(style_filter.id)

    await crud.user.update_banned_post_ids(
        db,
        user_id=user.id,
        reported_filter_ids=new_reported_filter_ids,
        commit=False,
    )

    await db.commit()

    return schemas.http.ReportStyleFilterOut(is_banned=is_banned)


@router.get(
    "",
    summary="Get style filters",
    status_code=status.HTTP_200_OK,
    responses=responses.get_style_filters,
    response_model=responses.get_style_filters[status.HTTP_200_OK]["model"],
)
async def get_style_filters(
    db: deps.db_dep,
    query: Annotated[schemas.GetStyleFiltersQuery, Query()],
) -> schemas.http.GetStyleFiltersOut:
    filters, total = await crud.style_filter.get_many(
        db,
        author_id=query.author_id,
        limit=query.limit,
        offset=query.offset,
    )

    return schemas.http.GetStyleFiltersOut(
        filters=[filter.to_schema() for filter in filters],
        total=total,
    )
