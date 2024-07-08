import asyncio

from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Text

from config import secret


typeNAME = Annotated[str, mapped_column(primary_key=True, nullable=False)]
typeSTR = Annotated[str, mapped_column(nullable=False)]
typeTEXT = Annotated[str, mapped_column(Text, nullable=False)]



class Base(AsyncAttrs, DeclarativeBase):
     pass



class User(Base):
     __tablename__ = 'users'
     
     name: Mapped[typeNAME]
     password: Mapped[typeSTR]
     orders: Mapped[typeTEXT]
     status: Mapped[typeSTR]
     
     
     
     
class Order(Base):
     __tablename__ = 'orders'
     
     orders: Mapped[typeTEXT]
     orders_names: Mapped[typeTEXT]
     
     
     

class ManageTables:
     eng = create_async_engine(secret.get_postgresql_url(), echo=True)
     session = async_sessionmaker(eng)
     
     
     @classmethod
     async def create_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.create_all)
               
               
     @classmethod
     async def drop_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.drop_all)
               
               
               
               
async def startUp() -> None:
     manage = ManageTables()
     await manage.create_tables()
     # await manage.drop_tables()
     
     
if __name__ == '__main__':
     asyncio.run(startUp())
