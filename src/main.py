from fastapi import FastAPI, File, UploadFile, HTTPException, status, Depends
from pymongo import MongoClient
from dotenv import dotenv_values
from redis_om import get_redis_connection

import gridfs
from contextlib import asynccontextmanager

from auth.access import get_current_user, router
from schema.schema import Video
from modules.sentry import sentryMessage
from auth.oauth import authenticate_with_oauth

config = dotenv_values()

redis_connect = get_redis_connection(
    host = config['HOST'],
    port = config['PORT'],
    password = config['PASSWORD'],
    decode_responses = True
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app start
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]
    
    print('Connected to mongodb database.')

    yield

    # app shutdown
    app.mongodb_client.close()
    print('Connection closed.')


app = FastAPI(lifespan=lifespan)
# app = FastAPI()
google_auth = authenticate_with_oauth()

app.include_router(router)

# fs = gridfs.GridFS(app.database)

@app.get('/')
def read_root():
    sentryMessage('Server is running..')
    return 'Server running...'


@app.post('/upload')
async def upload_video(to_notify: str, additional_message: str | None = None, file: UploadFile = File(...), current_user = Depends(get_current_user)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No file provided')
    
    fs = gridfs.GridFS(app.database)

    print('current user', current_user.get('sub'))
    print('current user', current_user['name'])
    
    try:
        file_id = fs.put(file.file, filename=file.filename, uploadby=current_user)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong, pleae try again')
    
    queue_message = {
        'Notify': to_notify,
        'Video_id': str(file_id),
        'Video_title': str(file.filename),
        'Uploaded_by': str(current_user),
        'Extras': additional_message
    }

    try:
        redis_connect.xadd('video_upload', queue_message, '*')
    except Exception as err:
        fs.delete(file_id)
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong, please try again')
    
    return 'upload successful'


@app.get('/get-videos')
def retreive(current_user = Depends(get_current_user)):
    names = []
    fs = gridfs.GridFS(app.database)
    for fid in fs.find({'uploadby': current_user}):
        names.append(fid.filename)
        
    if len(names) == 0:
        return "You haven't uploaded any videos yet."
    return names

