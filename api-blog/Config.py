import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSetting(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://ajarnkris:ajarnkris@ajarnkris.uv2vi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    DB_NAME: str = "AjarnKris"


class CommonSetting(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRE_MINUTES = 10080
    APP_NAME: str = "AjarnKris Blog API"
    DEBUG_MOODE: bool = False


class Settings(CommonSetting, DatabaseSetting, ServerSettings):
    pass


settings = Settings()
