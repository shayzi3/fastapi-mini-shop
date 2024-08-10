

from fastapi import Request, APIRouter, Depends, HTTPException

from auth2 import auth
from src.database.bases.auth_base import regstr



router = APIRouter(tags=['Data About User'])


async def depend_return_my_data(request: Request):
     jwt = request.cookies.get('access_token')
     
     decode = auth.decode_token(jwt)
     
     return await regstr.return_data_about_user(decode['sub'])



async def depend_get_user(user_name: str):
     get = await regstr.return_data_about_user(user_name)
     
     if isinstance(get, dict):
          return get
     raise HTTPException(status_code=301, detail='User was not found!')
     


@router.get('/me/')
async def return_my_data(returned = Depends(depend_return_my_data)):
     return returned



@router.get('/user/')
async def get_user(returned = Depends(depend_get_user)):
     return returned