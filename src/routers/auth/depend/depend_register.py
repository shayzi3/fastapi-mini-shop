
from typing import Annotated
from fastapi import (
     Response, 
     HTTPException, 
     Request, 
     Body,
     Depends
)
from src.routers.auth.schemas import Reg, Auth
from src.routers.auth.core import helper
from src.database.bases.auth_base import regstr, check
from src.auth2 import auth




async def depend_register_user(data: Reg, response: Response) -> dict:
     await helper.check_registration_name(data.name)
     
     insert = await regstr.insert_new_data(data)
     if insert:
          return await auth.get_access_refresh_tokens(
               username=data.name, 
               response=response
          )
     raise HTTPException(status_code=440, detail='This name already taken!')




async def depend_auth_user(data: Auth, response: Response) -> dict:
     await helper.check_registration_name(data.name)
     
     passw = await check.check_password(
          name=data.name,
          password=data.password
     )
     if passw is False:
          raise HTTPException(status_code=442, detail='Invalid name or password!')

     await auth.get_access_refresh_tokens(
          username=data.name,
          response=response
     )
     return {'status': 206, 'detail': 'Success!'}
     



async def depend_delete_user(
     password: Annotated[str, Body(embed=True)],
     token: Annotated[dict, Depends(auth.check_refresh_and_access_tokens)],
     response: Response,
     request: Request
) -> dict:
     password_check = await check.check_password(
          name=token.get('sub'),
          password=password
     )
     if not password_check:
          raise HTTPException(status_code=442, detail='Invalid name or password!')
     
     await auth.cookies_delete(request, response)
     return await regstr.delete_user_account(name=token.get('sub'))