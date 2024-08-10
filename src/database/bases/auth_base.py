import json

from src.database.models import User, ManageTables
from sqlalchemy import insert, update, select

from src.routers.auth.core import decor
from auth2 import auth



class Checkers(ManageTables):
         
               
     @classmethod
     async def check_name(cls, name: str) -> None | str:
          async with cls.session() as conn:
               sttm = select().add_columns(User.name).where(User.name == name)
               
               result = await conn.execute(sttm)
               return result.scalar()


     
     @classmethod
     async def check_password(cls, name: str, password: str) -> bool | None:
          async with cls.session() as conn:
               sttm = select().add_columns(User.password).where(User.name == name)
                    
               result = await conn.execute(sttm)
               if result.scalar() == password:
                    return True
               return None
     



class Registration(ManageTables):
     ch = Checkers()
     
     
     @classmethod
     async def insert_new_data(cls, data: dict[str, str]) -> bool:
          async with cls.session.begin() as conn:
               if not await cls.ch.check_name(data.get('name')):
                    sttm = (
                         insert(User).
                         values(
                              name=data.get('name'), 
                              password=data.get('password'), 
                              orders=json.dumps([]),
                              money=10
                         )
                    )
                    await conn.execute(sttm)
                    return True
               return False
          
          
          
          
     @classmethod
     async def add_items(cls, data: dict) -> None:
          async with cls.session.begin() as conn:
               sttm = select(User.orders).where(User.na)
          
          
regstr = Registration()
check = Checkers()