from src.application.ports.uow import IUnitOfWork
from src.infrastructure.messaging.messages import CancelReserveProductsMessage
from src.infrastructure.models import StocksModel


class CancelReserveProducts:
    async def __call__(self, uow: IUnitOfWork, message: CancelReserveProductsMessage) -> None:
        products = message.payload.products
        stocks: list[StocksModel] = await uow.stocks.find_by_products(
            products, with_for_update=True
        )
        if not stocks:
            return

        for stock in stocks:
            for product in products:
                if stock.product_id != product.id:
                    continue

                stock.reserved -= product.quantity
                stock.available += product.quantity
