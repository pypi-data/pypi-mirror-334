import asyncio
from datetime import timedelta
from numbers import Number
from signal import SIGTERM, SIGINT
from typing import Union, Coroutine, Optional, List, Dict, Any

import aiohttp
from aiohttp import TCPConnector


async def get_first_and_cancel_rest(*tasks: Union[asyncio.Task, Coroutine]) -> asyncio.Task:
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()

    return done.pop()


async def sleep_until_signal(duration: Union[timedelta, Number], signal: asyncio.Event) -> bool:
    """Sleep until duration unless signal fires. Returns True if signal fired first."""
    if isinstance(duration, (int, float)):
        duration = timedelta(seconds=duration)

    sleep_task = asyncio.create_task(asyncio.sleep(duration.total_seconds()))
    signal_task = asyncio.create_task(signal.wait())
    done = await get_first_and_cancel_rest(sleep_task, signal_task)
    return done is signal_task


def attach_shutdown_signals(shutdown: asyncio.Event, signals: Optional[List] = None):
    signals = signals or [SIGINT, SIGTERM]
    loop = asyncio.get_running_loop()

    def set_signal():
        shutdown.set()

    for signal in signals:
        loop.add_signal_handler(signal, set_signal)


async def grab_all_urls(key_url_map: Dict[Any, str], concurrency=100, timeout=15, print_progress=True) -> Dict[Any, Any]:
    results = {}
    tasks = []
    semaphore = asyncio.Semaphore(concurrency)

    async def fetch_url(session, url, key, results: Dict[Any, Any], timeout):
        async with semaphore:
            try:
                async with session.get(url, timeout=timeout) as response:
                    results[key] = (response.status, await response.read())
            except Exception as e:
                results[key] = None, str(e)

    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        for key, url in key_url_map.items():
            task = fetch_url(session, url, key, results, timeout)
            tasks.append(task)

        for i, task in enumerate(asyncio.as_completed(tasks)):
            await task
            if print_progress:
                print(f'Progress: {i+1}/{len(tasks)}', end="\r")

    return results
