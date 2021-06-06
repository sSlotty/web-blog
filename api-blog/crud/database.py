from pydantic import BaseSettings
from pymongo import MongoClient
from Config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]


