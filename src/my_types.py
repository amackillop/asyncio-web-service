"""
Types used project wide to catch runtime errors before they happen
"""

from dataclasses import dataclass, field
from typing import TypeVar, Callable, Any, List

import datetime as dt


FuncType = Callable[..., Any]
Func = TypeVar('Func', bound=FuncType)


@dataclass(frozen=True)
class Uploaded:
    """Represents uploaded urls"""
    pending: List[str] = field(default_factory=list)
    completed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)

@dataclass()
class Job:
    """Represents a submitted job"""
    uploaded: Uploaded
    job_id: str
    created: str = field(default_factory=lambda: dt.datetime.utcnow().isoformat())
    finished: str = ''
    status: str = 'Pending'
    