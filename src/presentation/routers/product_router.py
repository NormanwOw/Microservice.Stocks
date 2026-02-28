from fastapi import APIRouter, Response
from fastapi.params import Depends

from src.application.use_cases.add_products import AddProducts
from src.application.use_cases.get_products_use_case import GetProducts
from src.config import VERSION
from src.domain.entities import Product
from src.presentation.dependencies.product_dependencies import ProductDependencies
from src.presentation.pagination import Pagination
from src.presentation.schemas import AddProductSchema

router = APIRouter(prefix=f'/api/v{VERSION}/products', tags=['Products'])


@router.get(path='', summary='Получение товаров', status_code=200)
async def get_products_endpoint(
    pagination: Pagination = Depends(),
    get_products: GetProducts = Depends(ProductDependencies.get_products),
) -> list[Product]:
    return await get_products(pagination)


@router.post(path='', summary='Добавление товаров', status_code=201)
async def add_products(
    products: list[AddProductSchema],
    add_prods: AddProducts = Depends(ProductDependencies.add_products),
):
    await add_prods(products)
    return Response(status_code=201)
