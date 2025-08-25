from typing import Any

from pydantic import BaseModel

from finolog.models.abc import BaseManager, Record
from finolog.models.utils import Datetime, Decimal
from finolog.models.company import Summary


class AccountManager(BaseManager["Account"]):
    async def get(self, id: int):
        account = await self.api_manager.request("GET", f"/account/{id}")
        return Account(_manager=self, **account)

    async def get_list(self, **args) -> list["Account"]:
        accounts: list[dict[str, Any]] = await self.api_manager.request(
            "GET",
            "/account",
        )
        return [Account(_manager=self, **account) for account in accounts]


class Account(BaseModel, Record[AccountManager]):
    id: int
    bank_account: int | None = None
    bank_bik: str | None = None
    bank_iban: str | None = None
    bank_ks: str | None = None
    bank_mfo: str | None = None
    bank_name: str | None = None

    biz_id: int
    company_id: int
    created_at: Datetime

    created_by_id: int
    currency_id: int
    deleted_at: None | Datetime = None
    initital_balance: Decimal = Decimal(0)
    is_bank: bool = False
    is_closed: bool = False
    name: str
    planned_summary: list[Summary]
    summary: list[Summary]

    updated_at: Datetime | None = None
    updated_by_id: int | None = None

    # async def update(self, **args: Unpack[TransactionPutArgs.ArgDict]):
    #     return await super().update(**args)
