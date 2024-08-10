

from fastapi import APIRouter, Request, Response, Depends, HTTPException

from src.database.bases.auth_base import regstr, check
from src.routers.auth.schemas import Reg, Auth
from src.routers.auth.core import decor
from auth2 import auth



router = APIRouter(tags=['Register'])


async def depend_register_user(data: Reg, response: Response):
     '''
          Errors:
          
          In username must be only accessed symbols! status_name 460
          Username 3 - 15 letters or numbers. validation routers/auth/schemas.py
          Password 8 - 20 symbols. validation. routers/auth/schemas.py
          This name already taken! insert 170
     '''
     await decor.registration_name(arg=data.name)
     
     insert = await regstr.insert_new_data(data=data.model_dump())
     if insert:
          token = auth.encode_token(data.name)
          response.set_cookie(
               key='access_token', 
               value=token,
               httponly=True
          )
          return {'access_token': token, 'refresh_token': None}
     
     raise HTTPException(status_code=170, detail='This name already taken!')




async def depend_auth(data: Auth, response: Response):
     '''
          Errors:
          
          In username must be only accessed symbols! auth/core.py 460
          Username 3 - 15 letters or numbers. validation routers/auth/schemas.py
          Password 8 - 20 symbols. validation. routers/auth/schemas.py
          Invalid name or password. passw 50
     '''
     
     await decor.registration_name(arg=data.name)
     
     passw = await check.check_password(
          name=data.name,
          password=data.password
     )
     if not passw:
          raise HTTPException(status_code=50, detail='Invalid name or password!')
     
     token = auth.encode_token(data.name)
     response.set_cookie(
          key='access_token', 
          value=token,
          httponly=True
     )
     return {'access_token': token, 'refresh_token': None}
     
     
     
     
async def depend_out_user(response: Response):
     response.set_cookie(key='access_token', value='')
     return {'status': 550, 'access_token': None}




@router.post('/reg/')
async def register_user(returned = Depends(depend_register_user)):
     return returned


@router.post('/auth/')
async def auth_user(returned = Depends(depend_auth)):
     return returned


@router.get('/out/')
async def out_user(returned = Depends(depend_out_user)):
     return returned




     

