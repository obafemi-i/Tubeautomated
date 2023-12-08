from schemas.schema import VideoAdd
from fastapi import UploadFile, HTTPException, status

import gridfs
import magic

from redis_om import get_redis_connection
from dotenv import dotenv_values

from utils.sentry import sentryMessage, sentryError, sentry

config = dotenv_values()


redis_connect = get_redis_connection(
    host = config['HOST'],
    port = config['PORT'],
    password = config['PASSWORD'],
    decode_responses = True
)


async def take_video(youtuber_email: str, video_description: str, 
               video_title: str, video_category_id: str, 
               file: UploadFile, current_user, database):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No file provided')
    
    
    # Validate file type
    allowed_video_types = ["mp4", "mpeg", "quicktime", "x-msvideo", "video/mkv", "mp4"]
    mime = magic.Magic()
    file_type = mime.from_buffer(file.file.read(2048)).lower()

    if not any(allowed_type in file_type for allowed_type in allowed_video_types):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid file type. Only video files are allowed')
    
    
    fs = gridfs.GridFS(database)

    try:
        file_id = fs.put(file.file, uploadby=current_user.get('name'), 
                         video_title=video_title, video_category_id=video_category_id,
                         video_description=video_description)
    except Exception as err:
        print(err)
        sentryError(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong, please try again.')


    queue_message = {
        'Notify': youtuber_email,
        'video_id': str(file_id),
        'Uploaded_by': str(current_user.get('name'))
    }

    try:
        redis_connect.xadd('videoDB_upload', queue_message, '*')
        print('queue message be',queue_message)
    except Exception as err:
        fs.delete(file_id)
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong here, please try again.')
    
    return 'Upload sucessful! The Youtuber will be notified.'



async def retreive_user_videos(current_user, database):
    names = []
    fs = gridfs.GridFS(database)
    for fid in fs.find({'uploadby': current_user}):
        names.append(fid.filename)
        
    if len(names) == 0:
        return "You haven't uploaded any videos yet."
    return names

