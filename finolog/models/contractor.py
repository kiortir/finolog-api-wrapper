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


class ContractorPostArgs(Arguments):
    class ArgDict(TypedDict):
        name: str


class ItemArgs(Arguments):
    class ArgDict(TypedDict):
        query: NotRequired[str]


class ContractorManager(BaseManager["Contractor"]):
    async def get(self, id: int):
        company = await self.api_manager.request("GET", f"/contractor/{id}")
        return Contractor(_manager=self, **company)

    async def get_list(
        self, **args: Unpack[ItemArgs.ArgDict]
    ) -> list["Contractor"]:
        orders: list[dict[str, Any]] = await self.api_manager.request(
            "GET", "/contractor", ItemArgs.model_validate(args)
        )
        return [Contractor(_manager=self, **order) for order in orders]

    async def create(self, name):
        c = await self.api_manager.request(
            "POST",
            "/contractor",
            ContractorPostArgs.model_validate({"name": name}),
        )
        return Contractor(_manager=self, **c)


class Contractor(BaseModel, Record["ContractorManager"]):
    id: int
    name: str
