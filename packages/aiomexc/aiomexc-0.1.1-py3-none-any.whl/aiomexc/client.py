from aiomexc.methods import GetTickerPrice, GetAccountInformation, QueryOrder, MexcMethod
from aiomexc.types import TickerPrice, AccountInformation, Order, MexcType

from .session.base import BaseSession, Credentials
from .session.aiohttp import AiohttpSession


class MexcClient:
    def __init__(
        self, credentials: Credentials | None = None, session: BaseSession | None = None
    ):
        if session is None:
            session = AiohttpSession()

        self.session = session
        self.credentials = credentials

    async def __call__(
        self, method: MexcMethod[MexcType], credentials: Credentials | None = None
    ) -> MexcType:
        if method.__requires_auth__:
            credentials = credentials or self.credentials
            if credentials is None:
                raise ValueError(
                    f"Credentials are required for {method.__api_method__!r} method"
                )

            return await self.session.make_signed_request(method, credentials)
        else:
            return await self.session.make_request(method)

    async def get_ticker_price(self, symbol: str) -> TickerPrice:
        return await self(GetTickerPrice(symbol=symbol))

    async def get_account_information(
        self, credentials: Credentials | None = None
    ) -> AccountInformation:
        return await self(GetAccountInformation(), credentials=credentials)

    async def query_order(
        self,
        symbol: str,
        order_id: str | None = None,
        orig_client_order_id: str | None = None,
        credentials: Credentials | None = None,
    ) -> Order:
        return await self(
            QueryOrder(
                symbol=symbol,
                order_id=order_id,
                orig_client_order_id=orig_client_order_id,
            ),
            credentials=credentials,
        )
