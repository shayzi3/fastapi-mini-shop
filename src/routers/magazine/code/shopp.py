
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from src.database.bases.shop_base import shopping, user_shop
from auth2 import auth


router = APIRouter(tags=['Shop'])


async def depend_get_items(item_id: int = None):
     if item_id:
          res = await shopping.get_one_item_(item_id)
               
     else:
          return await shopping.get_all_items()
               
     if not res:
          raise HTTPException(status_code=355, detail='Invalid item!')
     return res



async def depend_add_item_to_user(
     item_id: int, 
     request: Request, 
     response: Response,
     q: int = 1
):
     res = await shopping.get_one_item_(item_id)
     
     if res:
          response = await shopping.check_quantity(q, item_id)
          
          if not response: 
               raise HTTPException(status_code=544, detail='Invalid quantity!')
          
          status = await auth.check_refresh_and_access_tokens(
               access_token=request.cookies.get('access_token'),
               refresh_token_=request.cookies.get('refresh_token'),
               response=response
          )
          
          res[item_id]['qua'] = q
          res[item_id]['price'] = q * res[item_id]['price']
          
          return await user_shop.update_storage_at_user(items=res, username=status['sub'], items_key=item_id)
     raise HTTPException(status_code=355, detail='Invalid item!')



async def depend_del_item_at_user(
     items_id: list[int],
     request: Request,
     response: Response,
     q: int = 1
):
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     return await user_shop.check_quantity_at_user(
          items_id=items_id,
          q=q,
          username=status['sub']
     )


async def depend_get_storage(request: Request, response: Response):
     status = await auth.check_refresh_and_access_tokens(
          access_token=request.cookies.get('access_token'),
          refresh_token_=request.cookies.get('refresh_token'),
          response=response
     )
     return await user_shop.get_my_storage(username=status['sub'])
     


@router.get('/api/items/')
async def get_items(returned = Depends(depend_get_items)):
     return returned



@router.post('/api/add_item/{item_id}')
async def add_item_at_user(returned = Depends(depend_add_item_to_user)):
     return returned



@router.post('/api/del_item/{item_id}')
async def del_item_at_user(returned = Depends(depend_del_item_at_user)):
     return returned



@router.get('/api/get_storage/')
async def get_user_storage(returned = Depends(depend_get_storage)):
     return returned
     






