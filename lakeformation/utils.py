# -*- coding: utf-8 -*-

from typing import List, Set, Tuple, Dict, Iterable, Any
from datetime import datetime, timezone
from ordered_set import OrderedSet

var_name_escape = {
    "-": "_",
    ":": "_",
    "/": "__",
    ".": "_dot_",
}


def to_var_name(s: str) -> str:
    """
    Convert string to variable name safe format. For example::

        >>> to_var_name("us-east-1")
        us_east_1
        >>> to_var_name("arn:aws")
        arn_aws
        >>> to_var_name("a/b")
        a__b
        >>> to_var_name("database.table")
        database_dot_table
    """
    for k, v in var_name_escape.items():
        s = s.replace(k, v)
    return s


def get_local_and_utc_now() -> Tuple[datetime, datetime]:
    """
    Get current time in both local timezone format and utc format.
    """
    local_now = datetime.now().replace(microsecond=0)
    local_tz = local_now.astimezone().tzinfo
    local_now = local_now.replace(tzinfo=local_tz)
    utc_now = local_now.astimezone(timezone.utc)
    return local_now, utc_now


def get_diff_and_inter(
    dct1: Dict[str, Any],
    dct2: Dict[str, Any],
) -> Tuple[OrderedSet, OrderedSet, OrderedSet]:
    """
    Each deployed ``Object`` usually has a unique id. ``Mapper`` is a dictionary
    data structure that stores a collection of ``Object``. Key is the
    ``Object`` id, value is the ``Object`` instance.

    Given a new ``Mapper`` and a deployed ``Mapper``, it is very common to
    find out which ``Object`` should be added, should be delayed and should be
    updated.

    This utility function takes two parameter

    1. new object ``Mapper``
    2. deployed object ``Mapper``

    Returns three set data structure

    1. to add object id set
    2. to delete object id set
    3. to update object id set

    :param dct1:
    :param dct2:
    :return:
    """
    s1 = OrderedSet(dct1)
    s2 = OrderedSet(dct2)
    return s1.difference(s2), s2.difference(s1), s1.intersection(s2)


def grouper_list(iterable: Iterable, n: int) -> List[list]:
    """
    Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.

    Example::

        >>> list(grouper_list(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    chunk = list()
    counter = 0
    for item in iterable:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk
