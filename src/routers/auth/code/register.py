
from typing import Annotated
from fastapi import APIRouter, Depends

from src.auth2 import auth
from  src.routers.auth.depend.depend_register import(
     depend_auth_user,
     depend_delete_user,
     depend_register_user
)


router = APIRouter(tags=['Registration'], prefix='/api/v1')


@router.post('/reg')
async def register_user(returned: Annotated[dict, Depends(depend_register_user)]):
     return returned



@router.post('/auth')
async def auth_user(returned: Annotated[dict, Depends(depend_auth_user)]):
     return returned



@router.get('/out')
async def out_user(returned: Annotated[dict, Depends(auth.cookies_delete)]):
     return returned



@router.delete('/delete')
async def delete_user(returned: Annotated[dict, Depends(depend_delete_user)]):
     return returned




     

