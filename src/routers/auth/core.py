
import email_validator as em_v

from string import ascii_letters
from fastapi import HTTPException



class Decors:
     letters = ascii_letters + ' йцукенгшщзхъфывапролджэячсмитьбю' + ' 1234567890'
     
     
     @classmethod
     async def registration_name(cls, arg: str) -> bool:
          if len(arg.strip(cls.letters.replace(' ', ''))) != 0:
               raise HTTPException(status_code=441, detail='In username must be only letters and numbers!')
          return True
     
     
           
     
decor = Decors()