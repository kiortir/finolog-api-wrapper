import datetime
from enum import Enum
from typing import (
    Annotated,
    Any,
    Literal,
    NotRequired,
    Sequence,
    Unpack,
    overload,
)

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from finolog.models.abc import BaseManager, Record
from finolog.models.arguments import Arguments
from finolog.models.utils import (
    CustomBoolean,
    Datetime,
    Decimal,
    EntityCollection,
    MaybeRange,
)


class TransactionType(str, Enum):
    IN = "in"
    OUT = "out"


class TransactionStatus(str, Enum):
    REGULAR = "regular"
    PLANNED = "planned"


class TransactionCategoryType(str, Enum):
    """
    in - приход
    out - расход
    inout - перевод
    """

    IN = "in"
    OUT = "out"
    INOUT = "inout"


class TransactionCategoryActivities(str, Enum):
    """
    Вид деятельности статьи
    """

    OPERATING = "operating"
    FINANCIAL = "financial"
    INVESTMENT = "investment"


class TransactionCategoryCode(str, Enum):
    """
    Код статьи
    transfer - нераспределенные переводы
    taxes - налоги
    unallocated_in - нераспределенные приходы
    unallocated_out - нераспределенные расходы
    cash_in - ввод денег
    cash_out - вывод денег
    """

    TRANSFER = "transfer"
    TAXES = "taxes"
    UNALLOCATED_IN = "unallocated_in"
    UNALLOCATED_OUT = "unallocated_out"
    CASH_IN = "cash_in"
    CASH_OUT = "cash_out"


class AvailableWith(str, Enum):
    ACCOUNT = "account"
    CATEGORY = "category"
    CONTRACTOR = "contractor"
    REQUISITE = "requisite"
    PROJECT = "project"
    ORDER = "order"
    AUTOEDITOR = "autoeditor"


class TransactionGetArgs(Arguments):
    class ArgDict(TypedDict):
        ids: NotRequired[EntityCollection[int]]
        type: NotRequired[TransactionType]
        status: NotRequired[TransactionStatus]
        date: NotRequired[MaybeRange[Datetime]]
        report_date: NotRequired[MaybeRange[Datetime]]
        value: NotRequired[MaybeRange[Decimal | int | float]]
        base_value: NotRequired[MaybeRange[Decimal | int | float]]
        description: NotRequired[str]
        category_ids: NotRequired[EntityCollection[int]]
        category_type: NotRequired[TransactionCategoryType]
        category_activities: NotRequired[TransactionCategoryActivities]
        category_code: NotRequired[TransactionCategoryCode]
        category_cash_in_out: NotRequired[CustomBoolean | Literal["all"]]
        category_interest_repayment: NotRequired[CustomBoolean]
        company_ids: NotRequired[EntityCollection[int]]
        account_ids: NotRequired[EntityCollection[int]]
        contractor_ids: NotRequired[EntityCollection[int]]
        requisite_ids: NotRequired[EntityCollection[int]]
        project_ids: NotRequired[EntityCollection[int]]
        order_ids: NotRequired[EntityCollection[int]]
        order_type: NotRequired[TransactionType]
        created_at: NotRequired[MaybeRange[Datetime]]
        updated_at: NotRequired[MaybeRange[Datetime]]
        deleted_at: NotRequired[MaybeRange[Datetime]]
        created_by_ids: NotRequired[EntityCollection[int]]
        updated_by_ids: NotRequired[EntityCollection[int]]
        deleted_by_ids: NotRequired[EntityCollection[int]]

        page: NotRequired[int]
        pagesize: NotRequired[int]
        with_: NotRequired[
            Annotated[
                AvailableWith,
                Field(serialization_alias="with"),
            ]
        ]
        extra: NotRequired[
            Literal["transfer", "split"]
        ]  # TODO: Разбить на несколько классов
        base_value_from: NotRequired[Decimal | int | float]
        base_value_to: NotRequired[Decimal | int | float]
        category_id: NotRequired[int]
        category_group_id: NotRequired[int]
        category_group_ids: NotRequired[EntityCollection[int]]
        contractor_id: NotRequired[int]
        requisite_id: NotRequired[int]
        project_id: NotRequired[int]
        order_id: NotRequired[int]
        report_date_from: NotRequired[MaybeRange[Datetime]]
        report_date_to: NotRequired[MaybeRange[Datetime]]
        descriptions: NotRequired[list[str]]
        query: NotRequired[str]
        with_transfer: NotRequired[CustomBoolean]
        with_multi_transfer: NotRequired[Literal["true"]]
        with_bizzed: NotRequired[CustomBoolean]
        with_splitted: NotRequired[CustomBoolean]
        created: NotRequired[MaybeRange[Datetime]]
        changed: NotRequired[MaybeRange[Datetime]]
        tax_types: NotRequired[EntityCollection[str]]
        without_closed_accounts: NotRequired[CustomBoolean]


