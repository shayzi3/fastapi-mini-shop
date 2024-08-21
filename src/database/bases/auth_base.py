import json

from fastapi import HTTPException

from src.database.models import User, ManageTables
from sqlalchemy import insert, update, select, delete
from src.auth2 import hashed
from src.routers.auth.schemas import Reg
from src.database.bases.shop_base import user_shop



class DataCheckers(ManageTables):
         
               
     @classmethod
     async def check_name(cls, name: str) -> None | str:
          async with cls.session() as conn:
               sttm = select().add_columns(User.name).where(User.name == name)
               
               result = await conn.execute(sttm)
               return result.scalar()


     
     @classmethod
     async def check_password(cls, name: str, password: str) -> bool:
          async with cls.session() as conn:
               sttm = select(User.password).where(User.name == name)
               result = await conn.execute(sttm)
               
               result = result.scalar()
               
               if result:
                    hasher = await hashed.check_password_hash(
                         plain_text_password=password,
                         hashed_password=result
                    )
                    return hasher
               return False
          
 


class DataBase(ManageTables):
     ch = DataCheckers()
     
     
     @classmethod
     async def insert_new_data(cls, data: Reg) -> bool:
          async with cls.session.begin() as conn:
               name_exists =  await cls.ch.check_name(data.name)
               
               if not name_exists:
                    hash_pass = await hashed.get_hashed_password(data.password)
                    
                    sttm = (
                         insert(User).
                         values(
                              name=data.name, 
                              password=hash_pass, 
                              money=100,
                              email=data.email,
                              storage=json.dumps({})
                         )
                    )
                    await conn.execute(sttm)
                    return True
               return False
          
          
     @classmethod
     async def return_data_about_user(cls, name: str) -> dict | None:
          async with cls.session() as conn:
               sttm = select(User).where(User.name == name)
               
               result = await conn.execute(sttm)
               result = result.scalar()
               
               if result:
                    return {
                         'status': 208,
                         'detail': {
                              'name': result.name,
                              'email': result.email,
                              'money': result.money,
                              'storage': await user_shop.get_my_storage(name)
                         }
                    }
               return None
          
          
     @classmethod
     async def save_new_password(cls, name: str, new_password: str) -> dict:
          async with cls.session.begin() as conn:
               hash_pass = await hashed.get_hashed_password(new_password)
               
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(password=hash_pass)
               )
               await conn.execute(sttm)
          return {'status': 209,'detail': 'Password changed success!'}
          
               
     
     @classmethod
     async def save_new_email(cls, name: str, new_email: str) -> dict:
          async with cls.session.begin() as conn:
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(email=new_email)
               )
               await conn.execute(sttm)  
          return {'status': 210, 'detail': 'Email changed success!'}

               
          
     
     @classmethod
     async def save_new_name(cls, name: str, new_name: str) -> dict:
          async with cls.session.begin() as conn:
               if await cls.ch.check_name(new_name):
                    raise HTTPException(status_code=440, detail='This name already taken!')
                    
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(name=new_name)
               )
               await conn.execute(sttm)  
          return {'status': 211, 'detail': 'Name changed success!'}
     
     
     
     @classmethod
     async def delete_user_account(cls, name: str) -> dict:
          async with cls.session.begin() as conn:
               sttm = (
                    delete(User).
                    where(User.name == name)
               )
               await conn.execute(sttm)
          return {'status': 215, 'detail': 'Account deleted success!'}

               
          
          
          
regstr = DataBase()
check = DataCheckers()