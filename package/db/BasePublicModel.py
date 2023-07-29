from abc import abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

Public = TypeVar('Public', bound=BaseModel)


class BasePublicModel(Generic[Public]):
    @abstractmethod
    async def public(self) -> Public:
        ...
