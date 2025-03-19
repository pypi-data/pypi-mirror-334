import asyncio
import datetime as dt
import os
from dataclasses import dataclass, replace
from logging import Logger
from typing import Dict, Callable, Tuple, List, Union, Type, Sequence, Iterable
import time
from functools import wraps
from operator import attrgetter
import random
from zoneinfo import ZoneInfo


MIN_FLOAT = float("-inf")
MAX_FLOAT = float("inf")
TZ = ZoneInfo(os.getenv("TZ")) if os.getenv("TZ") else dt.datetime.now().astimezone().tzinfo
TypeException = Type[Exception]

TaskType = Tuple[Callable, List, Dict]
Comparable = Union[None, dt.date, dt.datetime, int, float]


def camel_or_space_to_snake(s):
    s = s.replace(" ", "_")
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


@dataclass
class Interval:
    start: Comparable
    end: Comparable

    def intersects(self, other: "Interval") -> bool:
        return self.start <= other.end and other.start <= self.end

    def intersection(self, other: "Interval") -> "Interval":
        if not self.intersects(other):
            raise ValueError("No intersection possible")

        return replace(self, start=max(self.start, other.start), end=min(self.end, other.end))

    @classmethod
    def union(cls, intervals: Sequence["Interval"], allow_gaps: bool = False) -> "Interval":
        # TODO: Fix this: should have a signature same as intersection.
        if len(intervals) == 0:
            raise AssertionError("Length of intervals should at least be 1")
        if len(intervals) == 1:
            return intervals[0]

        intervals = sorted(intervals, key=attrgetter("start"))
        if not allow_gaps:
            for i in range(len(intervals) - 1):
                first = intervals[i]
                second = intervals[i + 1]
                if first.end < second.start:
                    raise ValueError(f"Gaps not supported in interval union")

        return cls(start=intervals[0].start, end=intervals[-1].end)

    @property
    def range(self) -> Comparable:
        return self.end - self.start

    def _validate(self):
        assert self.start < self.end, "start value should be less than equal to end"

    def __post_init__(self):
        self._validate()

    def __or__(self, other) -> "Interval":
        return self.__class__.union([self, other])

    def __and__(self, other) -> "Interval":
        return self.intersection(other)

    def __sub__(self, other: Comparable) -> "Interval":
        return self.__class__(start=self.start - other, end=self.end - other)

    def __add__(self, other: Comparable) -> "Interval":
        return self.__class__(start=self.start + other, end=self.end + other)

    def __contains__(self, item: Union[Comparable, "Interval"]):
        if isinstance(item, Interval):
            return item.start in self and item.end in self
        return self.start <= item <= self.end

    def __str__(self):
        return f"[{self.start} — {self.end}]"


class retry:  # noqa
    """Retry calling the decorated function using an exponential backoff. Asyncio compatible."""

    def __init__(
        self,
        exception_to_check: Union[TypeException, Tuple[TypeException]],
        tries: int = 4,
        delay: float = 1,
        backoff: float = 2,
        logger: Logger = None,
    ):
        """
        Args:
            exception_to_check: the exception to check. Maybe a tuple of exceptions to check.
            tries: number of times to try (not retry) before giving up
            delay: initial delay between retries in seconds
            backoff: backoff multiplier e.g. value of 2 will double the delay for each retry
            logger: logger to use. If None, print.
        """
        self._tries = tries
        self._delay = delay
        self._backoff = backoff
        self._ignore_exc_types = exception_to_check
        self._log_fn = logger.warning if logger else print

    def __call__(self, fn):
        is_async = asyncio.iscoroutinefunction(fn)
        if not is_async:

            @wraps(fn)
            def decorated(*a, **k):
                last_exception = None
                delay = self._delay
                for attempt in range(self._tries):
                    try:  # noqa
                        return fn(*a, **k)
                    except self._ignore_exc_types as e:
                        last_exception = e
                        msg = f"Error {e.__class__.__name__}: retrying {fn.__name__} - in {delay}s - attempt {attempt + 1}/{self._tries}"
                        self._log_fn(msg)
                    time.sleep(delay)
                    delay *= self._backoff
                if last_exception is not None:
                    raise last_exception

            return decorated

        else:

            @wraps(fn)
            async def decorated(*a, **k):
                last_exception = None
                delay = self._delay
                for attempt in range(self._tries):
                    try:  # noqa
                        return await fn(*a, **k)
                    except self._ignore_exc_types as e:
                        last_exception = e
                        msg = f"{str(e.__class__.__name__)}: retrying {fn.__name__} - in {delay}s - attempt {attempt + 1}/{self._tries}"
                        self._log_fn(msg)
                    await asyncio.sleep(delay)
                    delay *= self._backoff
                if last_exception is not None:
                    raise last_exception

            return decorated


JitterT = Union[float, int, dt.timedelta]


def add_jitter(n: JitterT, jitter_percentage: int = 20) -> JitterT:
    """Add jitter to seconds."""
    return n * (1 + random.randint(-jitter_percentage, jitter_percentage) / 100)


def group(iterable: Iterable, key: Callable) -> Dict:
    """Group elements of an iterable by a key function."""
    groups = {}
    for item in iterable:
        k = key(item)
        if k not in groups:
            groups[k] = []
        groups[k].append(item)
    return groups
