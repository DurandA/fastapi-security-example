from uuid import UUID, uuid4
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field(max_length=256, min_length=6)
    given_name: str
    family_name: str


class UserInput(SQLModel):
    email: EmailStr
    password: str = Field(max_length=256, min_length=6)
    given_name: str
    family_name: str


class UserRead(SQLModel):
    uuid: UUID
    email: str
    given_name: str
    family_name: str


class UserPatch(SQLModel):
    password: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
