"""
This is a script that run before the application is started. This will take care of
connecting to the database and retry several times before crashing if it's failing
to connect to the database
"""

import asyncio
import logging

from sqlalchemy import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core import log
from app.db.base import AsyncDbSession

MAX_RETRIES = 60 * 5
WAIT_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.WARN),
)
async def init() -> None:
    db = AsyncDbSession()

    try:
        await db.execute(text("SELECT 1"))
        return
    except Exception as e:
        log.critical(f"Failed to connect to the database: {e}")
        raise e
    finally:
        await db.close()


async def main() -> int:
    log.info("Testing database connection")
    await init()
    log.info("Established database connection")
    return 0


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
