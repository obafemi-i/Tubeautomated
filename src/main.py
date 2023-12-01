from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as authroute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authroute)


@app.get('/', tags=['Home'])
def read_root():
    return 'Server is running..'