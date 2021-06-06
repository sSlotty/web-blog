from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import Request, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.ResponseModel import ResponseModel
from models.Users import UserModel, TokenData

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from Config import settings
from crud.database import db

TABLE: str = "users"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    encode_jwt = jwt.encode(encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encode_jwt


async def getAll() -> Any:
    data = []
    user = db.users.find()
    if user.count() > 0:
        for doc in user:
            del doc['password']
            data.append(doc)
        return ResponseModel.SuccessResponseModel(data=data, code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(data=data, code=status.HTTP_204_NO_CONTENT, message="NO CONTENT")


async def getByID(userID: str) -> Any:
    data = []
    user = db.users.find({"_id": userID})
    if user.count() > 0:
        for i in user:
            del i['password']
            data.append(i)
        return ResponseModel.SuccessResponseModel(data=data, code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(data=data, code=status.HTTP_204_NO_CONTENT, message="NO CONTENT")


async def getUserByUsername(username: str) -> Any:
    data = []
    users = db.users.find({'username': username})
    if users.count() > 0:
        for user in users:
            del user['password']
            data.append(user)
    return data


async def post(payload: UserModel) -> ResponseModel:
    user = db.users.find({'username': payload['username']})
    mail = db.users.find({'email': payload['email']})
    if user.count() <= 0 and mail.count() <= 0:
        data = payload | {'password': get_password_hash(payload['password'])}
        new_user = db.users.insert_one(data)
        create_user = db.users.find_one(
            {"_id": new_user.inserted_id})
        del create_user['password']
        return ResponseModel.SuccessResponseModel(data=create_user, code=status.HTTP_201_CREATED, message="success")

    return ResponseModel.ErrorResponseModel(code=status.HTTP_208_ALREADY_REPORTED, message="Already have username")


async def delete(id: str) -> ResponseModel:
    user = db.users.find({'_id': id})
    if user.count() > 0:
        db.users.update({
            '_id': id
        }, {
            '$set': {
                'disabled': True
            }
        })
        return ResponseModel.SuccessResponseModel(code=status.HTTP_200_OK, message="Success to delete")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_404_NOT_FOUND, message="Not found")


async def login(payload: UserModel) -> ResponseModel:
    user = db.users.find({'username': payload['username']})

    if user.count() > 0:
        if user[0]['disabled']:
            return ResponseModel.ErrorResponseModel(code=status.HTTP_403_FORBIDDEN, message="Account username is {} "
                                                                                            "has block form "
                                                                                            "admin".format(
                payload['username']))
        verify = verify_password(payload['password'], user[0]['password'])
        if verify:
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

            access_token = create_token({"username": user[0]['username'], "role": user[0]['role']},
                                        expires_delta=access_token_expires)
            refresh_token = create_token({"username": user[0]['username'], "role": user[0]['role']},
                                         expires_delta=refresh_token_expires)
            response = {
                'role': user[0]['role'],
                'access_token': access_token,
                'token_type': "Bearer",
                'access_token_expires': settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                'refresh_token': refresh_token,
                'refresh_token_expires': settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            }
            return ResponseModel.SuccessResponseModel(data=response, code=status.HTTP_200_OK, message='OK')
        return ResponseModel.ErrorResponseModel(code=status.HTTP_403_FORBIDDEN,
                                                message="incorrect username or password")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_403_FORBIDDEN, message="incorrect username or password")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('username')
        role: str = payload.get('role')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = await getUserByUsername(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user[0]['disabled']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def refresh(current_user: UserModel = Depends(get_current_user)):
    if current_user[0]['disabled']:
        return ResponseModel.ErrorResponseModel(code=status.HTTP_200_OK, message='refresh token error')
    access_token_expires = timedelta(minutes=1)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token({"username": current_user[0]['username'], "role": current_user[0]['role']},
                                expires_delta=access_token_expires)
    refresh_token = create_token({"username": current_user[0]['username'], "role": current_user[0]['role']},
                                 expires_delta=refresh_token_expires)
    response = {
        'role':  current_user[0]['role'],
        'access_token': access_token,
        'token_type': "Bearer",
        'access_token_expires': settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        'refresh_token': refresh_token,
        'refresh_token_expires': settings.REFRESH_TOKEN_EXPIRE_MINUTES,

    }
    return ResponseModel.SuccessResponseModel(data=response, code=status.HTTP_200_OK, message='OK')