class TransactionPostBaseArgs(TypedDict):
    company_id: NotRequired[int]
    category_id: NotRequired[int]
    contractor_id: NotRequired[int]
    requisite_id: NotRequired[int]
    project_id: NotRequired[int]
    date: datetime.date
    report_date: NotRequired[datetime.date]
    value: Decimal | int | float
    from_value: NotRequired[Decimal | int | float]
    to_value: NotRequired[Decimal | int | float]
    status: NotRequired[TransactionStatus]
    description: NotRequired[str]
    order_id: NotRequired[int]
    is_debt: NotRequired[bool]


class TransactionPostFromArgs(TransactionPostBaseArgs, TypedDict):
    from_id: int


class TransactionPostToArgs(TransactionPostBaseArgs, TypedDict):
    to_id: int


class TransactionPostArgs(Arguments):
    class ArgDict(TransactionPostBaseArgs, TypedDict):
        from_id: NotRequired[int]
        to_id: NotRequired[int]


class TransactionPutArgs(Arguments):
    class ArgDict(TypedDict):
        company_id: NotRequired[int]
        category_id: NotRequired[int]
        contractor_id: NotRequired[int]
        requisite_id: NotRequired[int]
        project_id: NotRequired[int]
        date: NotRequired[datetime.date]
        report_date: NotRequired[datetime.date]
        from_id: NotRequired[int]
        to_id: NotRequired[int]
        value: NotRequired[Decimal | int | float]
        from_value: NotRequired[Decimal | int | float]
        to_value: NotRequired[Decimal | int | float]
        status: NotRequired[TransactionStatus]
        description: NotRequired[str]
        order_id: NotRequired[int]
        is_debt: NotRequired[bool]


class ItemArgs(Arguments):
    class ArgDict(TypedDict):
        value: Decimal | int | float
        report_date: NotRequired[datetime.date]
        category_id: NotRequired[int]
        project_id: NotRequired[int]
        contractor_id: NotRequired[int]
        requisite_id: NotRequired[int]
        order_id: NotRequired[int]
        is_debt: NotRequired[bool]


class SplitArgs(BaseModel):
    id: int
    items: Sequence[ItemArgs]


class TransactionManager(BaseManager["Transaction"]):
    async def get(self, id: int):
        transaction = await self.api_manager.request(
            "GET", f"/transaction/{id}"
        )
        return Transaction(_manager=self, **transaction)

    async def get_list(
        self, **args: Unpack[TransactionGetArgs.ArgDict]
    ) -> list["Transaction"]:
        transactions: list[dict[str, Any]] = await self.api_manager.request(
            "GET",
            "/transaction",
            TransactionGetArgs.model_validate(args),
        )
        return [
            Transaction(_manager=self, **transaction)
            for transaction in transactions
        ]

    @overload
    async def create(self, **args: Unpack[TransactionPostFromArgs]):
        ...

    @overload
    async def create(self, **args: Unpack[TransactionPostToArgs]):
        ...

    async def create(self, **args: Unpack[TransactionPostArgs.ArgDict]):
        response = await self.api_manager.request(
            "POST",
            "/transaction",
            TransactionPostArgs.model_validate(args),
        )
        return Transaction(_manager=self, **response)

    async def update(
        self, id: int, **args: Unpack[TransactionPutArgs.ArgDict]
    ):
        response = await self.api_manager.request(
            "PUT",
            f"/transaction/{id}",
            TransactionPutArgs.model_validate(args),
        )
        return Transaction(_manager=self, **response)

    async def delete(self, id: int) -> dict[str, bool]:
        response = await self.api_manager.request(
            "DELETE", f"/transaction/{id}"
        )
        return response

    async def split(self, *args: ItemArgs.ArgDict, id: int):
        split = await self.api_manager.request(
            "POST",
            f"/transaction/{id}/split",
            SplitArgs(
                id=id, items=[ItemArgs.model_validate(arg) for arg in args]
            ),
        )
        return split


class Transaction(BaseModel, Record[TransactionManager]):
    id: int
    date: datetime.date
    biz_id: int
    account_id: int
    type: TransactionType
    category_id: int
    contractor_id: int | None = None
    description: str | None = None
    value: Decimal | int | float
    created_at: Datetime
    updated_at: Datetime
    created_by_id: int
    updated_by_id: int
    base_value: Decimal | int | float
    requisite_id: int | None = None
    transfer_id: int | None
    report_date: datetime.date
    status: TransactionStatus
    split_id: EntityCollection[int] | None = None
    payment_id: int | None = None
    schedule_id: int | None = None
    source_id: int | None = None
    project_id: int | None = None
    is_splitted: bool
    deleted_at: Datetime | None = None
    deleted_by_id: int | None = None
    order_id: int | None = None
    is_multi_transfer: bool | None = None
    is_debt: bool | None = None
    has_comments: bool
    payment_number: int | None = None
    vat: Decimal | int | float | None = None
    base_vat: Decimal | int | float | None = None
    autoeditor_id: int | None = None
    original_schedule_id: int | None = None
    original_schedule: None = None

    async def update(self, **args: Unpack[TransactionPutArgs.ArgDict]):
        return await super().update(**args)

    async def split(self, *args: ItemArgs.ArgDict):
        if abs(self.value) != abs(sum(arg["value"] for arg in args)):
            raise ValueError("Нельзя дробить транзакцию на эти суммы")
        split = await self._manager.split(id=self.id, *args)
        return split
