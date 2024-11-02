from dataclasses import dataclass

import cloudinary
import cloudinary.api
from cloudinary.uploader import upload_image
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile

from app.core import log, settings

from .enums import CloudinaryFolderPath


@dataclass
class FilterUploadResult:
    img_id: str
    base_img_url: str
    blur_img_url: str
    small_img_url: str


class FilterStorage:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB cap for each image

    SUPPORTED_FILE_TYPE = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/heic",
        "image/heif",
        "image/heics",
        "png",
        "jpeg",
        "jpg",
        "heic",
        "heif",
        "heics",
    ]

    def __init__(self) -> None:
        self.config = cloudinary.config(
            secure=True,
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_cloud_key,
            api_secret=settings.cloudinary_cloud_secret,
        )

    def upload(self, file: UploadFile) -> FilterUploadResult | None:
        try:
            img = upload_image(
                file.file, folder=CloudinaryFolderPath.STYLE_FILTER.value
            )

            img_id = img.public_id
            img_url = img.url

            if not isinstance(img_id, str):
                log.error(f"Failed to upload img: public_id {img_id}, url {img_url}")
                return None

            blur_img_url = self.get_blur_image(img_id)
            small_img_url = self.get_small_image(img_id)

            log.info("Image uploaded")
            return FilterUploadResult(img_id, img_url, blur_img_url, small_img_url)
        except Exception as e:
            log.error(f"Failed to upload image: {e}")
            return None

    def delete(self, img_ids: set[str]) -> None:
        log.info(img_ids)
        cloudinary.api.delete_resources(list(img_ids))

    def get_blur_image(self, img_public_id: str) -> str:
        img_url, _opts = cloudinary_url(
            img_public_id,
            transformation=[{"effect": "blur:1000"}, {"quality": "auto"}],
        )

        return img_url

    def get_small_image(self, img_public_id: str) -> str:
        img_url, _opts = cloudinary_url(
            img_public_id,
            transformation=[{"width": 400}, {"height": 280}, {"crop": "fill"}],
        )

        return img_url

    @staticmethod
    def to_mb(size: int) -> float:
        return size / (1024 * 1024)


filter_storage = FilterStorage()
