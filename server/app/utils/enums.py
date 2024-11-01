from enum import Enum


class HttpHeader(Enum):
    """Custom HTTP headers used in the application"""

    REQUEST_ID = "X-Request-ID"
    PROCESS_TIME = "X-Process-Time"


class CloudinaryFolderPath(Enum):
    """Assets folder paths in Cloudinary"""

    STYLE_FILTER = "picasso/style-filters"
