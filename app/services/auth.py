from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.asset import Asset
from app.config import Settings
from app.security.password import verify_password
from app.db import a_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str, session: AsyncSession = Depends(a_session)) -> User:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta, secret_key: str) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=Settings.ALGORITHM)
    return encoded_jwt


def get_current_user(session: AsyncSession = Depends(a_session), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        user = session.exec(select(User).where(User.id == payload.get("sub"))).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return user

