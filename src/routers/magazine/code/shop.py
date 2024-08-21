
from typing import Annotated
from fastapi import APIRouter, Depends

from src.routers.magazine.depend.depend_shop import (
     depend_add_item_to_user,
     depend_del_item_at_user,
     depend_get_items
)
from src.database.bases.shop_base import user_shop
from src.auth2 import auth


router = APIRouter(tags=['Shop'], prefix='/api/v1')


@router.get('/items')
async def get_items(returned: Annotated[dict, Depends(depend_get_items)]):
    return returned


@router.post('/add_item/{item_id}')
async def add_item_at_user(returned: Annotated[dict, Depends(depend_add_item_to_user)]):
     return returned



@router.delete('/del_item')
async def del_item_at_user(returned: Annotated[dict, Depends(depend_del_item_at_user)]):
     return returned



@router.get('/get_storage')
async def get_user_storage(token:  Annotated[str, Depends(auth.check_refresh_and_access_tokens)]):
     return await user_shop.get_my_storage(username=token.get('sub'))

     






