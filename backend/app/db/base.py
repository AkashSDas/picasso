from typing import Any

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, InstanceState
from sqlalchemy.orm.attributes import Event, InstrumentedAttribute
from sqlalchemy.util.langhelpers import symbol

from app.core import settings
from app.core.exceptions import NonUpdateableColumnError

# Create an asynchronous engine with connection pooling
engine = create_async_engine(
    str(settings.db_sqlalchemy_url),
    echo=settings.debug,  # Enable SQL query logging if in debug mode
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Additional connections allowed above pool_size
    # Wait 30 seconds for a connection before throwing an error
    pool_timeout=30,
    # Recycle connections every 30 minutes to prevent stale connections
    pool_recycle=1800,
    pool_pre_ping=True,  # Ping the database to check if the connection is alive
)

# Create an async session factory using the engine
AsyncDbSession = async_sessionmaker(
    bind=engine,
    autocommit=False,  # Manually commit transactions
    autoflush=False,  # Manually flush changes to the database
    expire_on_commit=False,  # Keep objects in memory after commit
)


class BaseDbModel(AsyncAttrs, DeclarativeBase):
    pass


def make_column_unupdateable(column: InstrumentedAttribute):
    @event.listens_for(column, "set")
    def unupdateable_column_set_listener(
        _target: InstanceState,
        value: Any,
        old_value: Any,
        _initiator: Event,
    ) -> None:
        if (
            old_value != symbol("NEVER_SET")
            and old_value != symbol("NO_VALUE")
            and old_value != value
        ):
            raise NonUpdateableColumnError(
                column.class_.__name__, column.name, old_value, value
            )
