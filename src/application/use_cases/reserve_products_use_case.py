from src.application.ports.logger import ILogger
from src.application.ports.services import IOrderService
from src.application.ports.uow import IUnitOfWork
from src.domain.entities import Product
from src.infrastructure.messaging.messages import ReserveProductsMessage
from src.infrastructure.models import StocksModel


class ReserveProducts:
    def __init__(self, order_service_proxy: IOrderService, logger: ILogger):
        self.order_service_proxy = order_service_proxy
        self.logger = logger

    async def __call__(
        self, uow: IUnitOfWork, message: ReserveProductsMessage
    ) -> list[Product] | None:
        products = message.payload.products
        stocks = await uow.stocks.find_available(products, with_for_update=True)
        if not stocks:
            error_message = 'Products not found or not available'
            await self.order_service_proxy.reserve_failed(
                uow=uow, error_message=error_message, external_reference=message.external_reference
            )
            self.logger.warning(
                error_message + f' | Products: {products}, '
                f'Command message id: {message.message_id}'
            )
            return
        reserved_products = await self.reserve(stocks, products)
        await self.order_service_proxy.products_reserved(
            uow, reserved_products, message.external_reference
        )
        return reserved_products

    async def reserve(self, stocks: list[StocksModel], products: list[Product]) -> list[Product]:
        reserved_products = []
        for stock in stocks:
            if not stock.available:
                continue
            for product in products:
                if stock.product_id != product.id:
                    continue

                reserved = (
                    product.quantity if product.quantity <= stock.available else stock.available
                )
                product.quantity = reserved
                product.price = stock.product.price
                product.name = stock.product.name
                stock.available -= reserved
                stock.reserved += reserved
                reserved_products.append(product)
                break

        return reserved_products
