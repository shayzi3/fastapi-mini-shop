
from random import randint
from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger, Text, insert

from config import secret


typeNAME = Annotated[str, mapped_column(primary_key=True, nullable=False)]
typeEMAIL = Annotated[str, mapped_column(nullable=False)]
typeID = Annotated[int, mapped_column(BigInteger, primary_key=True, unique=True)]
typeITEM = Annotated[str, mapped_column(nullable=False)]
typeSELLER = Annotated[str, mapped_column(nullable=False)]


typeTEXT = Annotated[str, mapped_column(Text, nullable=True)]
typeINT = Annotated[int, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
     pass



class User(Base):
     __tablename__ = 'users'
     
     name: Mapped[typeNAME]
     password: Mapped[typeTEXT]
     money: Mapped[typeINT]
     email: Mapped[typeEMAIL]
     storage: Mapped[typeTEXT]
     
     
     
class Order(Base):
     __tablename__ = 'orders'
     
     id: Mapped[typeID]
     item: Mapped[typeITEM]
     price: Mapped[typeINT]
     qua: Mapped[typeINT]         
     
     

class ManageTables:
     __url = f'postgresql+asyncpg://{secret.DB_USER}:{secret.DB_PASS}@{secret.DB_HOST}:{secret.DB_PORT}/{secret.DB_NAME}'
     
     eng = create_async_engine(__url)
     session = async_sessionmaker(eng)
     
     
     @classmethod
     async def _create_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.create_all)
               
               
     @classmethod
     async def _drop_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.drop_all)
               
               
     @classmethod
     async def new_items_in_order(cls) -> None:
          # q - quantity banana
          
          items = [
               ('Banana', 10, 5),
               ('Apple', 4, 2),
               ('Cherry', 2, 4)
          ]
          
          async with cls.session.begin() as begin:
               for item in items:
                    sttm = (
                         insert(Order).
                         values(
                              item=item[0],
                              price=item[1],
                              qua=item[2],
                              id=randint(10, 1000)
                         )
                    )
                    await begin.execute(sttm)
          
          
               
               
               
               
async def startUp() -> None:
     manage = ManageTables()
     await manage._drop_tables()
     await manage._create_tables()
     await manage.new_items_in_order()
