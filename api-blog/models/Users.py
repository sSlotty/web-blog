import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, UUID4

from enum import Enum


class Role(str, Enum):
    user = 'user'
    admin = 'admin'
    owner = 'owner'


class UserModel(BaseModel):
    id: Optional[str] = Field(default_factory=str(uuid.uuid4().int)[0:5], alias="_id")
    name: Optional[str] = Field(...)
    username: Optional[str] = Field(...)
    password: Optional[str] = Field(min_length=6)
    email: Optional[EmailStr] = Field(...)
    role: Optional[Role] = Field(..., alias='role')
    create_at: Optional[datetime] = Field(...)
    update_at: Optional[datetime] = Field(...)
    disabled: Optional[bool] = None


class UpdateUserModel(BaseModel):
    name: Optional[str] = Field(...)
    username: Optional[str] = Field(...)
    password: Optional[str] = Field(..., min_length=6)
    email: Optional[EmailStr] = Field(...)
    role: Optional[Role] = Field(..., alias='role')
    create_at: Optional[datetime] = Field(...)
    update_at: Optional[datetime] = Field(...)


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
