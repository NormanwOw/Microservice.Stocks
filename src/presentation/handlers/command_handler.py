from src.application.disp_depends import DispDepends
from src.application.dispatcher import dispatcher
from src.application.ports.uow import IUnitOfWork
from src.application.use_cases.commit_products_use_case import CommitProducts
from src.application.use_cases.reserve_products_use_case import ReserveProducts
from src.domain.enums import CommandType
from src.infrastructure.logger.impl import logger
from src.infrastructure.messaging.messages import CommitProductsMessage, ReserveProductsMessage
from src.presentation.dependencies.product_dependencies import ProductDependencies


@dispatcher.register(CommandType.RESERVE_PRODUCTS)
async def reserve_products_handler(
    uow: IUnitOfWork,
    message: dict,
    reserve_products: ReserveProducts = DispDepends(ProductDependencies.reserve_products),
):
    msg = ReserveProductsMessage(**message)
    reserved_products = await reserve_products(uow, msg)
    if reserved_products:
        logger.info(
            f'Successfully reserved products: {reserved_products}, '
            f'Command message id: {msg.message_id}'
        )


@dispatcher.register(CommandType.COMMIT_PRODUCTS)
async def commit_products_handler(
    uow: IUnitOfWork,
    message: dict,
    commit_products: CommitProducts = DispDepends(ProductDependencies.commit_products),
):
    msg = CommitProductsMessage(**message)
    committed_products = await commit_products(uow, msg)
    logger.info(
        f'Successfully committed products: {committed_products}, '
        f'Command message id: {msg.message_id}'
    )
