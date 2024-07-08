import asyncio
import uvicorn

from fastapi import FastAPI
from src.database.models import startUp


app = FastAPI()


if __name__ == '__main__':
     asyncio.run(startUp())
     # uvicorn.run('main:app', reload=True)