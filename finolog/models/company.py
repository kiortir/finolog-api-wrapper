import datetime
from typing import Any

from pydantic import BaseModel

from models.abc import BaseManager, Record
from models.transaction import TransactionStatus
from models.utils import Datetime, Decimal


class CompanyManager(BaseManager["Company"]):
    async def get(self, id: int):
        company = await self.api_manager.request("GET", f"/company/{id}")
        return Company(_manager=self, **company)

    async def get_list(self) -> list["Company"]:
        companies: list[dict[str, Any]] = await self.api_manager.request(
            "GET",
            "/company",
        )
        # return companies
        return [Company(_manager=self, **company) for company in companies]


class Summary(BaseModel):
    balance: Decimal | None = None
    base_balance: Decimal | None = None
    base_outcoming: Decimal | None = None
    company_id: int | None = None
    currency_id: int | None = None
    date: datetime.date | None = None
    incoming: Decimal | None = None
    type: TransactionStatus | None = None


# class Company(Record["CompanyManager"], BaseModel):
#     id: int
#     bank_account: int
#     bank_bik: int
#     bank_iban: str
#     bank_ks: int
#     bank_mfo: int
#     bank_name: str

#     biz_id: int
#     company_id: int
#     created_at: Datetime

#     created_by_id: int
#     currency_id: int
#     deleted_at: None | Datetime = None
#     initital_balance: Decimal
#     is_bank: bool = False
#     is_closed: bool = False
#     name: str
#     planned_summary:
# async def update(self, **args: Unpack[TransactionPutArgs.ArgDict]):
#     return await super().update(**args)


class Company(Record["CompanyManager"], BaseModel):
    id: int
    name: str
    full_name: str

    address_city: str | None = None
    address_postal_index: str | None = None
    address_street: str | None = None
    biz_id: int
    contractor_id: int | None = None
    country_id: int | None = None
    created_at: Datetime
    created_by_id: int
    director_name: None | str = None
    director_position: None | str = None
    director_sign: None | str = None
    director_sign_file_id: int | None = None
    email: None | str = None
    inn: int | None = None
    is_closed: bool = False
    kpp: int | None = None
    logo: str | None = None
    logo_file_id: int | None = None
    more_information: Any | None = None
    phone: str | Any | None = None
    stamp: None | Any = None
    updated_at: Datetime | None = None
    updated_by_id: int | None = None
    web: None | Any = None

    planned_summary: list[Summary]
    summary: list[Summary]
