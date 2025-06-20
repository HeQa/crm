import asyncio
from tortoise import Tortoise
from config import TORTOISE_ORM
from database.models import ClientStatuses

async def main():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    # await ClientStatuses.all().delete()
    # statuses = await ClientStatuses.all()
    # print([s.id for s in statuses])
    statuses = [
        {"id": 1, "name": "Новый", "source": "system"},
        {"id": 2, "name": "Горячий", "source": "system"},
        {"id": 3, "name": "В работе", "source": "system"},
        {"id": 4, "name": "Успешно", "source": "system"},
        {"id": 5, "name": "Отказ", "source": "system"},
    ]
    
    for status in statuses:
        await ClientStatuses.get_or_create(**status)
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())