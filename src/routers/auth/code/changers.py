

from fastapi import APIRouter, Request, Depends, Response

from auth2 import auth
from src.routers.auth.schemas import NewPassword, NewEmail, NewName
from src.database.bases.auth_base import check, regstr



router = APIRouter(tags=['Change UserData'])


async def depend_password_change(data: NewPassword, request: Request, response: Response):
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
          await regstr.save_new_password(
               name=status['sub'],
               new_password=data.new_password
          )
          return {'status': 0, 'detail': 'Password changed success!'}
     return {'status': 1, 'detail': 'Invalid password!'}



async def depend_email_change(data: NewEmail, request: Request, response: Response):
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
          await regstr.save_new_email(
               name=status['sub'],
               new_email=data.email
          )
          return {'status': 3, 'detail': 'Email changed success!'}
     return {'status': 2, 'detail': 'Invalid password!'}



async def depend_name_change(data: NewName, request: Request, response: Response):
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
          await regstr.save_new_name(
               name=status['sub'],
               new_name=data.new_name
          )
               
          token = auth.encode_token(data.new_name)
          response.set_cookie(
               key='access_token',
               value=token,
               httponly=True
          )
          return {'status': 5, 'detail': 'Name changed success!'}
     return {'status': 4, 'detail': 'Invalid password!'}
     



@router.post('/api/change_password/')
async def password_change(returned = Depends(depend_password_change)):
     return returned



@router.post('/api/change_email/')
async def email_change(returned = Depends(depend_email_change)):
     return returned



@router.post('/api/change_name/')
async def name_change(returned = Depends(depend_name_change)):
     return returned