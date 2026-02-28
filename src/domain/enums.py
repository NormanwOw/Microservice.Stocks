from enum import Enum


class Currency(str, Enum):
    USD = 'USD'
    EUR = 'EUR'


class CommandType(str, Enum):
    RESERVE_PRODUCTS = 'ReserveProducts'
    COMMIT_PRODUCTS = 'CommitProducts'


class EventType(str, Enum):
    PRODUCTS_RESERVED = 'ProductsReserved'
    PRODUCTS_COMMITTED = 'ProductsCommitted'
    COMMIT_FAILED = 'CommitFailed'
    RESERVE_FAILED = 'ReserveFailed'


class AggregateType(str, Enum):
    ORDER = 'order'
