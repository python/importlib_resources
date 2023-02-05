from collections import defaultdict, deque
from itertools import filterfalse

from typing import (
    Callable,
    Iterable,
    Iterator,
    Optional,
    Set,
    TypeVar,
    Union,
)

# Type and type variable definitions
_T = TypeVar('_T')
_U = TypeVar('_U')


def unique_everseen(
    iterable: Iterable[_T], key: Optional[Callable[[_T], _U]] = None
) -> Iterator[_T]:
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen: Set[Union[_T, _U]] = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


# from more_itertools 9.0
class bucket:
    """Wrap *iterable* and return an object that buckets it iterable into
    child iterables based on a *key* function.

    >>> iterable = ['a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'b3']
    >>> s = bucket(iterable, key=lambda x: x[0])  # Bucket by 1st character
    >>> sorted(list(s))  # Get the keys
    ['a', 'b', 'c']
    >>> a_iterable = s['a']
    >>> next(a_iterable)
    'a1'
    >>> next(a_iterable)
    'a2'
    >>> list(s['b'])
    ['b1', 'b2', 'b3']

    The original iterable will be advanced and its items will be cached until
    they are used by the child iterables. This may require significant storage.
    By default, attempting to select a bucket to which no items belong  will
    exhaust the iterable and cache all values.
    If you specify a *validator* function, selected buckets will instead be
    checked against it.

    >>> from itertools import count
    >>> it = count(1, 2)  # Infinite sequence of odd numbers
    >>> key = lambda x: x % 10  # Bucket by last digit
    >>> validator = lambda x: x in {1, 3, 5, 7, 9}  # Odd digits only
    >>> s = bucket(it, key=key, validator=validator)
    >>> 2 in s
    False
    >>> list(s[2])
    []
    """

    def __init__(self, iterable, key, validator=None):
        self._it = iter(iterable)
        self._key = key
        self._cache = defaultdict(deque)
        self._validator = validator or (lambda x: True)

    def __contains__(self, value):
        if not self._validator(value):
            return False

        try:
            item = next(self[value])
        except StopIteration:
            return False
        else:
            self._cache[value].appendleft(item)

        return True

    def _get_values(self, value):
        """
        Helper to yield items from the parent iterator that match *value*.
        Items that don't match are stored in the local cache as they
        are encountered.
        """
        while True:
            # If we've cached some items that match the target value, emit
            # the first one and evict it from the cache.
            if self._cache[value]:
                yield self._cache[value].popleft()
            # Otherwise we need to advance the parent iterator to search for
            # a matching item, caching the rest.
            else:
                while True:
                    try:
                        item = next(self._it)
                    except StopIteration:
                        return
                    item_value = self._key(item)
                    if item_value == value:
                        yield item
                        break
                    elif self._validator(item_value):
                        self._cache[item_value].append(item)

    def __iter__(self):
        for item in self._it:
            item_value = self._key(item)
            if self._validator(item_value):
                self._cache[item_value].append(item)

        yield from self._cache.keys()

    def __getitem__(self, value):
        if not self._validator(value):
            return iter(())

        return self._get_values(value)
