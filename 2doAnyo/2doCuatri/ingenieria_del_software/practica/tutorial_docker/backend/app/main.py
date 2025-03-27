from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import engine, database, get_db
from app.models import Base, Producto

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "API conectada a MariaDB"}

@app.get("/productos/")
async def get_productos(db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(Producto))  # Ejecuta la consulta
        productos = result.scalars().all()  # Extrae los resultados

        print("Productos obtenidos:", productos)  # 🔍 Debugging
    return {"productos": productos}