

from fastapi import Request, APIRouter, Depends, HTTPException, Response

from auth2 import auth
from src.database.bases.auth_base import regstr



router = APIRouter(tags=['Data About User'])


async def depend_return_my_data(request: Request, response: Response) -> dict:
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     return await regstr.return_data_about_user(status['sub'])
     



async def depend_get_user(user_name: str) -> dict:
     get = await regstr.return_data_about_user(user_name)
     
     if isinstance(get, dict):
          return get
     raise HTTPException(status_code=444, detail='User was not found!')
     


@router.get('/api/me/')
async def return_my_data(returned = Depends(depend_return_my_data)):
     return returned



@router.get('/api/user/')
async def get_user(returned = Depends(depend_get_user)):
     return returned