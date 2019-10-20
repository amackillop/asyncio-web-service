
import imghdr
import base64
import collections
from io import BytesIO
from urllib.parse import urlparse
import itertools

from typing import TypeVar, Callable, Iterable, Iterator, Tuple

import aiohttp

T = TypeVar('T')

# HTTP stuff
def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
    except:
        return False
    return all([result.scheme in ['http', 'https'], result.netloc, result.path])


async def make_request(method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
    async with aiohttp.request(method, url, **kwargs) as resp:
        return resp


async def download_image(url: str) -> str:
    """Download and verify image from given URL."""
    async with aiohttp.request('get', url, raise_for_status=True) as resp:
        content = await resp.read()

    # Weak check that the page content is actually an image. 
    if imghdr.what(BytesIO(content)) is None:
        msg = f'Not a valid image at {url}.'
        raise IOError(msg)
    return base64.b64encode(content).decode('ascii')


# Functional Programming FTW
def tail(iterable: Iterable) -> Iterable:
    "Return an iterator over the last n items"
    deq = collections.deque(iterable)
    deq.popleft()
    return deq

def partition(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[Iterator[T], Iterator[T]]:
    'Use a predicate to partition entries into false entries and true entries'
    t1, t2 = itertools.tee(iterable)
    return filter(predicate, t1), itertools.filterfalse(predicate, t2)
