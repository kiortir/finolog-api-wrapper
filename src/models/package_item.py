import datetime
from enum import Enum
from typing import Annotated, Any, Literal, NotRequired, Unpack

from pydantic import BaseModel, Field, RootModel
from typing_extensions import TypedDict

from models.utils import (
    Args,
    CustomBoolean,
    EntityCollection,
    MaybeRange,
    Decimal,
    Datetime,
)
from repository import ApiManager
from models.abc import BaseManager, Manager, LazyObject


class ItemGetArgs(TypedDict):
    page: NotRequired[int]
    pagesize: NotRequired[int]
    id: NotRequired[int]
    ids: NotRequired[MaybeRange[int]]
    query: NotRequired[str]


ItemGetArgsModelRoot = RootModel[ItemGetArgs]


class ItemGetArgsModel(Args, ItemGetArgsModelRoot):
    ...


class Item(Manager, BaseModel):
    id: int
    name: str
    is_archived: bool
    biz_id: int
    can_edit_initial_balance: bool
    description: str | None
    initial_count: int | None
    initial_currency_id: int | None
    initial_price: int | None
    price: Decimal | int | float
    price_currency_id: int
    sku: str | None
    type: Literal["product", "service"]
    unit_id: int
    vat: int
    summary: list[Any]
    summary_assets: list[Any]
    created_at: Datetime
    updated_at: Datetime
    deleted_at: Datetime | None
    created_by_id: int
    updated_by_id: int
    deleted_by_id: int


class ItemManager(BaseManager[Item]):
    def __init__(self, manager: ApiManager):
        self.manager: ApiManager = manager

    async def __getitem__(self, id: int) -> LazyObject[Item]:
        return await super().__getitem__(id)  # type: ignore

    async def _get_by_id(self, id: int):
        order = await self.manager.request("GET", f"/orders/items/{id}")
        return order

    async def get_list(self, **args: Unpack[ItemGetArgs]) -> list[Item]:
        orders: list[dict[str, Any]] = await self.manager.request(
            "GET", "/orders/item/", args=ItemGetArgsModel.model_validate(args)
        )
        return [Item(_manager=self, **order) for order in orders]

    async def create(self, **args):
        ...

    async def update(self, id: int):
        ...

    async def delete(self, id: int):
        ...
