from datetime import timedelta
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from auth.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                       create_access_token)
from dependencies import get_session
from models.auth_models import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        'given_name': user.given_name,
        'family_name': user.family_name,
        'email': user.email,
    }
    access_token = create_access_token(
        data={"sub": str(user.uuid), "scopes": ["app"], **claims},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
