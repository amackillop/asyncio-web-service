from hypothesis import given
import hypothesis.strategies as st

import helpers as hf

@given(st.lists(st.integers(), unique=True, min_size=1))
def test_tail_only_removes_first_item(iterable):
    new_iterable = hf.tail(iterable)
    assert iterable[0] not in new_iterable
    assert all([x in new_iterable for x in iterable[1:]])
    
