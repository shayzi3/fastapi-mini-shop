import asyncio
import uvicorn

from fastapi import FastAPI
from src.database.models import startUp

from src.routers.auth.code import register, data_user, changers
from src.routers.magazine.code import shopp


app = FastAPI()


app.include_router(register.router)
app.include_router(shopp.router)
app.include_router(data_user.router)
app.include_router(changers.router)



if __name__ == '__main__':
     # asyncio.run(startUp())
     uvicorn.run('main:app', reload=True)