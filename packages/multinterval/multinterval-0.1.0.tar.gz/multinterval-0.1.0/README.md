# MultInterval

Represent large intervals of numeric/datetime data in Python with a small memory footprint.

## When to Use

- Your data is a long contiguous stretches (in fixed steps) of data that is separated by few missing gaps.
- Each data point can be compared to another, and divisble by the step factor (supports datetime/timedelta combinations)


## How to Use

```py
import multinterval as mi

# at instantiation, only a step is necessary
i = mi.MultInterval(step=5)
print(list(i))  # outputs []

# the set is fully instantiated only when there is at least one member
i.include(3)
print(list(i))  # outputs [3]


# include other compatible values, Intervals, MultIntervals
i.include(8, 13, 23) # include multiple numbers
i.include(mi.Interval(53, 68, step=5)) # include full intervals
i.include(
	mi.MultInterval(
		step=5,
		ranges=[mi.Interval(103, 113, step=5), mi.Interval(158, 193, step=5)],
	)
)
print(list(i))  # outputs [3, 8, 13, 23, 53, 58, 63, 103, 108, 158, 163, 168, 173, 178, 183, 188]


# exclude any compatible values
i.exclude(23)
i.exclude(mi.Interval(13, 108, step=5))
i.exclude(
	mi.MultInterval(
		step=5,
		ranges=[mi.Interval(53, 178, step=5)],
	)
)
print(list(i))  # outputs [3, 8, 178, 183, 188]


# the following will cause errors

# including values not in the same number line will cause an error
# i.include(7)

# including intervals on a different step
# i.include(mi.Interval(3, 9, step=3))

# including intervals that do not coincide on the same step
# i.include(mi.Interval(4, 10, step=5))
```

## Implementation Details

- Complete intervals are represented with a tuple of inclusive start and exclusive end.
- Longer intervals with gaps are represented by a list of the complete intervals.
