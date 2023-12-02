from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient

import gridfs
from contextlib import asynccontextmanager

from dotenv import dotenv_values

from routes.auth import router as authroute
from routes.videos import router as videorouter


config = dotenv_values()

@asynccontextmanager
async def lifesapn(app: FastAPI):
    # app start
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]

    print('Connected to Mongodb.')

    yield

    # app shutdown
    app.mongodb_client.close()
    print('Mongodb connection closed.')


app = FastAPI(lifespan=lifesapn)
# app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authroute)
app.include_router(videorouter)


@app.get('/', tags=['Home'])
def read_root():
    return 'Server is running..'