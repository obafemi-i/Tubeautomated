from fastapi import APIRouter, Depends, HTTPException, status
from crud.video import take_video
from schemas.schema import TokenData

from security.oauth import get_current_user
from utils.sentry import sentryMessage


router = APIRouter(tags=['Videos'])

@router.post('/add-video')
async def collect_videos(current_user: TokenData = Depends(get_current_user)):
    sentryMessage(f'Login succesful, welcome {current_user.first_name}')
    return f'Login succesful, welcome {current_user.first_name}'

