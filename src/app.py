"""
Image uploading service implemented using asyncio/aiohttp
"""

import asyncio
from asyncio import AbstractEventLoop
import os
from typing import Union, Optional
import signal
from signal import Signals  # pylint: disable=no-name-in-module

import uvloop  # type: ignore
from aiohttp import web
import aiologger  # type: ignore

from resources import ROUTES
from redis_client import ReJson

logger = aiologger.Logger.with_default_handlers()


async def handle_exception(loop: AbstractEventLoop, context: dict):
    """"""
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    await logger.error(f"Caught exception: {msg}")
    await logger.info("Shutting down...")
    asyncio.create_task(shutdown(loop))


async def shutdown(loop: AbstractEventLoop, sig: Optional[Signals] = None):
    """Cleanup tasks tied to the service's shutdown."""
    if sig:
        await logger.info(f"Received exit signal {sig.name}...")

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    for task in tasks:
        task.cancel()

    await logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def start(
    app: web.Application, host: str, port: Union[str, int]
) -> web.AppRunner:
    """Start the server"""
    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, host, int(port))
    await server.start()
    return runner


def main() -> None:
    """Entrypoint"""
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    app = web.Application()
    app.add_routes(ROUTES)
    app["db"] = ReJson(os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(loop, sig=s))
        )
    loop.set_exception_handler(handle_exception)
    print(
        f"======== Running on http://{host}:{port} ========\n" "(Press CTRL+C to quit)"
    )
    try:
        runner = loop.run_until_complete(start(app, host, port))
        loop.run_forever()
    finally:
        loop.run_until_complete(runner.cleanup())
        loop.close()


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    # uvloop.install()
    main()
