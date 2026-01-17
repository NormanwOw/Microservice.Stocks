from src.infrastructure.uow.interfaces import IUnitOfWork


class GetProducts:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self):
        async with self.uow:
            pass
