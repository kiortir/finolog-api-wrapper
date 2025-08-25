from typing import Generic, Self, TypeVar

from pydantic import BaseModel

from finolog.repository import ApiManager

T = TypeVar("T")


class BaseManager(Generic[T]):
    biz_managers: dict[int, Self] = {}

    def __init__(self: Self, api_manager: ApiManager):
        self.api_manager: ApiManager = api_manager
        self.biz_managers[api_manager.biz_id] = self

    async def get_list(self, **args) -> list[T]:
        raise NotImplementedError()

    async def get(self, id: int) -> T:
        raise NotImplementedError()

    async def create(self, **args) -> T:
        raise NotImplementedError()

    async def update(self, id: int, **args) -> T:
        raise NotImplementedError()

    async def delete(self, id: int) -> dict[str, bool]:
        raise NotImplementedError()


ManagerType = TypeVar("ManagerType", bound=BaseManager)


class Record(BaseModel, Generic[ManagerType]):
    """Отвечает за работу с записями"""

    id: int
    _manager: ManagerType

    def __init__(self, _manager: ManagerType, **data):
        super().__init__(**data)
        self._manager = _manager

    async def update(self, **args):
        a = self.model_dump(exclude_none=True)
        a.update(args)
        response = await self._manager.update(**a)
        self.__dict__ = response.__dict__
        return response

    async def delete(self):
        return await self._manager.delete(self.id)
