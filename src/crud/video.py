from schemas.schema import Video
from fastapi import UploadFile

import gridfs

from redis_om import get_redis_connection
from dotenv import dotenv_values


config = dotenv_values()


redis_connect = get_redis_connection(
    host = config['HOST'],
    port = config['PORT'],
    password = config['PASSWORD'],
    decode_responses = True
)


def take_video(request: Video, file: UploadFile, current_user, database):
    if not file:
        return {'status': 400,
                'message': 'No file provided'}
    
    fs = gridfs.GridFS(database)

    try:
        file_id = fs.put(file.file, request, uploadby=current_user)
    except Exception as err:
        print(err)
        return {'status': 500,
                'message': 'Something went wrong, please try again.'}
    
    queue_message = {
        'Notify': request.youtuber_email,
        'video_id': str(file_id),
        'Uploaded_by': str(current_user)
    }

    try:
        redis_connect.xadd('videoDB_upload', queue_message, '*')
    except Exception as err:
        fs.delete(file_id)
        print(err)
        return {'status': 500,
                'message': 'Something went wrong, please try again.'} 
    
    return 'Upload sucessful!'

