import json
from typing import Any

from src.database.models import User, Order, ManageTables
from sqlalchemy import insert, update, select



class Checkers(ManageTables):
         
               
     @classmethod
     async def check_name(cls, name: str) -> None | str:
          async with cls.session() as conn:
               sttm = select().add_columns(User.name).where(User.name == name)
               
               result = await conn.execute(sttm)
               return result.scalar()


     
     @classmethod
     async def check_password(cls, name: str, password: str) -> bool | None:
          if await cls.check_name(name):
               async with cls.session() as conn:
                    sttm = select().add_columns(User.password).where(User.name == name)
                    
                    result = await conn.execute(sttm)
                    if result.scalar() == password:
                         return True
                    return False
          return None



class DataHelper(ManageTables):
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
     async def change_nickname(cls, data: dict) -> bool:
          async with cls.session.begin() as conn:
               res = await cls.ch.check_password(
                    name=data.get('name'), 
                    password=data.get('password')
               )
               
               if res:
                    sttm = (
                         update(User).
                         where(User.password == data.get('password')).
                         values(name=data.get('new_name'))
                    )
                    await conn.execute(sttm)
                    return True
               return res
               
          
               
               
data_help = DataHelper()