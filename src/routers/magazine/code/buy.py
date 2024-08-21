

from fastapi import APIRouter, Depends

from src.routers.magazine.depend.depend_buy import depend_user_buy_items



router = APIRouter(tags=['Buy Item'], prefix='/api/v1')


@router.post('/buy_item/{item_id}')
async def user_buy_items(returned = Depends(depend_user_buy_items)):
     return returned
     