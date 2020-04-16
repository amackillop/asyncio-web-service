""""""
from typing import Iterable, TypeVar
from hypothesis import given
import hypothesis.strategies as st
from hypothesis import given
import hypothesis.provisional as stp

from .context import helpers as hf
from collections.abc import Iterator

from itertools import tee

T = TypeVar("T")


@given(stp.urls())
def test_is_valid_url_valid_example(url: str):
    assert hf.is_valid_url(url) == True


@given(st.text())
def test_is_valid_url_invalid_example(url: str):
    assert hf.is_valid_url(url) == False


@given(st.iterables(st.integers(), unique=True, min_size=1))
def test_tail_only_removes_first_item(iterable: Iterable[T]):
    # If iterable is an iterator then it will be consumed so we need a copy
    iterable1, iterable2 = tee(iterable)
    # Force to list for easy testing
    iterable1 = list(iterable1) # type: ignore
    new_iterable = list(hf.tail(iterable2))
    assert iterable1[0] not in new_iterable # type: ignore
    assert all(x in iterable1 for x in new_iterable)


@given(st.iterables(st.booleans()))
def test_partition(iterable: Iterable[T]):
    iterable1, iterable2 = tee(iterable)
    trues, falses = hf.partition(bool, iterable2)
    trues, falses = list(trues), list(falses)
    true_count, false_count = (0, 0)
    for elem in iterable1:
        if elem:
            true_count += 1
        else:
            false_count += 1
    assert len(trues) == true_count
    assert len(falses) == false_count
