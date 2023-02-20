from fastapi import APIRouter, Depends
from sqlmodel import Session

from auth.auth import get_current_app_user, get_current_user, get_password_hash
from dependencies import get_session
from models.user_model import User, UserInput, UserPatch, UserRead

router = APIRouter()


@router.post('/registration', status_code=201, response_model=UserRead, tags=['users'],
                  description='Register new user')
def register(user: UserInput, session: Session = Depends(get_session)):    
    hashed_pwd = get_password_hash(user.password)
    u = User(
        email=user.email,
        password=hashed_pwd,
        given_name=user.given_name,
        family_name=user.family_name)
    session.add(u)
    session.commit()
    return u


@router.patch('/users/me', response_model=UserRead, tags=['users'])
async def patch_self_user(user: UserPatch, current_user: User = Depends(get_current_app_user), session: Session = Depends(get_session)):
    update_data = user.dict(exclude_unset=True)
    if 'password' in update_data:
        password = update_data.pop('password')
        current_user.password = get_password_hash(password)
    for key, val in update_data.items():
        current_user.__setattr__(key, val)
    session.add(current_user)
    session.commit()
    return current_user
