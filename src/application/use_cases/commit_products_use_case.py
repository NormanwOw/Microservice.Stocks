from src.application.ports.logger import ILogger
from src.application.ports.services import IOrderService
from src.application.ports.uow import IUnitOfWork
from src.config import SERVICE_NAME
from src.domain.entities import Product
from src.domain.enums import EventType
from src.domain.exceptions import (
    DomainException,
    NotEnoughReserveProductsException,
    NotEnoughTotalProductsException,
)
from src.infrastructure.messaging.messages import (
    CommitProductsMessage,
    FailedEventPayload,
    FailedMessage,
)
from src.infrastructure.models import StocksModel


class CommitProducts:
    def __init__(self, order_service_proxy: IOrderService, logger: ILogger):
        self.order_service_proxy = order_service_proxy
        self.logger = logger

    async def __call__(self, uow: IUnitOfWork, message: CommitProductsMessage):
        products = message.payload.products
        stocks = await uow.stocks.find_total(products, with_for_update=True)

        if not stocks:
            await self.fail(
                uow=uow,
                message=message,
                error_message='Products not found or not available',
            )
            return

        try:
            committed_products = await self.commit(stocks, products)
        except DomainException as ex:
            await self.fail(
                uow=uow,
                message=message,
                error_message=ex.error_message,
            )
            return

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

    async def fail(
        self,
        uow: IUnitOfWork,
        message: CommitProductsMessage,
        error_message: str,
    ):
        failed_message = FailedMessage(
            action=EventType.COMMIT_FAILED,
            producer=SERVICE_NAME,
            external_reference=message.external_reference,
            payload=FailedEventPayload(
                failed_event=EventType.PRODUCTS_COMMITTED, error_message=error_message
            ),
        )

        await self.order_service_proxy.action_failed(uow, failed_message)

        self.logger.warning(
            f'{error_message} | Products: {message.payload.products}, '
            f'Command message id: {message.message_id}'
        )
