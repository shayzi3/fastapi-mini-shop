
from typing import Annotated
from fastapi import APIRouter, Depends

from src.routers.auth.depend.depend_changers import (
     depend_name_change
)
from src.routers.auth.schemas import NewPassword, NewEmail
from src.auth2 import auth
from src.routers.auth.core import helper


router = APIRouter(tags=['Change UserData'], prefix='/api/v1')



@router.patch('/change_password')
async def password_change(
     data: NewPassword,
     token:  Annotated[dict, Depends(auth.check_refresh_and_access_tokens)],
     
) -> dict:
     
     return await helper.changers_code_passwords(token, data)



@router.patch('/change_email')
async def email_change(
     data: NewEmail,
     token:  Annotated[dict, Depends(auth.check_refresh_and_access_tokens)],
     
) -> dict:
     
     return await helper.changers_code_email(token, data)



@router.patch('/change_name')
async def name_change(returned: Annotated[dict, Depends(depend_name_change)]) -> dict:
     return returned