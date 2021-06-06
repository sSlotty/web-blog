import datetime
import uuid
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from crud.crud_article import post, getArticles, getArticleByID, addView, deleteArticle
from crud.crud_user import get_current_active_user

router = APIRouter()


@router.get("")
async def get(reverse: bool = False, key: str = 'create_at') -> Any:
    request = await getArticles(reverse, key)
    return JSONResponse(status_code=request['code'], content=request)


@router.get("/{id:path}")
async def getByID(id: str) -> Any:
    request = await getArticleByID(id)
    return JSONResponse(status_code=request['code'], content=request)


@router.post("/create")
async def create(payload: Dict = Body(...), _token: str = Depends(get_current_active_user)) -> Any:
    data = jsonable_encoder(payload | {'_id': str(uuid.uuid4().int)[0:5], 'update_at': datetime.datetime.now(),
                                       'create_at': datetime.datetime.now(), 'disabled': False,
                                       'writerID': _token[0]['_id'],
                                       'view': 0})
    request = await post(data)
    return JSONResponse(status_code=request['code'], content=request)


@router.put("/edit/{id:path}")
async def put(payload: Dict = Body(...), _token: str = Depends(get_current_active_user)) -> Any:
    pass


@router.put("/add-view/{id:path}")
async def add_view(id: str) -> Any:
    request = await addView(id)
    return JSONResponse(status_code=request['code'], content=request)


@router.delete("/")
async def delete(payload: Dict = Body(...), _token: str = Depends(get_current_active_user)) -> Any:
    request = await deleteArticle(payload['id'])
    return JSONResponse(status_code=request['code'], content=request)


# Articles view
@router.get("/view")
async def articlesView() -> Any:
    pass
