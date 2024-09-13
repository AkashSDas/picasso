import logging
import sys
from logging.handlers import RotatingFileHandler

from asgi_correlation_id import CorrelationIdFilter

from app.core import settings


def create_app_logger() -> logging.Logger:
    """
    Creates and configures an enhanced logger for the application.

    Returns:
        logging.Logger: A configured logger instance with console and file
        handlers, rotation, and correlation ID support.

    Example:
    ```python
    logger = create_app_logger()
    logger.info("Hello, world!")
    logger.error("Something went wrong!")
    logger.debug("This is a debug message.")
    ```
    """

    # Create a logger with application name and a formatter

    app_logger = logging.getLogger(settings.logger_name)
    app_logger.setLevel(settings.logger_level)

    # Prevent logs from propagating to the root logger
    app_logger.propagate = False

    formatter = logging.Formatter(
        fmt=settings.logger_format,
        datefmt=settings.logger_date_format,
    )

    # Stream handler for logging to the console (stdout)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.logger_level)
    console_handler.addFilter(
        CorrelationIdFilter(uuid_length=32, default_value="-"),
    )

    # Rotating file handler for logging to a file with log rotation

    file_handler = RotatingFileHandler(
        filename=settings.logger_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB per log file
        backupCount=3,  # Keep 3 backup files
    )
    file_handler.setFormatter(formatter)

    # Use INFO level or higher for file logs
    file_handler.setLevel(logging.INFO)

    file_handler.addFilter(
        CorrelationIdFilter(uuid_length=32, default_value="-"),
    )

    # Add a separate file handler for ERROR level logs

    error_file_handler = RotatingFileHandler(
        filename=settings.logger_error_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB per log file
        backupCount=3,  # Keep 3 backup files
    )
    error_file_handler.setFormatter(formatter)

    # Use INFO level or higher for file logs
    error_file_handler.setLevel(logging.ERROR)

    error_file_handler.addFilter(
        CorrelationIdFilter(uuid_length=32, default_value="-"),
    )

    # Attach handlers to the logger

    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)
    app_logger.addHandler(error_file_handler)

    # Intercept Uvicorn's log and use the same handlers (but not altering the
    # actual Uvicorn log configuration)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = app_logger.handlers  # Redirect Uvicorn logs
    uvicorn_logger.setLevel(settings.logger_level)  # Match log level

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = app_logger.handlers
    uvicorn_access_logger.setLevel(settings.logger_level)

    return app_logger


log = create_app_logger()
