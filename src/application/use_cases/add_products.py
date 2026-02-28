from src.infrastructure.models import ProductsModel, StocksModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import AddProductSchema


class AddProducts:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, products: list[AddProductSchema]):
        async with self.uow:
            for product in products:
                new_product = ProductsModel(
                    name=product.name,
                    price=product.price,
                    currency=product.currency,
                )
                new_stock = StocksModel(
                    available=product.quantity,
                    total=product.quantity,
                    reserved=0,
                    product=new_product,
                )
                await self.uow.stocks.add(new_stock)

            await self.uow.commit()
