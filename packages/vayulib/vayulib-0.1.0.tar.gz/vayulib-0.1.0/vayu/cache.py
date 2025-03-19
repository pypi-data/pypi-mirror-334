import json
import os
from abc import ABC, abstractmethod
from datetime import timedelta
from functools import wraps
from hashlib import sha256
from pathlib import Path
from time import time
from typing import Callable, Any, Union, Dict, Tuple, Optional
import pickle

from vayu.log import L
from vayu.time import time_now, from_timestamp


class _MethodDecoratorAdaptor(object):
    def __init__(self, decorator, func):
        self.decorator = decorator
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))


def auto_adapt_to_methods(decorator):
    """Allows you to use the same decorator on methods and functions,
    hiding the self argument from the decorator."""

    def adapt(func):
        return _MethodDecoratorAdaptor(decorator, func)

    return adapt


class Serializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, bts: bytes) -> Any:
        pass


class NoOpSerializer(Serializer):
    def serialize(self, obj: Any) -> bytes:
        return obj

    def deserialize(self, bts: bytes) -> Any:
        return bts


class Pickler(Serializer):
    def serialize(self, obj: Any) -> bytes:
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    def deserialize(self, bts: bytes) -> Any:
        return pickle.loads(bts)


class Jsoner(Serializer):
    def serialize(self, obj: Any) -> bytes:
        return json.dumps(obj).encode()

    def deserialize(self, bts: bytes) -> Any:
        return json.loads(bts)


class Cache(ABC):
    def __init__(self, serializer: Serializer):
        self._serializer = serializer

    def cached(
        self,
        ttl: Union[timedelta, float] = None,
        prefix: str = None,
        key: Union[str, Callable] = None,
        serializer: Serializer = None,
        log: bool = True,
    ):
        """Used as decorator to cache function calls.

        Args:
            ttl: cache expiry ttl
            prefix: If set, gets prepended to the rest of the cache key, otherwise uses function,
                        class, and module name to create prefix.
            key:
               - None: Use SHA256 digest of *args & **kwargs to construct cache key
               - str: Use the specified string and ignore function arguments
               - Callable: Calls it with *args * **kwargs which returns a str key.
            serializer: If not specified, default pickler serializer is used
            log: If True, logs reports such as cache hit, miss etc.

        """
        serializer = serializer or self._serializer
        ttl = ttl or timedelta(days=365 * 10)
        if not isinstance(ttl, timedelta):
            ttl = timedelta(seconds=ttl)
        if ttl.total_seconds() <= 0:
            raise ValueError("ttl must be positive")

        @auto_adapt_to_methods
        def decorator(func):
            f_name = func.__name__

            @wraps(func)
            def inner(*args, **kwargs):
                t = time()
                k = self._key(func, prefix=prefix, key=key, args=args, kwargs=kwargs)
                t_del = time() - t
                if 0.001 < t_del and log:
                    L.warn(f"Key construction for cached fn `{f_name}` took too long: {t_del:.6f}s")

                got = self._read(k)
                if got is not None:
                    return serializer.deserialize(got)
                t = time()
                result = func(*args, **kwargs)
                t_del = time() - t
                if log:
                    L.info(f"@cached({f_name}) - CACHE MISS | took: {t_del:.6}s")
                self._write(k, serializer.serialize(result), ttl)
                return result

            @wraps(func)
            def evict(*args, **kwargs):
                k = self._key(func, prefix=prefix, key=key, args=args, kwargs=kwargs)
                self._delete(k)

            inner.evict = evict

            return inner

        return decorator

    def read(self, key: str) -> Any:
        got = self._read(key)
        return None if got is None else self._serializer.deserialize(got)

    def write(self, key: str, value: Any, ttl: timedelta):
        return self._write(key, self._serializer.serialize(value), ttl)

    @abstractmethod
    def _read(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _write(self, key: str, value: Any, ttl: timedelta):
        raise NotImplementedError

    @abstractmethod
    def _delete(self, key: str):
        raise NotImplementedError

    @staticmethod
    def _key(
        fn: Callable,
        prefix: str = None,
        key: Union[str, Callable] = None,
        args: Tuple = None,
        kwargs: Dict = None,
    ) -> str:
        is_method = hasattr(fn, "__self__")

        if isinstance(key, str):
            return key

        parts = []
        if prefix:
            parts.append(prefix)
        else:
            parts.append(fn.__module__)
            parts.append(fn.__qualname__)
        parts = [".".join(parts)]
        if callable(key):
            parts.append(key(*args, **kwargs))
        else:
            arg_key = ",".join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])
            parts.append(sha256(arg_key.encode()).hexdigest())
        return ":".join(parts)


class InMemCache(Cache):
    def __init__(self, serializer: Serializer = None):
        super().__init__(serializer or NoOpSerializer())
        self._d = dict()

    def _write(self, key: str, value: bytes, ttl: timedelta):
        self._d[key] = (value, time_now(with_ms=True) + ttl)

    def _read(self, key: str) -> Optional[bytes]:
        got = self._d.get(key)
        if got is None:
            return None
        value, expiry_time = got
        if expiry_time < time_now(with_ms=True):
            self._delete(key)
            return None
        return value

    def _delete(self, key: str):
        self._d.pop(key, None)


class FileCache(Cache):
    def __init__(self, path: str, serializer: Serializer = None):
        super().__init__(serializer or Pickler())
        self._path = Path(path)
        self._ttl_bytes_length = 8

    def _write(self, key: str, value: bytes, ttl: timedelta):
        expiry_time = time_now(with_ms=True) + ttl
        ttl_bytes = int(expiry_time.timestamp() * 1e6).to_bytes(
            length=self._ttl_bytes_length, byteorder="big"
        )
        bts = ttl_bytes + value
        with open(self._path / key, "wb") as f:
            f.write(bts)

    def _read(self, key: str) -> Optional[bytes]:
        try:
            with open(self._path / key, "rb") as f:
                ttl_bytes = f.read(self._ttl_bytes_length)
                ttl = from_timestamp(int.from_bytes(ttl_bytes, "big") / 1e6)
                if ttl < time_now(with_ms=True):
                    bts = None
                else:
                    bts = f.read()
        except FileNotFoundError:
            return None

        if bts is None:
            self._delete(key)
        return bts

    def _delete(self, key: str):
        os.remove(self._path / key)


# file_cache = FileCache(Config.CACHE_DIR, serializer=Pickler())
# file_cached = file_cache.cached
# in_mem_cache = InMemCache(serializer=NoOpSerializer())
# in_mem_cached = in_mem_cache.cached
