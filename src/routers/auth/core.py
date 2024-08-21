from string import ascii_letters
from fastapi import HTTPException

from src.database.bases.auth_base import check, regstr
from src.routers.auth.schemas import NewEmail, NewPassword


class Helper:
     letters = ascii_letters + ' йцукенгшщзхъфывапролджэячсмитьбю' + ' 1234567890' + 'йцукенгшщзхъфывапролджэячсмитьбю'.upper()
     
     
     @classmethod
     async def check_registration_name(cls, arg: str) -> None:
          if len(arg.strip(cls.letters.replace(' ', ''))) != 0:
               raise HTTPException(status_code=441, detail='In username must be only letters and numbers!')
          
          
     @staticmethod
     async def changers_code_passwords(token: dict, data: NewPassword) -> dict:
          ps = await check.check_password(
               name=token.get('sub'),
               password=data.password
          )
          if ps:
               return await regstr.save_new_password(
                    name=token.get('sub'),
                    new_password=data.new_password
               )
          raise HTTPException(status_code=445, detail='Invalid password!')
     
     
     
     @staticmethod
     async def changers_code_email(token: dict, data: NewEmail) -> dict:
          ps = await check.check_password(
               name=token.get('sub'),
               password=data.password
          )
          if ps:
               return await regstr.save_new_email(
                    name=token.get('sub'),
                    new_email=data.email
               )
          raise HTTPException(status_code=445, detail='Invalid password!')
               
     
     
           
     
helper = Helper()