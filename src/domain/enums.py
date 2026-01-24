from enum import Enum


class Currency(str, Enum):
    USD = 'USD'
    EUR = 'EUR'


class CommandType(str, Enum):
    RESERVE_PRODUCTS = 'ReserveProducts'


class EventType(str, Enum):
    PRODUCTS_RESERVED = 'ProductsReserved'
    RESERVE_FAILED = 'ReserveFailed'


class AggregateType(str, Enum):
    ORDER = 'order'
