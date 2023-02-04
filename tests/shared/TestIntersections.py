from typing import Generic, TypedDict, TypeVar
from unittest import TestCase


class WithId(TypedDict):
    id: int


ToCompare = TypeVar('ToCompare', bound=WithId)

class TestIntersections(Generic[ToCompare], TestCase):
    def __init__(self, omitted_fields: set[str] | None = None) -> None:
        super().__init__()

        self.omitted = set(['created_at', 'updated_at'])
        if omitted_fields is not None:
            self.omitted = self.omitted.union(omitted_fields)


    def assert_dicts(
        self,
        first: ToCompare,
        second: ToCompare,
    ):
        first_keys = set(first)
        second_keys = set(second)

        needed_first = {}
        needed_second = {}
        for key in first_keys.intersection(second_keys):
            if key in self.omitted:
                continue

            needed_first[key] = first[key]
            needed_second[key] = second[key]

        self.assertDictEqual(needed_first, needed_second)


    def _sort(self, dicts: list[ToCompare]) -> list[ToCompare]:
        return sorted(dicts, key=lambda item: item['id'])


    def assert_lists(
        self,
        first: list[ToCompare],
        second: list[ToCompare],
        sort=True
    ):
        if sort:
            first, second = self._sort(first), self._sort(second)

        for first_item, second_item in zip(first, second):
            self.assert_dicts(first_item, second_item)
