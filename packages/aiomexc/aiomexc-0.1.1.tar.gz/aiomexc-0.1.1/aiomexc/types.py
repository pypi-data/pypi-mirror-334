from decimal import Decimal
from typing import TypeVar, Generic
from dataclasses import dataclass

from aiomexc.enums import OrderStatus, OrderType, OrderSide

MexcType = TypeVar("MexcType")


@dataclass
class MexcResult(Generic[MexcType]):
    ok: bool = True
    msg: str | None = None
    code: int | None = None
    result: MexcType | None = None


@dataclass
class TickerPrice:
    symbol: str
    price: Decimal


@dataclass
class Balance:
    asset: str
    free: Decimal
    locked: Decimal


@dataclass
class AccountInformation:
    can_trade: bool
    can_withdraw: bool
    can_deposit: bool
    update_time: int | None
    account_type: str
    balances: list[Balance]
    permissions: list[str]


@dataclass
class Order:
    symbol: str
    order_id: str
    order_list_id: int | None
    client_order_id: str | None
    price: Decimal
    orig_qty: Decimal
    executed_qty: Decimal
    cummulative_quote_qty: Decimal
    status: OrderStatus
    time_in_force: int | None
    type: OrderType
    side: OrderSide
    stop_price: Decimal | None
    time: int
    update_time: int
    is_working: bool
    orig_quote_order_qty: Decimal | None
