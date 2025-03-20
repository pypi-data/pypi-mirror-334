import itertools
from typing import Generic, Iterable, Optional, Union

from .interval import Interval, P, S


class MultInterval(Generic[P, S]):
    __slots__ = ("intervals", "step")
    step: S
    intervals: list[Interval[P, S]]

    def __init__(
        self,
        *,
        step: S = 1,  # type: ignore
        ranges: Optional[list[Interval[P, S]]] = None,
    ):
        self.step = step
        self.intervals = []

        if ranges:
            assert all(step == r.step for r in ranges)
            assert all(r.compatible_with(ranges[0].start) for r in ranges)
            self.intervals = sorted(ranges, key=lambda r: r.start)

    ## identity

    def to_tuple(self):
        return (self.step, self.intervals)

    def __repr__(self):
        return f"MultiInterval(step={self.step}, ranges={self.intervals})"

    def __hash__(self):
        return hash((self.step, self.intervals))

    def __eq__(self, other: object):
        if not isinstance(other, MultInterval):
            return False
        return self.to_tuple() == other.to_tuple()

    ## properties

    def __bool__(self) -> bool:
        return bool(self.intervals) and any(r for r in self.intervals)

    def __len__(self) -> int:
        return sum(len(r) for r in self.intervals)

    ## access / iteration

    def __getitem__(self, index: int) -> P:
        if index < 0:
            index += len(self)
        for r in self.intervals:
            if index >= len(r):
                index -= len(r)
                continue
            return r[index]
        raise IndexError("index out of range")

    def __iter__(self) -> Iterable[P]:
        for r in self.intervals:
            yield from r

    ## membership

    def __contains__(self, value: Union[P, Interval[P, S], "MultInterval[P, S]"]) -> bool:
        """Full containment of the other value"""
        if isinstance(value, MultInterval):
            return all(r in self for r in value.intervals)
        else:
            return any(value in r for r in self.intervals)

    def overlaps(self, other: Union[Interval[P, S], "MultInterval[P, S]"]):
        """Partial containment of the other range"""
        if isinstance(other, MultInterval):
            return any(r.overlaps(s) for r in self.intervals for s in other.intervals)
        else:
            return any(r.overlaps(other) for r in self.intervals)

    def compatible_with(self, value: Union[P, Interval[P, S], "MultInterval[P, S]"]) -> bool:
        if isinstance(value, MultInterval):
            return self.step == value.step and (
                not self.intervals or self.intervals[0].compatible_with(value.intervals[0])
            )
        else:
            return not self.intervals or self.intervals[0].compatible_with(value)

    ## manipulation

    def _compact(self):
        self.intervals = sorted(self.intervals, key=lambda r: r.start)
        index = 0
        while index < len(self.intervals) - 1:
            a, b = self.intervals[index : index + 2]
            if a.neighbours(b):
                self.intervals[index : index + 2] = [a.combine(b)]
            else:
                index += 1

    def include(self, *others: Union[P, Interval[P, S], "MultInterval[P, S]"]):
        assert all(self.compatible_with(o) for o in others)
        ranges = list(
            itertools.chain.from_iterable(
                o.intervals
                if isinstance(o, MultInterval)
                else [o if isinstance(o, Interval) else Interval(o, o + self.step, step=self.step)]
                for o in others
            )
        )
        self.intervals.extend(ranges)
        self._compact()
        return self

    def exclude(self, other: Union[P, Interval[P, S], "MultInterval[P,S]"]):
        assert self.compatible_with(other)
        if isinstance(other, MultInterval):
            for r in other.intervals:
                self.exclude(r)
        else:
            self.intervals = list(
                filter(
                    bool,
                    itertools.chain.from_iterable(r.split(other) for r in self.intervals),
                )
            )
        return self
