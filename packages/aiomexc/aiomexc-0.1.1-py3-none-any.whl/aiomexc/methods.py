from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING, ClassVar, Generic
from dataclasses import dataclass
from http import HTTPMethod

from aiomexc.types import TickerPrice, MexcType, AccountInformation, Order


class MexcMethod(Generic[MexcType], ABC):
    if TYPE_CHECKING:
        __returning__: ClassVar[type]
        __api_http_method__: ClassVar[HTTPMethod]
        __api_method__: ClassVar[str]
        __requires_auth__: ClassVar[bool]
    else:

        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __api_http_method__(self) -> HTTPMethod:
            pass

        @property
        @abstractmethod
        def __api_method__(self) -> str:
            pass

        @property
        @abstractmethod
        def __requires_auth__(self) -> bool:
            pass


@dataclass(kw_only=True)
class GetTickerPrice(MexcMethod):
    __returning__ = TickerPrice
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "ticker/price"
    __requires_auth__ = False

    symbol: str


@dataclass(kw_only=True)
class GetAccountInformation(MexcMethod):
    __returning__ = AccountInformation
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "account"
    __requires_auth__ = True


@dataclass(kw_only=True)
class QueryOrder(MexcMethod):
    __returning__ = Order
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "order"
    __requires_auth__ = True

    symbol: str
    order_id: str | None
    orig_client_order_id: str | None
