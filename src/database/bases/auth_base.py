import json

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
                              orders=json.dumps([]),
                              money=10,
                              email=data.get('email'),
                              storage=json.dumps([])
                         )
                    )
                    await conn.execute(sttm)
                    return True
               return False
          
          
     @classmethod
     async def return_data_about_user(cls, username: str) -> dict:
          async with cls.session() as conn:
               sttm = select(User.name, User.email).where(User.name == username)
               
               result = await conn.execute(sttm)
               result = result.all()
               
               if result:
                    return {
                         'status': 700,
                         'detail': {
                              'name': result[0][0],
                              'email': result[0][1]
                         }
                    }
               return None
          
          
     @classmethod
     async def save_new_password(cls, name: str, new_password: str):
          async with cls.session.begin() as conn:
               hash_pass = await auth.get_hashed_password(new_password)
               
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(password=hash_pass.decode())
               )
               await conn.execute(sttm)
               
     
     @classmethod
     async def save_new_email(cls, name: str, new_email: str):
          async with cls.session.begin() as conn:
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(email=new_email)
               )
               await conn.execute(sttm)  
          
     
     @classmethod
     async def save_new_name(cls, name: str, new_name: str):
          async with cls.session.begin() as conn:
               sttm = (
                    update(User).
                    where(User.name == name).
                    values(name=new_name)
               )
               await conn.execute(sttm)  
          
          
regstr = Registration()
check = Checkers()