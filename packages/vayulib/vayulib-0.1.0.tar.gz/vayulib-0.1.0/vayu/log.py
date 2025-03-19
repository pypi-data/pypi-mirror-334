import logging
import os
import sys
import datetime
from pytz import timezone

LOGGING_TZ = timezone(os.getenv("TZ", "UTC"))


def _format_time(self, record, _=None):
    return (
        datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        .replace(microsecond=0)
        .astimezone(LOGGING_TZ)
        .isoformat(sep="T")
    )


formatter = logging.Formatter("[%(asctime)s] %(levelname)s> %(message)s")
logging.Formatter.formatTime = _format_time

_asyncio_logger = logging.getLogger("asyncio")
L = logging.getLogger()

_asyncio_logger.setLevel(logging.WARNING)
L.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

_handler = logging.StreamHandler(sys.stdout)
_handler.setLevel(logging.INFO)
_handler.setFormatter(formatter)
L.addHandler(_handler)
_asyncio_logger.addHandler(_handler)

L.i = L.info
L.d = L.debug
L.e = L.error
L.w = L.warning
L.c = L.critical

__all___ = [L]
