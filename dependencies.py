from typing import Union

from fastapi import Cookie, Depends, FastAPI
from sqlmodel import Session

from database import engine


def get_session():
    print('get_session')
    with Session(engine) as session:
        yield session