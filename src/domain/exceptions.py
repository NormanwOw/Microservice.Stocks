from uuid import UUID


class DomainException(Exception):
    error_message: str


class NotEnoughReserveProductsException(DomainException):
    def __init__(self, product_id: UUID, product_qty: int, reserved: int) -> None:
        self.product_id = product_id
        self.product_qty = product_qty
        self.reserved = reserved
        self.error_message = 'Not enough reserve products'


class NotEnoughTotalProductsException(DomainException):
    def __init__(self, product_id: UUID, product_qty: int, total: int) -> None:
        self.product_id = product_id
        self.product_qty = product_qty
        self.total = total
        self.error_message = 'Not enough total products'
