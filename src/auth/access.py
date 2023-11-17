from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import dotenv_values

import requests

router = APIRouter()

config = dotenv_values()

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = 'HS256'
AUTH_SERVICE_URL = config['AUTH_SERVICE_URL']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return payload.get('sub')
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate credentials')
    


# This endpoint requests authentication from the auth service and returns a token that gives the user access to the app
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    payload = {'username': request.username, 'password': request.password}

    response = requests.post(AUTH_SERVICE_URL, payload)

    if response.status_code == 200:
        token = response.json().get('access_token')
        return {'access_token': token}
    else:
        raise HTTPException(status_code=401, detail='Invalid Credentials')
    
