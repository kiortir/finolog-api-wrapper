import datetime
from typing import Any, NotRequired, TypedDict, Unpack

from pydantic import BaseModel

from finolog.models.abc import BaseManager, Record
from finolog.models.transaction import TransactionStatus, TransactionType
from finolog.models.utils import Datetime, Decimal
from finolog.models.arguments import Arguments

from finolog.models.utils import (
    CustomBoolean,
    Datetime,
    Decimal,
    EntityCollection,
    MaybeRange,
)


class ItemArgs(Arguments):
    class ArgDict(TypedDict):
        status_ids: NotRequired[MaybeRange[int]]
        contractor_ids: NotRequired[MaybeRange[int]]
        requisite_ids: NotRequired[MaybeRange[int]]
        type: NotRequired[TransactionType]
        date: NotRequired[MaybeRange[datetime.date]]
        description: NotRequired[str]
        page: NotRequired[int]
        pagesize: NotRequired[int]
        ids: NotRequired[int]
        query: NotRequired[str]
        descriptions: NotRequired[list[str]]


class OrderManager(BaseManager["Order"]):
    async def get(self, id: int):
        order = await self.api_manager.request("GET", f"/orders/order/{id}")
        return Order(_manager=self, **order)

    async def get_list(
        self, **args: Unpack[ItemArgs.ArgDict]
    ) -> list["Order"]:
        orders: list[dict[str, Any]] = await self.api_manager.request(
            "GET", "/orders/order", ItemArgs.model_validate(args)
        )
        return [Order(_manager=self, **order) for order in orders]


class Order(Record["OrderManager"], BaseModel):
    id: int

    biz_id: int
    buyer_id: int
    buyer: dict[str, Any]
    cost: Decimal
    cost_package: None | Any = None
    cost_package_id: None | Any = None
    created_at: Datetime
    created_by_id: int
    currency_id: int
    date: Datetime
    deleted_at: None | Datetime = None
    deleted_by_id: None | int = None
    description: None | str = None
    documents: list[Any]
    number: str
    offer_id: None | int = None
    package: dict[str, Any]
    package_id: int | None = None
    paid: Decimal
    paid_at: Datetime | None = None
    paid_status: str
    payment_method_id: None | int = None
    payment_url: str
    seller: dict[str, Any]
    seller_id: int
    shipment: int
    shipped_at: None | Datetime = None
    shipped_status: str
    status_id: None | int = None
    token: str
    type: str
    updated_at: Datetime | None = None
    updated_by_id: int | None = None
    utm_campaign: None | Any = None
    utm_content: None | Any = None
    utm_medium: None | Any = None
    utm_source: None | Any = None
    utm_term: None | Any = None
    widget_id: None | Any = None
