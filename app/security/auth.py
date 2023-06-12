from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.models.user import User
from app.config import settings
from app.security.password import verify_password
from app.models.asset import Asset
from app.services.auth import  get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def authenticate_user(session: Session, username: str, password: str) -> User:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password_hash(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user = session.exec(select(User).where(User.id == payload.get("sub"))).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return user


def check_user_is_owner_or_admin(user: User) -> bool:
    return user.is_admin or Asset.owner_id == user.id
