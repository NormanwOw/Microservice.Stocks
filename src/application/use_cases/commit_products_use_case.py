from src.application.ports.logger import ILogger
from src.application.ports.services import IOrderService
from src.application.ports.uow import IUnitOfWork
from src.domain.entities import Product
from src.domain.exceptions import NotEnoughReserveProductsException, NotEnoughTotalProductsException
from src.infrastructure.messaging.messages import CommitProductsMessage
from src.infrastructure.models import StocksModel


class CommitProducts:
    def __init__(self, order_service_proxy: IOrderService, logger: ILogger):
        self.order_service_proxy = order_service_proxy
        self.logger = logger

    async def __call__(self, uow: IUnitOfWork, message: CommitProductsMessage):
        products = message.payload.products
        stocks = await uow.stocks.find_total(products, with_for_update=True)
        if not stocks:
            error_message = 'Products not found or not available'
            await self.order_service_proxy.commit_failed(
                uow=uow, error_message=error_message, external_reference=message.external_reference
            )
            self.logger.warning(
                error_message + f' | Products: {products}, '
                f'Command message id: {message.message_id}'
            )
            return
        committed_products = await self.commit(stocks, products)
        await self.order_service_proxy.products_committed(
            uow, committed_products, message.external_reference
        )
        return committed_products

    async def commit(self, stocks: list[StocksModel], products: list[Product]) -> list[Product]:
        committed_products = []
        for stock in stocks:
            for product in products:
                if stock.product_id != product.id:
                    continue

                stock.reserved -= product.quantity
                if stock.reserved < 0:
                    raise NotEnoughReserveProductsException(
                        product_id=stock.product_id,
                        product_qty=product.quantity,
                        reserved=stock.reserved,
                    )
                stock.total -= product.quantity
                if stock.total < 0:
                    raise NotEnoughTotalProductsException(
                        product_id=stock.product_id, product_qty=product.quantity, total=stock.total
                    )
                committed_products.append(product)

        return committed_products
