import json
from typing import Any

from sqlalchemy import select, update, text

from src.database.models import Order, User, ManageTables


class Shopping(ManageTables):
     
     
     @classmethod
     async def get_all_items(cls) -> list[dict]:
          async with cls.session() as conn:
               sttm = text('SELECT * FROM orders')
               response = await conn.execute(sttm)
               
               items = {}
               for data in response.fetchall():
                    items[data[0]] = {
                         'name': data[1],
                         'price': data[2],
                         'qua': data[3]
                    }
               return items
          
               
          
     @classmethod
     async def get_one_item_(cls, item_id: int) -> dict:
          async with cls.session() as conn:
               sttm = select(Order).where(Order.id == item_id)
               response = await conn.execute(sttm)
               
               result = response.scalar()
               if result:
                    items = {
                         result.id: {
                              'price': result.price,
                              'qua': result.qua,
                              'name': result.item
                         }
                    }
                    return items
               return None
          
          
          
     @classmethod
     async def check_quantity(cls, q: int, item_id: int) -> None:
          async with cls.session() as conn:
               sttm = select(Order.qua).where(Order.id == item_id)
               response = await conn.execute(sttm)
               
               quantity = response.scalar()               
               if q <= quantity and q >= 1:
                    return True
               return None
           
          
          
class ShopAtUser(ManageTables):
     
     @classmethod
     async def update_storage_at_user(cls, items: dict, username: str, items_key: int) -> dict:
          async with cls.session.begin() as conn:
               sttm = select(User.storage).where(User.name == username)
               response = await conn.execute(sttm)
               
               storage: dict = json.loads(response.scalar())
               key = items[items_key]
               
               storage[items_key] = {
                    'price': key['price'],
                    'qua': key['qua'],
                    'name': key['name']
               }
               
               sttm = (
                    update(User).
                    where(User.name == username).
                    values(storage=json.dumps(storage))
               )
               await conn.execute(sttm)
          return {'status': 980, 'detail': 'Success add item in storage!'}
          
          
          
     @classmethod
     async def check_quantity_at_user(cls, items_id: list[int], q: int, username: str) -> tuple:
          async with cls.session.begin() as conn:
               sttm = select(User.storage).where(User.name == username)
               response = await conn.execute(sttm)
               
               sttm_base = select(Order.id)
               response_base = await conn.execute(sttm_base)
               
               result: dict = json.loads(response.scalar())
               result_base = response_base.scalars().all()
               
               deleter = []
               for item in items_id:
                    if item in result_base:
                         del result[str(item)]
                         deleter.append(item)
                    
               sttm = (
                    update(User).
                    where(User.name == username).
                    values(storage=json.dumps(result))
               )
               await conn.execute(sttm)
                         
               return {'status': 462, 'delete_items': deleter}
               
              
               
               
     @classmethod
     async def get_my_storage(cls, username: str) -> dict:
          async with cls.session() as conn:
               sttm = select(User.storage).where(User.name == username)
               response = await conn.execute(sttm)   # Storage user
               
               sttm_base = text('SELECT id FROM orders')
               response_base = await conn.execute(sttm_base)   # Items at server
               
               result_user: dict = json.loads(response.scalar())
               result_server: list = response_base.scalars().all()
               
               for key in result_user.keys():
                    if int(key) not in result_server:
                         result_user[key] = 'Нет в наличии :/'
               
               return result_user
               
                    
          
shopping = Shopping()
user_shop = ShopAtUser()