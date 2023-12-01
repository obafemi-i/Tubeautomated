from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as authroute
from routes.videos import router as videorouter
app = FastAPI()

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