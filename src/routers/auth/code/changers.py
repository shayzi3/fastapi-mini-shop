

from fastapi import APIRouter, Request, Depends, Response

from auth2 import auth
from src.routers.auth.schemas import NewPassword, NewEmail, NewName
from src.database.bases.auth_base import check, regstr



router = APIRouter(tags=['Change UserData'])


async def depend_password_change(data: NewPassword, request: Request):
     access_token = request.cookies.get('access_token')
     decode = auth.decode_token(access_token)
     
     ps = await check.check_password(
          name=decode['sub'],
          password=data.password
     )
     if ps:
          await regstr.save_new_password(
               name=decode['sub'],
               new_password=data.new_password
          )
          return {'status': 0, 'detail': 'Password changed success!'}
     
     return {'status': 1, 'detail': 'Invalid password!'}



async def depend_email_change(data: NewEmail, request: Request):
     access_token = request.cookies.get('access_token')
     decode = auth.decode_token(access_token)
     
     ps = await check.check_password(
          name=decode['sub'],
          password=data.password
     )
     if ps:
          await regstr.save_new_email(
               name=decode['sub'],
               new_email=data.email
          )
          return {'status': 3, 'detail': 'Email changed success!'}
     
     return {'status': 2, 'detail': 'Invalid password!'}



async def depend_name_change(data: NewName, request: Request, response: Response):
     access_token = request.cookies.get('access_token')
     decode = auth.decode_token(access_token)
     
     ps = await check.check_password(
          name=decode['sub'],
          password=data.password
     )
     if ps:
          await regstr.save_new_name(
               name=decode['sub'],
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
     



@router.post('/change_password/')
async def password_change(returned = Depends(depend_password_change)):
     return returned



@router.post('/change_email/')
async def email_change(returned = Depends(depend_email_change)):
     return returned



@router.post('/change_name/')
async def name_change(returned = Depends(depend_name_change)):
     return returned