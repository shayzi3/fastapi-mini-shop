

from fastapi import APIRouter, Request, Response, HTTPException, Depends

from auth2 import auth
from src.database.bases.shop_base import user_shop



router = APIRouter(tags=['Buy Item'])


async def depend_user_buy_items(item_id: str, request: Request, response: Response):
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     return await user_shop.bougt_item(item=item_id, username=status['sub'])


@router.post('/api/buy_item/{item_id}')
async def user_buy_items(returned = Depends(depend_user_buy_items)):
     return returned
     