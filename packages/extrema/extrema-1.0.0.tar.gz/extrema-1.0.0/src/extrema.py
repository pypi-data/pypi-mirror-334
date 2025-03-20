"""Finding an iterable's minima or maxima.

Functions
---------
minima
    Minimize a function on an iterable.
maxima
    Maximize a function on an iterable.
"""

import functools


@functools.total_ordering
class _Max:
    def __eq__(self, other):
        return isinstance(other, _Max)

    def __ge__(self, other):
        return True


_MAX = _Max()


def minima(items, key=lambda item: item):
    """Minimize key on items.

    Examples
    --------
    >>> import extrema
    >>> extrema.minima([1, 2, -1, -2], abs)
    [1, -1]
    >>> extrema.minima([])
    []
    """
    least_key = _MAX
    minima_ = []
    for item in items:
        this_key = key(item)
        if least_key >= this_key:
            if least_key > this_key:
                least_key = this_key
                minima_ = []
            minima_.append(item)
    return minima_


@functools.total_ordering
class _Min:
    def __eq__(self, other):
        return isinstance(other, _Min)

    def __le__(self, other):
        return True


_MIN = _Min()


def maxima(items, key=lambda item: item):
    """Maximize key on items.

    Examples
    --------
    >>> import extrema
    >>> extrema.maxima([1, 2, -1, -2], abs)
    [2, -2]
    >>> extrema.maxima([])
    []
    """
    greatest_key = _MIN
    maxima_ = []
    for item in items:
        this_key = key(item)
        if greatest_key <= this_key:
            if greatest_key < this_key:
                greatest_key = this_key
                maxima_ = []
            maxima_.append(item)
    return maxima_
