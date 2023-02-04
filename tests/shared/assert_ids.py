from typing import Any, Iterable, Protocol, TypeVar


class ModelWithId(Protocol):
    id: Any

FirstItem = TypeVar('FirstItem', bound=ModelWithId)
SecondItem = TypeVar('SecondItem', bound=ModelWithId)


def access_id(with_id: ModelWithId) -> int:
    if isinstance(with_id, dict):
        return with_id['id']
    else:
        return with_id.id

def assert_ids(first: Iterable[FirstItem], second: Iterable[SecondItem]) -> None:
    first_ids = [access_id(item) for item in first]
    second_ids = [access_id(item) for item in second]

    assert first_ids == second_ids
