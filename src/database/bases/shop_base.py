import json

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
                    items[data[1]] = {
                         'ID': data[0],
                         'Price': data[2],
                         'Qua': data[3]
                    }
               return items
                    
          
     @classmethod
     async def get_one_item_(cls, item: str) -> dict:
          async with cls.session() as conn:
               sttm = select(Order).where(Order.item == item)
               
               response = await conn.execute(sttm)
               response = response.scalar()
               
               if response:
                    return {response.item: {
                         'price': response.price, 
                         'qua': response.qua, 
                         'id': response.id, 
                         'seller': response.seller
                         }
                    }
               return None
          
          
     @classmethod
     async def check_quantity(cls, q: int, item: str) -> None:
          async with cls.session() as conn:
               sttm = select(Order.qua).where(Order.item == item)
               
               response = await conn.execute(sttm)
               
               if q <= response.scalar():
                    return True
               return None
          
          
shopping = Shopping()