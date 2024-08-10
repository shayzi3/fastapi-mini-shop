import asyncio
import uvicorn

from fastapi import FastAPI
from src.database.models import startUp

from src.routers.auth import register
from src.routers.magazine import shopp


app = FastAPI()


app.include_router(register.router)
app.include_router(shopp.router)


if __name__ == '__main__':
     # asyncio.run(startUp())
     uvicorn.run('main:app', reload=True)