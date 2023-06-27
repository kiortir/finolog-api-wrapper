from datetime import datetime
from decimal import Decimal as DEC
from enum import Enum
from typing import Annotated, TypeAlias, TypeVar, Union

from pydantic import BaseModel, PlainSerializer

T = TypeVar("T")
EntityCollection = Annotated[
    tuple[T, ...], PlainSerializer(lambda v: ",".join(str(e) for e in v))
]


MaybeRange = Union[T, tuple[T, T]]

CustomBoolean: TypeAlias = bool
Decimal = Annotated[DEC, PlainSerializer(lambda v: float(v))]
Datetime = Annotated[
    datetime, PlainSerializer(lambda v: v.strftime("%Y-%m-%d %H:%M:%S"))
]


class TaxTypes(str, Enum):
    """
    Фильтр по статьям налогов через запятую
    Available values :
    taxes_vat(НДС)
    taxes_foundation(Фонд оплаты труда)
    taxes_property(Налог на собственность)
    taxes_money(Налог на доход)
    """

    TAXES_VAT = "taxes_vat"
    TAXES_FOUNDATION = "taxes_foundation"
    TAXES_PROPERTY = "taxes_property"
    TAXES_MONEY = "taxes_money"


class Args(BaseModel):
    ...
