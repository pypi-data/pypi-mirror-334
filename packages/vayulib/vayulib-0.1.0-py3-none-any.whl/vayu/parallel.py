import random
import time
import threading
from abc import abstractmethod, ABC
from enum import Enum
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, ProcessPoolExecutor
from typing import Dict, Hashable, Callable, Union

from vayu.log import L


class SafeCounter(ABC):
    @abstractmethod
    def increment(self, key):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @staticmethod
    def make(executor_cls: type) -> "SafeCounter":
        if executor_cls == ThreadPoolExecutor:
            return ThreadSafeCounter()
        elif executor_cls == ProcessPoolExecutor:
            return ProcessSafeCounter()
        else:
            raise ValueError(f"Invalid executor type {executor_cls}")


class ThreadSafeCounter(SafeCounter):
    def __init__(self):
        self.lock = threading.Lock()
        self.d = {}

    def increment(self, key):
        with self.lock:
            self.d[key] = self.d.get(key, 0) + 1

    def get(self, key):
        with self.lock:
            return self.d.get(key, 0)

    def get_all(self):
        with self.lock:
            return self.d.copy()


class ProcessSafeCounter(SafeCounter):
    def __init__(self):
        manager = Manager()
        self.d = manager.dict()

    def increment(self, key):
        try:
            self.d[key] = self.d.get(key, 0) + 1
        except Exception:
            L.warn("Exception in ProcessSafeCounter.increment", exc_info=True)

    def get(self, key):
        return self.d.get(key, 0)

    def get_all(self):
        return self.d.copy()


class SafeDict(ABC):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def pop(self, key):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @staticmethod
    def make(executor_cls: type) -> "SafeDict":
        if executor_cls == ThreadPoolExecutor:
            return ThreadSafeDict()
        elif executor_cls == ProcessPoolExecutor:
            return ProcessSafeDict()
        else:
            raise ValueError(f"Invalid executor type {executor_cls}")


class ThreadSafeDict(SafeDict):
    def __init__(self):
        self.lock = threading.Lock()
        self.d = {}

    def set(self, key, value):
        with self.lock:
            self.d[key] = value

    def get(self, key):
        with self.lock:
            return self.d.get(key)

    def pop(self, key):
        with self.lock:
            return self.d.pop(key)

    def get_all(self):
        with self.lock:
            return self.d.copy()


class ProcessSafeDict(SafeDict):
    def __init__(self):
        manager = Manager()
        self.d = manager.dict()

    def set(self, key, value):
        self.d[key] = value

    def get(self, key):
        return self.d.get(key)

    def pop(self, key):
        return self.d.pop(key)

    def get_all(self):
        return self.d.copy()


class ParallelRunner:
    """Simplified wrapper over ThreadPoolExecutor / ProcessPoolExecutor."""

    class State(Enum):
        INIT = 1
        RUNNING = 2
        DONE = 3

    def __init__(
        self,
        n_workers: int = None,
        executor_cls: type = None,
        initializer: Callable = None,
        init_args: tuple = None,
        return_when=ALL_COMPLETED,
        print_progress_every=5,
        report_exceptions=True,
    ):
        if executor_cls not in (ThreadPoolExecutor, ProcessPoolExecutor):
            raise ValueError(f"Invalid executor type {executor_cls}")

        self._n_workers = n_workers
        self._return_when = return_when
        self._tasks = dict()
        self._counter = SafeCounter.make(executor_cls)
        self._executor_cls = executor_cls if executor_cls else ThreadPoolExecutor
        self._executor = None
        self._initializer = initializer
        self._init_args = init_args or ()
        self._print_progress_every = print_progress_every
        self._state = ParallelRunner.State.INIT
        self._completion_signal: threading.Event = threading.Event()
        self._n_tasks = 0
        self._report_exceptions = report_exceptions

    def add(self, key: Hashable, func: Callable, *args, **kwargs):
        if self._state != ParallelRunner.State.INIT:
            raise RuntimeError("Cannot add tasks after calling run()")
        self._tasks[key] = (func, args, kwargs)
        self._n_tasks += 1

    def run(self) -> Dict[Hashable, object]:
        if self._state != ParallelRunner.State.INIT:
            raise RuntimeError("Cannot call run() more than once")
        self._state = ParallelRunner.State.RUNNING

        progress_thread = threading.Thread(target=self._print_progress)
        progress_thread.start()

        futures = dict()
        with self._executor_cls(
            max_workers=self._n_workers, initializer=self._initializer, initargs=self._init_args
        ) as ex:
            self._executor = ex
            for _ in range(len(self._tasks)):
                key, (func, args, kwargs) = self._tasks.popitem()
                futures[key] = ex.submit(
                    self._run, self._counter, key, self._report_exceptions, func, *args, **kwargs
                )
            try:
                wait(list(futures.values()), return_when=self._return_when)
                print("Values fetched")
            except KeyboardInterrupt:
                print("Shutting down...")
                self.shutdown()
                raise
            finally:
                self._state = ParallelRunner.State.DONE
                self._completion_signal.set()
        return {key: future.result() for key, future in futures.items()}

    def _print_progress(self):
        t = time.time()
        while self._completion_signal.wait(self._print_progress_every) is False:
            counters = self._counter.get_all()
            n_successes = counters.get("success", 0)
            n_failures = counters.get("failure", 0)
            completions = n_successes + n_failures
            perc = completions / self._n_tasks * 100
            time_taken = time.time() - t
            print(
                f"Success: {n_successes}, Failure: {n_failures}, "
                f"Completion: [{completions}/{self._n_tasks}] {perc:.2f}% "
                f"{time_taken:.1f}s ({(completions/time_taken):.2f} exec/s)",
                end="\r",
            )

    def shutdown(self, wait=True, *, cancel_futures=True):
        self._executor.shutdown(wait=wait, cancel_futures=cancel_futures)

    @staticmethod
    def _run(counter: SafeCounter, key, report_exception, f, *args, **kwargs):
        try:
            result = f(*args, **kwargs)
            counter.increment("success")
        except Exception as e:
            result = e
            counter.increment("failure")
            if report_exception:
                L.error(f"Exception in task for key {key}", exc_info=True)

        return result


if __name__ == "__main__":
    # Test ParallelRunner with ThreadPoolExecutor
    def f(x):
        time.sleep(random.randint(__ctx__["a"], __ctx__["b"]) / 10)
        return x**2

    def init():
        global __ctx__
        __ctx__ = {"a": 0, "b": 3}

    runner = ParallelRunner(
        n_workers=5,
        executor_cls=ThreadPoolExecutor,
        print_progress_every=1,
        initializer=init,
    )
    for i in range(300):
        runner.add(i, f, i)
    result = runner.run()
    print(result)
