import uuid
from typing import Optional
from pydantic import BaseModel, Field

from datetime import datetime


class ArticlesModel(BaseModel):
    id: Optional[str] = Field(default_factory=str(uuid.uuid4().int)[0:5], alias="_id")
    name: Optional[str] = Field(...)
    content: Optional[str] = Field(...)
    banner: Optional[str] = Field(...)
    writerID: Optional[str] = Field(...)
    create_at: datetime = Field(...)
    update_at: datetime = Field(...)
    view: Optional[int] = Field(...)
    disabled: Optional[bool] = None


class ViewModel(BaseModel):
    id: Optional[str] = Field(default_factory=str(uuid.uuid4().int)[0:5], alias="_id")
    article_id: Optional[str] = Field(...)
    create_at: datetime = Field(...)
