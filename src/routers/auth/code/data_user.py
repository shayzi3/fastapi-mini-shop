
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException


from src.auth2 import auth
from src.database.bases.auth_base import regstr


router = APIRouter(tags=['Data About User'], prefix='/api/v1')


@router.get('/me')
async def return_my_data(token: Annotated[dict, Depends(auth.check_refresh_and_access_tokens)]):
     return await regstr.return_data_about_user(token.get('sub'))



@router.get('/user')
async def get_user(about_user: Annotated[dict | None, Depends(regstr.return_data_about_user)]):
     if isinstance(about_user, dict):
          return about_user
     raise HTTPException(status_code=444, detail='User was not found!')