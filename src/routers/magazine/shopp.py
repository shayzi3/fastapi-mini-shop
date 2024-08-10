
from fastapi import APIRouter

from src.database.bases.shop_base import shopping


router = APIRouter(tags=['Shop'])



@router.get('/items/')
async def get_items() -> None:
     return await shopping.get_all_items()



@router.get('/item/{item}')
async def get_one_item(item: str) -> None:
     res = await shopping.get_one_item_(item)
     
     if not res:
          return {'status': 115, 'message': 'Invalid item!'}
     return res



@router.post('/add_item/{item}')
async def add_item_to_user(item: str, q: int) -> None:
     res = await shopping.get_one_item_(item)
     
     if res:
          response = await shopping.check_quantity(q, item)
          
          if not response:
               return {'status': 54, 'message': 'Invalid quantity.'}
          
          res['q'] = q
          res['price'] = q * res['price']
          
          
     
     return res






