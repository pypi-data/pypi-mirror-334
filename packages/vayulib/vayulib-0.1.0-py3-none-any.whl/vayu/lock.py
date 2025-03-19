import asyncio
import time
import uuid
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Optional

try:
    from redis.asyncio.lock import Lock
    from redis.asyncio import Redis
except ImportError:
    Lock = None
    Redis = None

from vayu.aio import sleep_until_signal
from vayu.common import add_jitter


def _validate_import():
    if Lock is None or Redis is None:
        raise ImportError("redis.asyncio.lock and redis.asyncio are not available.")


class LongLivedLock(Lock):
    """A long-lived distributed lock that extends its expiration time periodically until released."""
    def __init__(self, shutdown: Optional[asyncio.Event] = None, **kwargs):
        super(LongLivedLock, self).__init__(**kwargs)
        self._shutdown = shutdown

    async def acquire(self, **kwargs):
        if not self._shutdown:
            self._shutdown = asyncio.Event()

        result = await super(LongLivedLock, self).acquire(**kwargs)
        asyncio.create_task(self._extend_lock_periodically())
        return result

    async def _extend_lock_periodically(self):
        first_loop = True
        while not self._shutdown.is_set():
            if self.local.token is None:
                return
            if first_loop:
                first_loop = False
            else:
                await self.extend(additional_time=self.timeout, replace_ttl=True)
            sleep_for = self.timeout / 4
            # Add jitter upto 20% of sleep_for.
            sleep_for = add_jitter(sleep_for, 20)
            await sleep_until_signal(duration=timedelta(seconds=sleep_for), signal=self._shutdown)

    @staticmethod
    def make_lock(
        redis: "Redis",
        name,
        timeout: timedelta = None,
        sleep: timedelta = None,
        blocking_timeout: timedelta = None,
        shutdown: Optional[asyncio.Event] = None,
    ) -> "LongLivedLock":
        return LongLivedLock(
            # TODO: See if we can get away with using a single redis connection.
            redis=redis,
            name=f"lock.{name}",
            timeout=timeout.total_seconds() if timeout else 60,
            sleep=sleep.total_seconds() if sleep else 5,
            blocking_timeout=blocking_timeout.total_seconds() if blocking_timeout else None,
            shutdown=shutdown,
        )


class RedisSemaphore:
    def __init__(self, redis_client: Redis, key: str, limit: int, ttl: timedelta = None, retry_every: timedelta = None, keep_renewing: bool = False):
        """A distributed semaphore using redis sorted sets.

        Caveats:

        Args:
            redis_client:
            key: Key to use for the semaphore.
            limit: Maximum number of concurrent users.
            ttl: Time to live for each user's lock.
            retry_every:
            keep_renewing:
        """
        self._client = redis_client
        self._key = key
        self._limit = limit
        self._ttl = ttl or timedelta(seconds=60)
        self._retry_every = retry_every or timedelta(seconds=5)
        self._keep_renewing = keep_renewing

        # Lua script to add to sorted set if it is not full.
        lua_script = """
        local key = KEYS[1]
        local member = ARGV[1]
        local score = ARGV[2]
        local min_score = ARGV[3]
        local n = tonumber(ARGV[4])
        redis.call('ZREMRANGEBYSCORE', key, '-inf', min_score)
        if redis.call('ZCARD', key) < n then
            return redis.call('ZADD', key, score, member)
        else
            return nil
        end
        """

        self._lua_script = self._client.register_script(lua_script)

    async def _add_to_sorted_set(self, member: str, score: int, min_score: int):
        result = await self._lua_script(keys=[self._key], args=[member, str(score), str(min_score), self._limit])
        return result is not None

    async def acquire(self, identifier: str, shutdown: Optional[asyncio.Event] = None):
        while True:
            score = round(time.time())
            min_score = score - self._ttl.total_seconds()
            if await self._add_to_sorted_set(member=identifier, score=int(score), min_score=int(min_score)):
                return True
            # Retry after some time with some jitter.
            if await sleep_until_signal(duration=add_jitter(self._retry_every), signal=shutdown or asyncio.Event()):
                # Shutdown signal received.
                return False

    async def release(self, identifier: str):
        await self._client.zrem(self._key, identifier)

    @asynccontextmanager
    async def lock(self, identifier: str = None, shutdown: Optional[asyncio.Event] = None):
        identifier = identifier or uuid.uuid4().bytes
        acquired = False
        sig_renew = asyncio.Event()
        task_renew = None

        try:
            acquired = await self.acquire(identifier, shutdown=shutdown)
            if acquired and self._keep_renewing:
                task_renew = asyncio.create_task(self._renew_periodically(identifier, shutdown=sig_renew))
            yield
        finally:
            if acquired:
                await self.release(identifier)
            if task_renew:
                sig_renew.set()
                await task_renew

    async def _renew_periodically(self, identifier: str, shutdown: asyncio.Event):
        while not shutdown.is_set():
            # Renew lock every quarter of ttl only if it is still in the set.
            await self._client.zadd(self._key, {identifier: int(round(time.time()))}, xx=True)
            await sleep_until_signal(duration=add_jitter(self._ttl/4), signal=shutdown)
