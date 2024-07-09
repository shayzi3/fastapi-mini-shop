

from typing import Any
from fastapi import APIRouter

from src.database.models import User, ManageTables
from src.database.base import data_help
from src.routers.auth.schemas import Registration, ChangeName, ChangePassword
from src.routers.auth.core import decor


router = APIRouter(tags=['Register'])


@router.post('/reg/')
async def register_user(data: Registration):
     name = await decor.registration_name(arg=data.name)
     if isinstance(name, dict):
          return name
     
     insert = await data_help.insert_new_data(data=data.model_dump())
     if insert:
          return {
               'status': 200, 
               'message': 'You success create new account!'
          }
          
     return {
          'status': 404,
          'message': 'This name already taken!'
     }
     
     

@router.post('/change_name/')
async def change_user_name(data: ChangeName):
     result = await data_help.change_nickname(data=data.model_dump())
     
     if result:
          return {'status': 200, 'message': f'Your name now {data.new_name}'}
     
     
     elif result == False:
          return {'status': 404, 'message': 'Invalid password!'}
     
     
     elif result == None:
          return {'status': 404, 'message': 'Invalid nickname!'}

