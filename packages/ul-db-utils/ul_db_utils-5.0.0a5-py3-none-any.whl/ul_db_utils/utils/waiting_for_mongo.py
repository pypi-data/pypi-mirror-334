import logging
import time

from pymongo import MongoClient

logger = logging.getLogger(__name__)


def waiting_for_mongo(uri: str, *, retry_max_count: int = 100, retry_delay_s: float = 0.4) -> bool:
    for i in range(0, retry_max_count):
        try:
            client = MongoClient(uri)
            logger.info("MongoDB is available")
            client.close()
            return True
        except Exception:  # noqa: B902
            logger.warning(f'{i + 1:0>{len(str(retry_max_count))}}/{retry_max_count} retry connect to MongoDB. sleep delay is {retry_delay_s} seconds')
            time.sleep(retry_delay_s)
            continue
    logger.error('MongoDB is NOT available')
    return False
