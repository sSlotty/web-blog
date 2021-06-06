import datetime
import uuid
from typing import Any, Dict

from fastapi import APIRouter, Body, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from crud.crud_user import getAll, post, login, get_current_active_user, refresh, getByID, delete
from models.ResponseModel import ResponseModel

router = APIRouter()


@router.get("")
async def read_items(_token: str = Depends(get_current_active_user)) -> Any:
    user = await getAll()
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post("/signup")
async def signup(payload: Dict = Body(...)) -> Any:
    data = jsonable_encoder(payload | {'_id': str(uuid.uuid4().int)[0:5], 'update_at': datetime.datetime.now(),
                                       'create_at': datetime.datetime.now(), 'disabled': False})
    req = await post(data)
    return JSONResponse(status_code=req['code'], content=req)


@router.post("/token")
async def token(payload: Dict = Body(...)) -> Any:
    data = jsonable_encoder(payload)
    req = await login(data)
    return JSONResponse(status_code=req['code'], content=req)


@router.post("/refresh")
async def refresh_token(_token: str = Depends(refresh)) -> Any:
    return JSONResponse(status_code=int(_token['code']), content=_token)


@router.get("/me")
async def get_profile(_token: str = Depends(get_current_active_user)) -> Any:
    user = _token
    res = ResponseModel.SuccessResponseModel(user, status.HTTP_200_OK, "OK")
    return JSONResponse(status_code=status.HTTP_200_OK, content=res)


@router.get("/{userID:path}")
async def get_profile_by_id(userID: str, _token: str = Depends(get_current_active_user)) -> Any:
    request = await getByID(userID)
    return JSONResponse(status_code=request['code'], content=request)


@router.delete("/delete")
async def delete_profile(payload: Dict = Body(...), _token: str = Depends(get_current_active_user)) -> Any:
    request = await delete(payload['id'])
    # print(payload)
    return JSONResponse(status_code=request['code'], content=request)
