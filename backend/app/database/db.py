from tortoise.contrib.fastapi import register_tortoise
from app.config import config, TORTOISE_ORM
import asyncpg
from tortoise import Tortoise


async def ensure_db_exists(db_url: str):
    """Автоматически создаёт базу данных, если её нет."""
    # Парсим URL, чтобы получить имя БД (например, 'postgres://user:pass@host:5432/dbname')
    db_name = db_url.split("/")[-1].split("?")[0]  # Извлекаем 'dbname'

    # Подключаемся к стандартной БД 'postgres' для создания новой БД
    temp_url = db_url.replace(db_name, "postgres")

    try:
        conn = await asyncpg.connect(temp_url)
        await conn.execute(f"CREATE DATABASE {db_name}")
        print(f"✅ База данных '{db_name}' создана")
        await conn.close()
    except asyncpg.DuplicateDatabaseError:
        print(f"🔹 База данных '{db_name}' уже существует")
    except Exception as e:
        print(f"❌ Ошибка при создании БД: {e}")

async def init_tortoise():
    """Явная инициализация Tortoise"""
    await Tortoise.init(
        config=TORTOISE_ORM
    )
    await Tortoise.generate_schemas()
    print("🟢 Таблицы созданы")

async def close_db():
    await Tortoise.close_connections()
    print("🔴 Соединения с базой закрыты")

def init_db(app):
    register_tortoise(
        app,
        db_url=config.DATABASE_URL,
        modules={"app": ["app.database.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


if __name__ == '__main__':
    import asyncio
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    # Создаём временное FastAPI приложение для инициализации
    app = FastAPI()
    
    # Запускаем проверку и создание БД
    asyncio.run(ensure_db_exists(config.DATABASE_URL))

    asyncio.run(init_tortoise())

    # Инициализируем Tortoise
    init_db(app)

    print("🟢 База данных инициализирована")