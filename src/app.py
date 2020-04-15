"""
Image uploading service implemented using asyncio/aiohttp
"""

import asyncio
from asyncio import AbstractEventLoop
import os
from typing import Union, Type, Optional

import uvloop  # type: ignore
from aiohttp import web
import signal
from signal import Signals

from resources import ROUTES
import aiologger  # type: ignore

from redis_client import ReJson

logger = aiologger.Logger.with_default_handlers()


async def handle_exception(loop: AbstractEventLoop, context: dict):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    await logger.error(f"Caught exception: {msg}")
    await logger.info("Shutting down...")
    asyncio.create_task(shutdown(loop))


async def shutdown(loop: AbstractEventLoop, signal: Optional[Signals]=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        await logger.info(f"Received exit signal {signal.name}...")

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
    host = os.environ.get("HOST", "localhost")
    port = os.environ.get("PORT", 8000)
    app = web.Application()
    app.add_routes(ROUTES)
    app["db"] = ReJson(
        os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", 6379)
    )
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(loop, signal=s))
        )
    loop.set_exception_handler(handle_exception)
    print(
        f"======== Running on http://{host}:{port} ========\n" "(Press CTRL+C to quit)"
    )
    try:
        runner = loop.run_until_complete(start(app, host, port))
        loop.run_forever()
    finally:
        # runner.cleanup()
        loop.close()


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    # uvloop.install()
    main()
