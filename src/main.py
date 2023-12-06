from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
from dotenv import dotenv_values

from contextlib import asynccontextmanager

from routes.auth import router as authroute
from routes.videos import router as videorouter

from crud.video import take_video, retreive_user_videos
from security.oauth import get_current_user

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
async def read_root():
    return 'Server is running..'

# def video_db(body: VideoAdd,file: UploadFile = File(...), current_user = Depends(get_current_user)):

@app.post('/upload-video-to-db', tags=['Videos'])
async def video_db(youtuber_email: str, video_description: str, 
               video_title: str, video_category_id: str,file: UploadFile = File(...), current_user = Depends(get_current_user)):
    # print('add be', add.youtuber_email)
    return await take_video(youtuber_email, video_description, video_title, video_category_id, file=file, current_user=current_user, database=app.database)



@app.get('/all-videos')
def get_user_video(current_user = Depends(get_current_user)):
    files = retreive_user_videos(current_user, app.database)
    return files
