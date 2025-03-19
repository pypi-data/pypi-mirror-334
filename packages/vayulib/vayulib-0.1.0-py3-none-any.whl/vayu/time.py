import datetime
import time

from dataclasses import dataclass
import datetime as dt
from typing import Union
from functools import wraps
from zoneinfo import ZoneInfo

from vayu.common import Interval, TZ


def epoch_time() -> dt.datetime:
    return from_timestamp(0)


def time_now(with_ms=False, local=True) -> dt.datetime:
    t = dt.datetime.now(tz=TZ if local else datetime.UTC)
    if not with_ms:
        t = t.replace(microsecond=0)

    return t


def min_time(date: dt.date, tz=None) -> dt.datetime:
    return dt.datetime.combine(date, dt.time.min, tzinfo=tz or dt.UTC)


def max_time(date: dt.date, tz=None) -> dt.datetime:
    return dt.datetime.combine(date, dt.time.max, tzinfo=tz or dt.UTC)


def ts_ms(t: datetime.datetime) -> int:
    return int(t.timestamp() * 1000)


def utc_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
) -> dt.datetime:
    return dt.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
        tzinfo=datetime.UTC,
    )


def local_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
    tz=TZ,
) -> datetime.datetime:
    t = datetime.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
    )
    return t.replace(tzinfo=tz)


def from_timestamp(ts: float, tz=TZ) -> dt.datetime:
    if ts > 1e12:
        # ts is in ms.
        ts = ts / 1000
    return dt.datetime.fromtimestamp(ts, tz=tz or dt.UTC)


def from_z_string(t: str) -> dt.datetime:
    return dt.datetime.fromisoformat(t.upper().replace("Z", "+00:00"))


@dataclass
class TimeWindow(Interval):
    start: Union[dt.datetime, dt.date, None] = None
    end: Union[dt.datetime, dt.date, None] = None

    @property
    def duration(self) -> dt.timedelta:
        return self.end - self.start

    @property
    def start_ms(self) -> int:
        return int(self.start.timestamp() * 1000)

    @property
    def end_ms(self) -> int:
        return int(self.end.timestamp() * 1000)

    @staticmethod
    def ahead(
        *,
        t: dt.datetime = None,
        duration: dt.timedelta = None,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ) -> "TimeWindow":
        if not duration:
            duration = dt.timedelta(
                days=days,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds,
                minutes=minutes,
                hours=hours,
                weeks=weeks,
            )
        else:
            assert days == seconds == milliseconds == milliseconds == minutes == hours == weeks == 0
        t = t or time_now()
        return TimeWindow(t, t + duration)

    @staticmethod
    def behind(
        *,
        t: dt.datetime = None,
        duration: dt.timedelta = None,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ) -> "TimeWindow":
        if not duration:
            duration = dt.timedelta(
                days=days,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds,
                minutes=minutes,
                hours=hours,
                weeks=weeks,
            )
        else:
            assert days == seconds == milliseconds == milliseconds == minutes == hours == weeks == 0

        t = t or time_now()
        return TimeWindow(t - duration, t)

    @staticmethod
    def around(
        *,
        t: dt.datetime = None,
        duration: dt.timedelta = None,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        if not duration:
            duration = dt.timedelta(
                days=days,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds,
                minutes=minutes,
                hours=hours,
                weeks=weeks,
            )
        else:
            assert days == seconds == milliseconds == milliseconds == minutes == hours == weeks == 0

        t = t or time_now()
        return TimeWindow(t - duration, t + duration)

    @staticmethod
    def from_date(year: int, month: int, day: int, tz=None) -> "TimeWindow":
        tz = tz or ZoneInfo("UTC")
        date = dt.date(year, month, day)
        return TimeWindow(start=min_time(date, tz=tz), end=max_time(date, tz=tz))

    @staticmethod
    def from_timestamp(start_ts: [int, float], end_ts: [int, float], tz=None) -> "TimeWindow":
        start = from_timestamp(start_ts, tz=tz)
        end = from_timestamp(end_ts, tz=tz)
        return TimeWindow(start, end)

    def __str__(self):
        if isinstance(self.start, dt.date):
            return f"[{self.start.isoformat()} - {self.end.isoformat()}]"
        return f"[{self.start.replace(microsecond=0).isoformat()} - {self.end.replace(microsecond=0).isoformat()}]"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.end, self.start))

    def _validate(self):
        if self.start == self.end is None:
            is_date = False
        else:
            # Note: we cannot do isinstance(t, dt.date) as it'd be True even if t was a datetime.
            is_date = not (isinstance(self.start, dt.datetime) or isinstance(self.end, dt.datetime))
        if self.start and self.end:
            assert type(self.start) is type(self.end), "Both start and end should be of same type"

        if self.start is None:
            self.start = epoch_time().date() if is_date else epoch_time()
        if self.end is None:
            self.end = time_now().date() if is_date else time_now()
        if not is_date and bool(self.start.tzinfo) != bool(self.end.tzinfo):
            raise ValueError("end and start should either be tz aware or unaware.")

        assert self.start <= self.end, "start time should be less than equal to end time"

    def __post_init__(self):
        self._validate()


def timeit(f):
    @wraps(f)
    def timed(*args, **kw):

        t = -time.time()
        result = f(*args, **kw)
        t += time.time()

        print(f"`{f.__name__}` took: {round(t, 3)}s")
        return result

    return timed


def to_human_readable_time(t: Union[dt.timedelta, float]):
    if isinstance(t, dt.timedelta):
        t = int(t.total_seconds())
    if t < 0:
        return "invalid-time"

    h, remainder = divmod(t, 3600)
    m, s = divmod(remainder, 60)

    parts = []
    if h > 0:
        parts.append(f"{h}h")
    if m > 0:
        parts.append(f"{m}m")
    if s > 0:
        parts.append(f"{s}s")

    return "".join(parts) if parts else "0s"
