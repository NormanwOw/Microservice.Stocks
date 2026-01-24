from src.application.disp_depends import DispDepends
from src.application.dispatcher import dispatcher
from src.application.use_cases.reserve_products_use_case import ReserveProducts
from src.domain.enums import CommandType
from src.infrastructure.messaging.messages import ReserveProductsMessage
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.dependencies.product_dependencies import ProductDependencies


@dispatcher.register(CommandType.RESERVE_PRODUCTS)
async def reserve_products_handler(
    uow: IUnitOfWork,
    message: dict,
    reserve_products: ReserveProducts = DispDepends(ProductDependencies.reserve_products),
):
    msg = ReserveProductsMessage(**message)
    await reserve_products(uow, msg)
