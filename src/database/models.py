import json

from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Text, insert

from config import secret


typeNAME = Annotated[str, mapped_column(primary_key=True, nullable=False)]
typeSTR = Annotated[str, mapped_column(nullable=False)]
typeTEXT = Annotated[str, mapped_column(Text, nullable=True)]
typeORDERS = Annotated[str, mapped_column(Text, primary_key=True)]
typeMONEY = Annotated[int, mapped_column(nullable=True)]



class Base(AsyncAttrs, DeclarativeBase):
     pass



class User(Base):
     __tablename__ = 'users'
     
     name: Mapped[typeNAME]
     password: Mapped[typeSTR]
     orders: Mapped[typeTEXT]
     money: Mapped[typeMONEY]
     
     
     
class Order(Base):
     __tablename__ = 'orders'
     
     orders: Mapped[typeORDERS]
     
     
     
     

class ManageTables:
     __url = f'postgresql+asyncpg://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}'
     
     eng = create_async_engine(__url, echo=True)
     session = async_sessionmaker(eng)
     
     
     @classmethod
     async def create_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.create_all)
               
               
     @classmethod
     async def drop_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.drop_all)
               
               
     @classmethod
     async def new_items_in_order(cls) -> None:
          # q - quantity banana
          
          items = [
               {'Banana': {'price': 10, 'q': 5}},
               {'Apple': {'price': 8, 'q': 3}},
               {'Cherry': {'price': 2, 'q': 6}}
          ]
          
          async with cls.session.begin() as begin:
               sttm = (
                    insert(Order).
                    values(
                         orders=json.dumps(items)
                    )
               )
               await begin.execute(sttm)
          
          
               
               
               
               
async def startUp() -> None:
     manage = ManageTables()
     # await manage.create_tables()
     # await manage.drop_tables()
     await manage.new_items_in_order()
