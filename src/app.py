"""
Image uploading service implemented using asyncio/aiohttp
"""

import asyncio
import logging
import os
from typing import Union, Type

import uvloop  # type: ignore
from aiohttp import web
import signal

from resources import ROUTES

logging.basicConfig(level=logging.INFO)


async def start(app: web.Application, host: str, port: Union[str, int]) -> web.AppRunner:
    """Start the server"""
    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, host, int(port))
    await server.start()
    return runner

async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    logging.info(f"Received exit signal {signal.name}...")
    logging.info("Closing database connections")
    logging.info("Nacking outstanding messages")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks)
    logging.info(f"Flushing metrics")
    loop.stop()


def main() -> None:
    """Entrypoint"""
    host = os.environ.get("HOST", "localhost")
    port = os.environ.get("PORT", 8000)
    app = web.Application()
    app.add_routes(ROUTES)
    app["jobs"] = dict()
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    runner = loop.run_until_complete(start(app, host, port))
    print(f"======== Running on http://{host}:{port} ========\n(Press CTRL+C to quit)")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(runner.cleanup())
    finally:
        loop.close()


if __name__ == "__main__":
    # import tracemalloc

    # tracemalloc.start()
    uvloop.install()
    main()
