from fastapi import APIRouter
from fastapi.params import Depends

from src.application.use_cases.get_products_use_case import GetProducts
from src.config import VERSION
from src.domain.entities import Product
from src.presentation.dependencies.product_dependencies import ProductDependencies

router = APIRouter(prefix=f'/api/v{VERSION}/products', tags=['Products'])


@router.get(path='', summary='Получение товаров', status_code=200)
async def get_products_endpoint(
    get_products: GetProducts = Depends(ProductDependencies.get_products),
) -> list[Product]:
    return await get_products()
