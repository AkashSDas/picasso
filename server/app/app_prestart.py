import asyncio
import logging

from sqlalchemy import text
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed,
)

from app.core import log
from app.db.base import AsyncDbSession

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.WARN),
)
async def init() -> None:
    db = AsyncDbSession()

    try:
        await db.execute(text("SELECT 1"))
        return
    except Exception as e:
        log.error(e)
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
