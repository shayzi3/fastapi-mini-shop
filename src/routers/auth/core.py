
from string import ascii_letters



class Decors:
     letters = ascii_letters + 'йцукенгшщзхъфывапролджэячсмитьбю'
     
     
     @classmethod
     async def registration_name(cls, arg: str):
          if len(arg.strip(cls.letters)) != 0:
               return {
                    'status': 404, 
                    'message': 'In username must be only letters!'
               }
               
          return True
               
     
decor = Decors()