from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
import os

DATABASE_URL = "mysql+asyncmy://root:root@database:3306/tienda"

# Crear el motor de conexión asíncrono
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Crear la sesión de la base de datos
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Conexión usando databases
database = Database(DATABASE_URL)

async def get_db():
    async with async_session() as session:
        yield session