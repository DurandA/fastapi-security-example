from typing import Union, List
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    user_uuid: Union[UUID, None] = None
    scopes: List[str] = []
