import datetime
import os
import uuid
from typing import Any, Dict, Optional

from fastapi import status

from models.ResponseModel import ResponseModel
from models.Articles import ArticlesModel

from Config import settings
from crud.database import db

import base64

SAVE_PATH = 'assets/images/'


async def getArticles(_reverse: bool = False, key: bool = "create_at") -> ResponseModel:
    articles = db.articles.find()
    data = []

    if articles.count() > 0:
        for article in articles:
            data.append(article)
        data.sort(key=lambda r: r[key], reverse=_reverse)
        return ResponseModel.SuccessResponseModel(data=data, code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_204_NO_CONTENT, message="NO Content")


async def getArticleByID(id: str) -> ResponseModel:
    articles = db.articles.find_one({'_id': id})
    if len(articles) > 0:
        return ResponseModel.SuccessResponseModel(data=[articles], code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_204_NO_CONTENT, message="NO Content")


async def post(payload: ArticlesModel) -> ResponseModel:
    img_data = base64.b64decode(payload['banner'])
    filename = '{}_{}.png'.format(payload['_id'],
                                  str(uuid.uuid4().int)[0:5])  # I assume you have a way of picking unique filenames
    with open(SAVE_PATH + filename, 'wb') as f:
        f.write(img_data)
    data = payload | {'images': filename, 'image_link': 'http://' + settings.HOST + ':3000/' + SAVE_PATH + filename}
    new_articles = db.articles.insert_one(data)
    create_articles = db.articles.find_one(
        {"_id": new_articles.inserted_id}
    )
    return ResponseModel.SuccessResponseModel(data=create_articles, code=status.HTTP_200_OK, message="OK")


async def put(payload: ArticlesModel) -> ResponseModel:
    pass


async def addView(id: ArticlesModel) -> ResponseModel:
    articles = await getArticleByID(id)
    if len(articles['data']) > 0:
        date = str(datetime.datetime.now())
        db.views.insert({'_id': str(uuid.uuid4().int)[0:5], 'idArticles': id, 'create_at': date})

        db.articles.update({
            '_id': id
        }, {
            '$set': {
                'view': articles['data'][0]['view'] + 1,
                'update_at': date
            }
        })
        data = db.articles.find_one({'_id': id})
        return ResponseModel.SuccessResponseModel(data=data, code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_204_NO_CONTENT, message="NO CONTENT")


async def deleteArticle(id: str) -> ResponseModel:
    articles = await getArticleByID(id)
    if len(articles['data']) > 0:
        date = str(datetime.datetime.now())
        db.articles.update({
            '_id': id
        }, {
            '$set': {
                'disabled': True,
                'update_at': date
            }
        })
        data = db.articles.find_one({'_id': id})
        return ResponseModel.SuccessResponseModel(data=data, code=status.HTTP_200_OK, message="OK")
    return ResponseModel.ErrorResponseModel(code=status.HTTP_204_NO_CONTENT, message="NO CONTENT")
