import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..models import Token, User
from ..services.auth import AuthService, get_current_user

SECRET = os.environ["JWT_SECRET"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["JWT_EXPIRATION"])

router = APIRouter(
    prefix='',
    tags=["auth"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login(request: Request,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                service: AuthService = Depends()):
    user_data = await service.get_user(form_data.username)
    if user_data:
        user = User.from_orm(user_data)
        if service.verify_password(form_data.password, user.password):
            access_token = service.create_access_token(
                data={"sub": user.email},
                expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400,
                                detail="Incorrect username or password")
    else:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")


@router.get("/")
async def users_list(current_user: Annotated[User, Depends(get_current_user)],
                     service: AuthService = Depends()):
    return {"admin": "admin"}
