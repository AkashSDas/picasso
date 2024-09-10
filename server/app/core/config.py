from typing import Literal, Self
from urllib.parse import quote_plus

from pydantic import AnyHttpUrl, Json, ValidationInfo, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    This class defines the database configuration settings.
    It includes fields like username, password, host, port, and name.
    """

    db_username: str  # Database username
    db_password: str  # Database password
    db_host: str  # Database host (IP or domain)
    db_port: int = 5432  # Default database port (PostgreSQL's default port)
    db_name: str  # Database name

    # SQLAlchemy connection URL, either passed directly or constructed
    db_sqlalchemy_url: str | None = None

    @field_validator("db_sqlalchemy_url", mode="before")
    def create_sqlalchemy_url(cls, v: str | None, field_info: ValidationInfo) -> str:
        """
        Automatically generate the SQLAlchemy database URL if not provided.
        If the URL is already set, return it unchanged.
        Otherwise, construct it using the provided database credentials.
        """
        if isinstance(v, str) and v:
            return v

        # Extract necessary fields from the settings object (data context)
        username = field_info.data.get("db_username")
        password = field_info.data.get("db_password")
        host = field_info.data.get("db_host")
        port = field_info.data.get("db_port", 5432)
        name = field_info.data.get("db_name")

        # Safely encode the password for URL
        parsed_pwd = quote_plus(str(password))

        # Return the constructed asyncpg connection URL
        return f"postgresql+asyncpg://{username}:{parsed_pwd}@{host}:{port}/{name}"


class LoggerSettings(BaseSettings):
    """
    This class defines the logger configuration settings, allowing customization
    of logger name, level, format, and date format.
    """

    # Logger name, which identifies the source of the log entry
    logger_name: str = "Picasso"

    # Log level, defaults to INFO but can be changed to control verbosity
    logger_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Log message format, which includes time, level, process/thread info, and more
    logger_format: str = (
        "[%(asctime)s] [%(levelname)s] [%(name)s] "
        "[PID %(process)d] [TID %(thread)d] [X-ID %(correlation_id)s] "
        "[%(filename)s.%(lineno)s -> %(funcName)s()] %(message)s"
    )

    # Date format for timestamps in log messages
    logger_date_format: str = "%d-%m-%YT%H:%M:%SZ"

    logger_file_path: str = "./logs/app.log"
    logger_error_file_path: str = "./logs/error.log"


class Settings(DatabaseSettings, LoggerSettings):
    """
    This is the main settings class that aggregates database, logger, and other settings,
    and includes application-specific settings like title, version, CORS origins, and debug mode.
    """

    # Configuration for Pydantic settings
    model_config = SettingsConfigDict(
        case_sensitive=False,  # Settings are case-insensitive by default
        env_file=".env",  # Load settings from the .env file
        extra="ignore",  # Ignore unknown environment variables
    )

    # Application-specific settings
    app_title: str = "Picasso"  # Title of the application
    app_version: str = "0.1.0"  # Version of the application

    # CORS origins, expected to be a JSON-formatted list of URLs
    cors_origins: Json[list[AnyHttpUrl]] = "[]"  # type: ignore[assignment]

    # Trusted hosts, expected to be a JSON-formatted list of URLs
    trusted_hosts: Json[list[AnyHttpUrl]] = '["http://localhost:3000"]'  # type: ignore[assignment]

    # Debug mode, set this to True for development environments
    debug: bool = False

    @model_validator(mode="after")
    def configure_debug(self) -> Self:
        """
        After the model is initialized, check if debug mode is enabled.
        If so, set the logger level to DEBUG for more detailed logging.
        """
        if self.debug:
            self.logger_level = "DEBUG"
        return self


# Instantiate the settings object, loading from environment variables and defaults.
settings = Settings()  # type: ignore[call-arg]
