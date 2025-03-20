from adaptix import NameStyle, Retort, name_mapping

from aiomexc.methods import MexcMethod, QueryOrder
from aiomexc.types import Order, AccountInformation, TickerPrice

type_recipes = [
    name_mapping(
        mexc_type,
        name_style=NameStyle.CAMEL,
    )
    for mexc_type in [
        Order,
        AccountInformation,
        TickerPrice,
    ]
]

_retort = Retort(
    recipe=[
        name_mapping(
            MexcMethod,
            name_style=NameStyle.CAMEL,
            omit_default=True,
        ),
        name_mapping(
            QueryOrder,
            name_style=NameStyle.CAMEL,
            omit_default=True,
        ),
    ]
    + type_recipes,
)

__all__ = ["_retort"]
