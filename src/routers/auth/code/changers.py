

from fastapi import APIRouter, HTTPException, Request, Depends, Response

from auth2 import auth
from src.routers.auth.schemas import NewPassword, NewEmail, NewName
from src.database.bases.auth_base import check, regstr
from src.routers.auth.core import decor


router = APIRouter(tags=['Change UserData'])


async def depend_password_change(data: NewPassword, request: Request, response: Response) -> dict:
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     ps = await check.check_password(
          name=status['sub'],
          password=data.password
     )
     if ps:
          return await regstr.save_new_password(
               name=status['sub'],
               new_password=data.new_password
          )
     raise HTTPException(status_code=445, detail='Invalid password!')



async def depend_email_change(data: NewEmail, request: Request, response: Response) -> dict:
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     ps = await check.check_password(
          name=status['sub'],
          password=data.password
     )
     if ps:
          return await regstr.save_new_email(
               name=status['sub'],
               new_email=data.email
          )
     raise HTTPException(status_code=445, detail='Invalid password!')




async def depend_name_change(data: NewName, request: Request, response: Response) -> dict:
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     await decor.registration_name(
          arg=data.new_name
     )
     ps = await check.check_password(
          name=status['sub'],
          password=data.password
     )
     if ps:
          await auth.get_access_refresh_tokens(
               username=data.new_name, 
               response=response
          )
          return await regstr.save_new_name(
               name=status['sub'],
               new_name=data.new_name
          )
     raise HTTPException(status_code=445, detail='Invalid password!')
     



@router.post('/api/change_password/')
async def password_change(returned = Depends(depend_password_change)):
     return returned



@router.post('/api/change_email/')
async def email_change(returned = Depends(depend_email_change)):
     return returned



@router.post('/api/change_name/')
async def name_change(returned = Depends(depend_name_change)):
     return returned