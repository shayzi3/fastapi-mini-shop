import uvicorn

from fastapi import FastAPI

from src.routers.auth.code import register, data_user, changers
from src.routers.magazine.code import shop, buy


app = FastAPI()


app.include_router(register.router)
app.include_router(shop.router)
app.include_router(data_user.router)
app.include_router(changers.router)
app.include_router(buy.router)



if __name__ == '__main__':
     uvicorn.run('main:app', reload=True)