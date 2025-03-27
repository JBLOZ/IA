from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Producto(Base):
    __tablename__ = "products"  # Debe coincidir EXACTAMENTE con la tabla en MariaDB

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))  # TEXT en SQL puede ser String grande
    precio = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)