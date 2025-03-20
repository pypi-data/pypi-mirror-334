import math
from typing import Generic, Iterator, TypeVar, Union, cast

from .types import Point, Step

P = TypeVar("P", bound=Point)
S = TypeVar("S", bound=Step)


class Interval(Generic[P, S]):
    __slots__ = ("start", "stop", "step")
    start: P
    stop: P
    step: S

    def __init__(
        self,
        start: P,
        stop: P,
        /,
        step: S = 1,  # type: ignore
    ):
        self.start = start
        self.stop = stop
        self.step = step

    def to_tuple(self):
        return (self.start, self.stop, self.step)

    def __repr__(self):
        return repr(self.to_tuple()[:-1])

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other: object):
        if not isinstance(other, Interval):
            return False
        return self.to_tuple() == other.to_tuple()

    ## properties

    def __bool__(self):
        return self.start < self.stop

    def __len__(self) -> int:
        if not self:
            return 0
        return math.ceil((self.stop - self.start) / self.step)

    ## access / iteration

    def __getitem__(self, index: int) -> P:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("index out of range")
        return self.start + (self.step * index)

    def __iter__(self) -> Iterator[P]:
        current = self.start
        while current < self.stop:
            yield current
            current += self.step

    ## membership

    def __contains__(self, value: Union[P, "Interval[P, S]"]) -> bool:
        """Full containment of the other value"""
        if isinstance(value, Interval):
            assert (value.step / self.step).is_integer()
            return value[0] in self and value[-1] in self and (value.step / self.step).is_integer()
        else:
            return self.start <= value and value < self.stop and self.compatible_with(value)

    def overlaps(self, other: "Interval[P, S]") -> bool:
        """Partial containment of the other range"""
        assert self.step == other.step
        return self.start < other.stop and other.start < self.stop

    def neighbours(self, value: Union[P, "Interval[P, S]"]) -> bool:
        if value in self or self.overlaps(cast(Interval[P, S], value)):
            return True

        nexts = (self[0] + (-self.step), self[-1] + self.step)
        if isinstance(value, Interval):
            return any(v in nexts for v in (value[0], value[-1]))
        else:
            return value in nexts

    def compatible_with(self, value: Union[P, "Interval[P, S]"]) -> bool:
        if isinstance(value, Interval):
            if self.step != value.step:
                return False
            return self.compatible_with(value.start)
        else:
            return ((value - self.start) / self.step).is_integer()

    ## manipulation

    def replace(self, **kwargs: P):
        start, stop = self.start, self.stop
        if "start" in kwargs:
            start = kwargs["start"]
            del kwargs["start"]
        if "stop" in kwargs:
            stop = kwargs["stop"]
            del kwargs["stop"]

        if kwargs:
            raise Exception(f"unknown kwargs to replace: {list(kwargs.keys())}")

        return Interval(start, stop, step=self.step)

    def combine(self, other: "Interval[P, S]"):
        a, b = (self, other) if self.start < other.start else (other, self)
        if b in a:
            return a

        assert a.step == b.step, f"must have same step {self.step} != {other.step}"
        assert b.start in a or b.start == a[-1] + a.step
        return a.replace(stop=b.stop)

    def split(self, other: Union[P, "Interval[P, S]"]):
        if isinstance(other, Interval):
            if not self.overlaps(other):
                return [self]
            assert self.step == other.step
            exclude = (other.start, other[-1])
        else:
            if other not in self:
                return [self]
            exclude = (other, other)

        return list(
            filter(
                bool,
                [self.replace(stop=exclude[0]), self.replace(start=exclude[1] + self.step)],
            )
        )
