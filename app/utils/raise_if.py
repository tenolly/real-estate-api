from typing import TypeVar


T = TypeVar("T")


def raise_if_none(target: T, error: Exception) -> T:
    if target is None:
        raise error

    return target


def raise_if_not_none(target: T, error: Exception) -> T:
    if target is not None:
        raise error

    return target
