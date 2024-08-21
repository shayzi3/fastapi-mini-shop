

from typing import Annotated
from fastapi import Depends

from src.auth2 import auth
from src.database.bases.shop_base import user_shop



async def depend_user_buy_items(
     item_id: int,
     token: Annotated[dict, Depends(auth.check_refresh_and_access_tokens)]
     
) -> dict:
     
     return await user_shop.bougt_item(item=item_id, username=token.get('sub'))