"""
Image uploading service implemented using asyncio/aiohttp
"""

import asyncio
import logging
import os
from typing import Union, Type

import uvloop  # type: ignore
from aiohttp import web

from resources import ROUTES

logging.basicConfig(level=logging.INFO)


async def start(app: web.Application, host: str, port: Union[str, int]) -> web.AppRunner:
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
    app["jobs"] = dict()
    loop = asyncio.get_event_loop()
    runner = loop.run_until_complete(start(app, host, port))
    print(f"======== Running on http://{host}:{port} ========\n(Press CTRL+C to quit)")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(runner.cleanup())


if __name__ == "__main__":
    # import tracemalloc

    # tracemalloc.start()
    uvloop.install()
    main()
