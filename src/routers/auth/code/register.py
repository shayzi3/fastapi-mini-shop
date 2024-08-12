

from fastapi import APIRouter, Response, Depends, HTTPException

from src.database.bases.auth_base import regstr, check
from src.routers.auth.schemas import Reg, Auth
from src.routers.auth.core import decor
from auth2 import auth


router = APIRouter(tags=['Register'])


async def depend_register_user(data: Reg, response: Response):
     await decor.registration_name(arg=data.name)
     
     insert = await regstr.insert_new_data(data=data.model_dump())
     if insert:
          return await auth.get_access_refresh_tokens(
               username=data.name, 
               response=response
          )
     
     raise HTTPException(status_code=170, detail='This name already taken!')




async def depend_auth(data: Auth, response: Response):
     await decor.registration_name(arg=data.name)
     
     passw = await check.check_password(
          name=data.name,
          password=data.password
     )
     if passw is False:
          return {'status': 50, 'detail': 'Invalid name or password!'}

     return await auth.get_access_refresh_tokens(
          username=data.name,
          response=response
     )
     
     
     
     
async def depend_out_user(response: Response):
     response.delete_cookie(key='access_token', httponly=True)
     response.delete_cookie(key='refresh_token', httponly=True)
     
     return {'status': 550, 'access_token': None, 'refresh_token': None}



@router.post('/api/reg/')
async def register_user(returned = Depends(depend_register_user)):
     return returned



@router.post('/api/auth/')
async def auth_user(returned = Depends(depend_auth)):
     return returned



@router.get('/api/out/')
async def out_user(returned = Depends(depend_out_user)):
     return returned




     

