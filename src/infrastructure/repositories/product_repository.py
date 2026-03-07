from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import IProductRepository
from src.infrastructure.models import ProductsModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository, IProductRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, ProductsModel)
