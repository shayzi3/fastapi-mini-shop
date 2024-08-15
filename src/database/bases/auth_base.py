import json

from fastapi import HTTPException

from src.database.models import User, ManageTables
from sqlalchemy import insert, update, select
from auth2 import auth



class Checkers(ManageTables):
         
               
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
                    hasher = await auth.check_password_hash(
                         plain_text_password=password,
                         hashed_password=result
                    )
                    return hasher
               return False
          
 


class Registration(ManageTables):
     ch = Checkers()
     
     
     @classmethod
     async def insert_new_data(cls, data: dict[str, str]) -> bool:
          async with cls.session.begin() as conn:
               if not await cls.ch.check_name(data.get('name')):
                    hash_pass = await auth.get_hashed_password(data.get('password'))
                    
                    sttm = (
                         insert(User).
                         values(
                              name=data.get('name'), 
                              password=hash_pass.decode(), 
                              money=100,
                              email=data.get('email'),
                              storage=json.dumps({})
                         )
                    )
                    await conn.execute(sttm)
                    return True
               return False
          
          
     @classmethod
     async def return_data_about_user(cls, username: str) -> dict | None:
          async with cls.session() as conn:
               sttm = select(User).where(User.name == username)
               
               result = await conn.execute(sttm)
               result = result.scalar()
               
               if result:
                    return {
                         'status': 208,
                         'detail': {
                              'name': result.name,
                              'email': result.email,
                              'money': result.money,
                              'storage': json.loads(result.storage)
                         }
                    }
               return None
          
          
     @classmethod
     async def save_new_password(cls, name: str, new_password: str) -> dict:
          async with cls.session.begin() as conn:
               hash_pass = await auth.get_hashed_password(new_password)
               
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(password=hash_pass.decode())
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
               
          
          
          
regstr = Registration()
check = Checkers()