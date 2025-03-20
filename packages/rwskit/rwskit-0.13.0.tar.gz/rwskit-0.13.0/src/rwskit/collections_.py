"""Utilities for working with collections."""

# Future Library
from __future__ import annotations

# Standard Library
import logging as log

from types import GeneratorType
from typing import Any, Iterable, Mapping, Optional

# 3rd Party Library
import yaml

log = log.getLogger(__name__)


def is_iterable(obj: Any, consider_string_iterable: bool = False) -> bool:
    """
    Tests if the object is iterable.

    Parameters
    ----------
    obj : any
        An object.
    consider_string_iterable : bool, default = False
        Whether to consider strings iterable or not.

    Returns
    -------
    bool
        ``True`` if ``obj`` is iterable.
    """
    if isinstance(obj, str):
        return consider_string_iterable

    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def is_generator(obj: Any) -> bool:
    """
    Checks if the object is a generator.

    Parameters
    ----------
    obj : any
        An object.

    Returns
    -------
    bool
        ``True`` if the object is a generator.

    """
    return isinstance(obj, GeneratorType)


def get_first_non_null_value(collection: Iterable) -> Optional[Any]:
    """Recursively try to get the first non-null value in a collection.

    This method will recursively traverse the collection until it finds
    a non-iterable value that is not ``None``.

    Parameters
    ----------
    collection : Iterable
        The collection to retrieve the value from.

    Returns
    -------
    Any, optional
        The first non-null value in the series, if one exists, otherwise return
        ``None``.

    """
    for value in collection:
        if is_iterable(value) and not isinstance(value, str):
            value = get_first_non_null_value(value)

        if value is not None:
            return value

    return None


def recursive_sort(obj: Any) -> Any:
    """
    Attempts to sort an object recursively according to the following rules:

    * If the object is a dictionary, it will be sorted by its keys and its
      values will be sorted recursively.
    * If the object is a list or tuple, it will be sorted by its values.
      Typically, a value is a primitive, but lists, tuples, and dictionaries
      are also valid. In these cases, the collections are compared after
      sorting.
    * Any other value is returned unchanged.

    .. note::
        Collections of dictionaries (e.g., lists, tuples, sets, other
        dictionaries) cannot be directly compared because ``__lt__`` is not
        defined. When a collection of dictionaries is encountered, they are
        compared using (sorted) yaml strings. Yaml is used because it supports
        sorting by keys, similar to json, but supports more data types.

    Parameters
    ----------
    obj : Any
        The input object

    Returns
    -------
    Any
        The returned object sorted.

    Raises
    ------
    TypeError
        If you have a collection of dictionaries that cannot be converted to
        yaml strings.
    """

    def _key_fn(e: Any) -> Any:
        if isinstance(e, dict):
            return yaml.dump(
                e,
                sort_keys=True,
                default_flow_style=True,
                explicit_start=False,
                explicit_end=False,
                width=float("inf"),
            )
        elif is_iterable(e):
            return sorted(e, key=lambda x: _key_fn(x))
        else:
            return e

    if isinstance(obj, dict):
        return {k: recursive_sort(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        values = sorted(obj, key=lambda e: _key_fn(e))
        return [recursive_sort(e) for e in values]
    elif isinstance(obj, tuple):
        values = sorted(obj, key=_key_fn)
        return tuple([recursive_sort(e) for e in values])
    elif is_iterable(obj) or is_generator(obj):
        return list(obj)
    else:
        return obj


def remove_none_from_dict(d: dict[Any, Any]) -> dict[Any, Any]:
    """Recursively remove ``None`` values from a (nested) dictionary."""

    def _do_removal(obj: Any) -> Any:
        if isinstance(obj, Mapping):
            return {k: _do_removal(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [remove_none_from_dict(e) for e in obj]
        elif isinstance(obj, set):
            return {remove_none_from_dict(e) for e in obj}  # type: ignore
        else:
            return obj

    return _do_removal(d)
