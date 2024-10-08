import json

from fastapi import HTTPException
from sqlalchemy import select, update, text, delete

from src.database.models import Order, User, ManageTables


class Shopping(ManageTables):
     
     
     @classmethod
     async def get_all_items(cls) -> dict:
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
     async def get_one_item_(cls, item_id: int | None = None) -> dict | None:
          async with cls.session() as conn:
               if item_id:
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
                    return ()
               return None
          
          
          
     @classmethod
     async def check_quantity(cls, q: int, item_id: int) -> None | bool:
          async with cls.session() as conn:
               sttm = select(Order.qua).where(Order.id == int(item_id))
               response = await conn.execute(sttm)
               
               quantity = response.scalar()               
               if q <= quantity and q >= 1:
                    return True
               return None
           
          
          
class UserShop(ManageTables):
     shop = Shopping()
     
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
          return {'status': 212, 'detail': 'Success add item in storage!'}
          
          
          
          
     @classmethod
     async def check_quantity_at_user(cls, items_id: list[int], username: str) -> dict:
          async with cls.session.begin() as conn:
               sttm = select(User.storage).where(User.name == username)
               response = await conn.execute(sttm)
               
               sttm_base = select(Order.id)
               response_base = await conn.execute(sttm_base)
               
               result: dict = json.loads(response.scalar())
               result_base = response_base.scalars().all()
               
               deleter = []
               for item in items_id:
                    if item in result_base and str(item) in result.keys():
                         del result[str(item)]
                         deleter.append(item)
                    
               sttm = (
                    update(User).
                    where(User.name == username).
                    values(storage=json.dumps(result))
               )
               await conn.execute(sttm)      
          return {'status': 213, 'delete_items': deleter}
               
              
               
               
               
     @classmethod
     async def get_my_storage(cls, username: str) -> dict:
          async with cls.session() as conn:
               sttm = select(User.storage).where(User.name == username)
               response = await conn.execute(sttm)   # Storage user
               
               sttm_base = select(Order.id)
               response_base = await conn.execute(sttm_base)   # Items at server
               
               result_user: dict = json.loads(response.scalar())
               result_server: list[int] = response_base.scalars().all()
               
               for key in result_user.keys():
                    if int(key) not in result_server:
                         result_user[key] = 'Нет в наличии :/'
          return result_user
          
          
          
     @classmethod
     async def get_balance(cls, username: str) -> int:
          async with cls.session() as conn:
               sttm = select(User.money).where(User.name == username)
               response = await conn.execute(sttm)
               
               return response.scalar()
          
          
     @classmethod
     async def update_balance_at_user(cls, username: str, user_balance: int, price: int) -> None:
          async with cls.session.begin() as conn:
               sttm = (
                    update(User).
                    where(User.name == username).
                    values(money = user_balance - price)
               )
               await conn.execute(sttm)
               
               
     @classmethod
     async def update_quantity(cls, q: int, item_id: int) -> None:
          async with cls.session.begin() as conn:
               sttm = select(Order.qua).where(Order.id == item_id)
               response = await conn.execute(sttm)
               
               result = response.scalar() - q
               sttm = (
                    update(Order).
                    where(Order.id == item_id).
                    values(qua = result)
               )
               if result <= 0:
                    sttm = (
                         delete(Order).
                         where(Order.id == item_id)
                    )
               await conn.execute(sttm)
          
          
     @classmethod
     async def bougt_item(cls, item: int, username: str) -> dict:
          balance = await cls.get_balance(username)
          storage = await cls.get_my_storage(username)
          
          if str(item) not in storage.keys():
               raise HTTPException(status_code=448, detail='Item was not found in your storage!')
          
          
          if isinstance(storage[str(item)], str):
               raise HTTPException(status_code=451, detail='Item was finished...')
               
               
          if storage[str(item)]['price'] > balance:
               raise HTTPException(status_code=449, detail='Not enough money!')
          
          
          qua = await cls.shop.check_quantity(q=storage[str(item)]['qua'], item_id=item)
          if not qua:
               raise HTTPException(status_code=450, detail='The store has less quantity.')
          
          await cls.update_balance_at_user(
               username=username, 
               user_balance=balance, 
               price=storage[str(item)]['price']
          )
          await cls.update_quantity(
               q=storage[str(item)]['qua'],
               item_id=item
          )
          await cls.check_quantity_at_user(
               items_id=[item],
               username=username
          )
          return {'status': 214, 'detail': f'Item {item} bought success!'}
          
          
          
shopping = Shopping()
user_shop = UserShop()
