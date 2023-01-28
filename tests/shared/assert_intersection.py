from typing import Any
from unittest import TestCase


def assert_intersection(
    first: dict[str, Any],
    second: dict[str, Any],
    ommited: list[str] = list()
):
    first_keys = set(first)
    second_keys = set(second)

    needed_first = {}
    needed_second = {}
    for key in first_keys.intersection(second_keys):
        if key in ommited:
            continue

        needed_first[key] = first[key]
        needed_second[key] = second[key]

    TestCase().assertDictEqual(needed_first, needed_second)
