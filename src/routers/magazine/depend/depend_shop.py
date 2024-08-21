

from typing import Annotated
from fastapi import Depends, HTTPException


from src.database.bases.shop_base import shopping, user_shop
from src.auth2 import auth



async def depend_get_items(item: Annotated[dict | None, Depends(shopping.get_one_item_)]):
     if isinstance(item, tuple):
          raise HTTPException(status_code=446, detail='Invalid item!')
     
     if not item:
          return await shopping.get_all_items()
     
     return item



async def depend_add_item_to_user(
     item_id: int, 
     token: Annotated[dict, Depends(auth.check_refresh_and_access_tokens)],
     item: Annotated[int, Depends(shopping.get_one_item_)],
     q: int = 1
     
) -> dict:
     
     if item:
          response = await shopping.check_quantity(q, item_id)
          
          if not response: 
               raise HTTPException(status_code=447, detail='Invalid quantity!')
          
          item[item_id]['qua'] = q
          item[item_id]['price'] = q * item[item_id]['price']
          
          return await user_shop.update_storage_at_user(items=item, username=token.get('sub'), items_key=item_id)
     raise HTTPException(status_code=446, detail='Invalid item!')



async def depend_del_item_at_user(
     items_id: list[int],
     token: Annotated[dict,  Depends(auth.check_refresh_and_access_tokens)],

) -> dict:
     
     return await user_shop.check_quantity_at_user(
          items_id=items_id,
          username=token.get('sub')
     )