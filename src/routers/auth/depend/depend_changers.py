

from typing import Annotated
from fastapi import Depends, Response, HTTPException

from src.routers.auth.schemas import NewName
from src.auth2 import auth
from src.database.bases.auth_base import check, regstr
from src.routers.auth.core import helper



async def depend_name_change(
     data: NewName,
     token: Annotated[dict, Depends(auth.check_refresh_and_access_tokens)],
     response: Response
     
) -> dict:

     await helper.check_registration_name(
          arg=data.new_name
     )
     ps = await check.check_password(
          name=token.get('sub'),
          password=data.password
     )
     if ps:
          await auth.get_access_refresh_tokens(
               username=data.new_name, 
               response=response
          )
          return await regstr.save_new_name(
               name=token.get('sub'),
               new_name=data.new_name
          )
     raise HTTPException(status_code=445, detail='Invalid password!')