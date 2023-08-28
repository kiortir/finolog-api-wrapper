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
        query: NotRequired[str]


class ContractorManager(BaseManager["Contractor"]):
    async def get(self, id: int):
        company = await self.api_manager.request("GET", f"/company/{id}")
        return Contractor(_manager=self, **company)

    async def get_list(
        self, **args: Unpack[ItemArgs.ArgDict]
    ) -> list["Contractor"]:
        orders: list[dict[str, Any]] = await self.api_manager.request(
            "GET", "/orders/order", ItemArgs.model_validate(args)
        )
        return [Contractor(_manager=self, **order) for order in orders]


class Contractor(Record["ContractorManager"], BaseModel):
    id: int
    name: str
